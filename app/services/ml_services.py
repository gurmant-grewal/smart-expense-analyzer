import json
import os

import joblib
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sqlalchemy.orm import Session

from app.repositories.expense_repository import ExpenseRepository
from app.utils import clean_text
from logging_config import logger


MODEL_FILE = "saved/model.pkl"
METRICS_FILE = "saved/model_metrics.json"
TRAINING_FILE = "data/training_data.csv"

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def load_model():
    """
    Load the trained ML model from disk.

    If the model does not exist, train a new model from
    the base training CSV.
    """

    if os.path.exists(MODEL_FILE):
        logger.info("Loading trained model...")
        return joblib.load(MODEL_FILE)

    logger.info(
        "No trained model found. Training model from training data..."
    )

    return train_base_model()


def train_base_model():
    """
    Train the initial ML model using data/training_data.csv.

    This function does not require a database session and is therefore
    safe to use during application startup and testing.
    """

    if not os.path.exists(TRAINING_FILE):
        raise FileNotFoundError(
            f"Training data not found: {TRAINING_FILE}"
        )

    logger.info("Loading base training data...")

    data = pd.read_csv(TRAINING_FILE)

    required_columns = {"text", "category"}

    if not required_columns.issubset(data.columns):
        raise ValueError(
            "Training CSV must contain 'text' and 'category' columns."
        )

    data = data.dropna(subset=["text", "category"])

    if len(data) < 2:
        raise ValueError(
            "Not enough training data to train the model."
        )

    data["text"] = data["text"].astype(str).apply(clean_text)
    data["category"] = data["category"].astype(str)

    if data["category"].nunique() < 2:
        raise ValueError(
            "Training data must contain at least two categories."
        )

    logger.info(
        "Generating embeddings for %d training samples...",
        len(data),
    )

    X = embedding_model.encode(
        data["text"].tolist(),
        show_progress_bar=False,
    )

    y = data["category"]

    # Use a train/test split when enough data is available.
    if len(data) >= 10:
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y if y.value_counts().min() >= 2 else None,
        )
    else:
        # Very small datasets cannot always be stratified safely.
        X_train = X
        y_train = y
        X_test = X
        y_test = y

    trained_model = LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
    )

    trained_model.fit(X_train, y_train)

    predictions = trained_model.predict(X_test)

    metrics = {
        "accuracy": float(
            accuracy_score(y_test, predictions)
        ),
        "precision": float(
            precision_score(
                y_test,
                predictions,
                average="weighted",
                zero_division=0,
            )
        ),
        "recall": float(
            recall_score(
                y_test,
                predictions,
                average="weighted",
                zero_division=0,
            )
        ),
        "f1_score": float(
            f1_score(
                y_test,
                predictions,
                average="weighted",
                zero_division=0,
            )
        ),
        "report": classification_report(
            y_test,
            predictions,
            zero_division=0,
        ),
        "training_samples": int(len(data)),
        "categories": list(y.unique()),
        "last_trained": str(pd.Timestamp.now()),
    }

    os.makedirs("saved", exist_ok=True)

    history = []

    if os.path.exists(METRICS_FILE):
        try:
            with open(METRICS_FILE, "r") as f:
                history = json.load(f)
        except (json.JSONDecodeError, OSError):
            history = []

    history.append(metrics)

    with open(METRICS_FILE, "w") as f:
        json.dump(history, f, indent=4)

    joblib.dump(trained_model, MODEL_FILE)

    logger.info(
        "Base ML model trained and saved successfully."
    )

    return trained_model


model = load_model()


def predict_category(text: str):
    """
    Predict the expense category and return:

        (category, confidence)

    Example:

        ("Food", 0.91)
    """

    if not text or not text.strip():
        return "Unknown", 0.0

    cleaned_text = clean_text(text)

    vector = embedding_model.encode(
        [cleaned_text],
        show_progress_bar=False,
    )

    prediction = model.predict(vector)[0]

    confidence = float(
        model.predict_proba(vector).max()
    )

    if confidence < 0.50:
        return "uncertain", confidence

    return str(prediction), confidence


def should_retrain(db: Session):
    """
    Determine whether the model should be retrained.

    Retraining occurs after every 20 verified expenses.
    """

    count = ExpenseRepository.verify_expense_count(db)

    return count > 0 and count % 20 == 0


def retrain_model(db: Session):
    """
    Retrain the ML model using:

    1. Base training data from training_data.csv
    2. Verified expenses from the database
    """

    global model

    try:
        logger.info("Retraining ML model...")

        training_data = pd.read_csv(TRAINING_FILE)

        verified = ExpenseRepository.get_verified_expenses(db)

        verified_df = pd.DataFrame(
            [
                {
                    "text": expense.text,
                    "category": expense.category,
                }
                for expense in verified
            ]
        )

        data = pd.concat(
            [training_data, verified_df],
            ignore_index=True,
        )

        if len(data) < 20:
            logger.warning(
                "Not enough data for retraining."
            )
            return

        data = data.dropna(
            subset=["text", "category"]
        )

        data["text"] = data["text"].astype(str).apply(clean_text)
        data["category"] = data["category"].astype(str)

        if data["category"].nunique() < 2:
            logger.warning(
                "Need at least two categories for retraining."
            )
            return

        X = embedding_model.encode(
            data["text"].tolist(),
            show_progress_bar=False,
        )

        y = data["category"]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y if y.value_counts().min() >= 2 else None,
        )

        new_model = LogisticRegression(
            max_iter=2000,
            class_weight="balanced",
        )

        new_model.fit(X_train, y_train)

        predictions = new_model.predict(X_test)

        metrics = {
            "accuracy": float(
                accuracy_score(y_test, predictions)
            ),
            "precision": float(
                precision_score(
                    y_test,
                    predictions,
                    average="weighted",
                    zero_division=0,
                )
            ),
            "recall": float(
                recall_score(
                    y_test,
                    predictions,
                    average="weighted",
                    zero_division=0,
                )
            ),
            "f1_score": float(
                f1_score(
                    y_test,
                    predictions,
                    average="weighted",
                    zero_division=0,
                )
            ),
            "report": classification_report(
                y_test,
                predictions,
                zero_division=0,
            ),
            "training_samples": int(len(data)),
            "categories": list(y.unique()),
            "last_trained": str(pd.Timestamp.now()),
        }

        os.makedirs("saved", exist_ok=True)

        history = []

        if os.path.exists(METRICS_FILE):
            try:
                with open(METRICS_FILE, "r") as f:
                    history = json.load(f)
            except (json.JSONDecodeError, OSError):
                history = []

        history.append(metrics)

        with open(METRICS_FILE, "w") as f:
            json.dump(history, f, indent=4)

        joblib.dump(new_model, MODEL_FILE)

        model = new_model

        logger.info(
            "Model retrained and saved successfully."
        )

    except Exception:
        logger.exception(
            "Model retraining failed."
        )
        raise