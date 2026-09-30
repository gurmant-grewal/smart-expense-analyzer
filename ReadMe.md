💰 AI-Powered Personal Expense Tracker

An intelligent expense tracking application built with FastAPI, Streamlit, SQLite, SQLAlchemy, and Machine Learning that automatically categorizes expenses, provides spending analytics, generates AI-powered insights, and continuously improves its prediction model using user feedback.

⸻

Features

Expense Management

* Add daily expenses
* Automatic expense categorization using Machine Learning
* Manual category correction
* Merchant extraction from expense descriptions
* Secure user-specific expense storage

Authentication & Security

* User Registration
* User Login
* Password hashing using BCrypt
* JWT Authentication for protected FastAPI endpoints

Machine Learning

* Sentence Transformer embeddings (all-MiniLM-L6-v2)
* Logistic Regression classifier
* Confidence score for every prediction
* User feedback collection
* Automatic model retraining after sufficient verified data
* Model performance tracking

Analytics

* Daily spending summary
* Weekly spending summary
* Monthly spending summary
* Top spending categories
* Top merchants
* Largest merchant
* Daily spending visualization
* Category-wise spending visualization

AI Insights

* Spending increase detection
* Spending decrease detection
* Percentage change calculation
* Daily spending comparison

Testing

* Authentication tests
* API endpoint tests
* Machine Learning prediction tests

⸻

Tech Stack

Backend

* FastAPI
* SQLAlchemy
* SQLite
* Pydantic

Frontend

* Streamlit

Machine Learning

* Sentence Transformers
* Scikit-learn
* Logistic Regression
* Joblib
* Pandas

Security

* JWT Authentication
* Passlib (BCrypt)
* Python-JOSE

Testing

* Pytest
* FastAPI TestClient

⸻

Project Structure

Expense-Tracker/
│
├── app/
│   ├── repositories/
│   ├── security/
│   ├── services/
│   ├── api.py
│   ├── models.py
│   ├── schemas.py
│   ├── constants.py
│   └── utils.py
│
├── dashboard/
│   ├── add_expense.py
│   ├── analytics.py
│   ├── AI_insight.py
│   ├── login.py
│   ├── registration.py
│   ├── ml_model_performance.py
│   └── main_dashboard.py
│
├── data/
│   ├── expenses.db
│   └── training_data.csv
│
├── saved/
│   ├── model.pkl
│   └── model_metrics.json
│
├── tests/
│
├── database.py
├── database_session.py
├── init_db.py
├── logging_config.py
└── requirements.txt

⸻

System Architecture

             +---------------------+
             |     Streamlit UI    |
             +----------+----------+
                        |
                        |
               Business Logic
                        |
                        |
      +-----------------+-----------------+
      |                                   |
Expense Services                  Analytics Services
      |                                   |
      +-----------------+-----------------+
                        |
                  Repository Layer
                        |
                  SQLAlchemy ORM
                        |
                    SQLite Database
                        |
               Machine Learning Model
                        |
          Sentence Transformer + Logistic Regression

⸻

Machine Learning Pipeline

Expense Text
      │
      ▼
Text Cleaning
      │
      ▼
Sentence Embeddings
(all-MiniLM-L6-v2)
      │
      ▼
Logistic Regression
      │
      ▼
Predicted Category
      │
      ▼
User Feedback
      │
      ▼
Verified Dataset
      │
      ▼
Automatic Retraining

⸻

Database Schema

Users

Column	Type
id	Integer
username	String
password	String

⸻

Expenses

Column	Type
id	Integer
user_id	Integer
date	DateTime
text	String
category	String
amount	Float
merchant	String
feedback_verified	Boolean

⸻

API Endpoints

Authentication

Register

POST /register

Login

POST /login

Returns a JWT Access Token.

⸻

Expense Analysis

POST /expenses/analyze

Predicts the category of an expense.

⸻

Save Expense

POST /expenses

Protected endpoint requiring JWT authentication.

⸻

Expense Summary

GET /summary/{daily|weekly|monthly}

Protected endpoint requiring JWT authentication.

⸻

Installation

Clone the repository

git clone https://github.com/gurmant-grewal/ai-expense-tracker.git

Move into the project directory

cd AI-Expense-Tracker

Install dependencies

pip install -r requirements.txt

Initialize the database

python init_db.py

⸻

Running the Backend

uvicorn app.api:app --reload

Swagger UI

http://127.0.0.1:8000/docs

⸻

Running the Dashboard

streamlit run dashboard/main_dashboard.py

⸻

Running Tests

pytest

or

pytest -v

⸻

Model Retraining

Whenever enough verified expenses are collected, the application automatically:

* Reads verified expenses
* Combines them with training data
* Generates sentence embeddings
* Retrains the Logistic Regression model
* Evaluates model performance
* Saves:
    * Updated model
    * Performance metrics
    * Classification report

⸻

Security Features

* BCrypt password hashing
* JWT Authentication
* Protected FastAPI endpoints
* SQLAlchemy ORM
* Pydantic request validation

⸻

Future Improvements

* Docker support
* PostgreSQL deployment
* Redis caching
* OAuth2 (Google Login)
* Expense OCR from receipts
* Multi-currency support
* Budget planning
* Email notifications
* Monthly AI reports
* Cloud deployment (AWS/Azure/GCP)

⸻

Learning Outcomes

This project demonstrates practical implementation of:

* FastAPI REST APIs
* Repository Pattern
* Service Layer Architecture
* SQLAlchemy ORM
* JWT Authentication
* Password Hashing
* Streamlit Dashboards
* Machine Learning Integration
* Sentence Transformers
* Logistic Regression
* Model Retraining
* Automated Testing
* Software Engineering Best Practices

⸻

Author

Your Name

LinkedIn: https://linkedin.com/in/gurmant-grewal

GitHub: https://github.com/gurmant-grewal

⸻

License

This project is licensed under the MIT License.
