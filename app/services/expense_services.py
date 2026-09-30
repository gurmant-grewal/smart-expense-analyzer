from app.services.ml_services import predict_category as predict_category_model
from app.utils import extract_merchant
from app.models import Expense
from sqlalchemy.orm import Session
from logging_config import logger
from app.repositories.user_repository import UserRepository
from app.repositories.expense_repository import ExpenseRepository
from app.services.ml_services import retrain_model,should_retrain


def analyze_expense(text:str,amount:float):
    category,confidence=predict_category_model(text)
    merchant=extract_merchant(text)

    logger.info("Predicted category for '%s': %s (confidence: %.2f)", text, category, confidence)
    
    return {
        "text": text,
        "category": category,
        "amount": amount,
        "confidence": confidence,
        "merchant": merchant
    }

def add_expense(
    db: Session,
    username: str,
    text: str,
    amount: float,
    predicted_category: str,
    corrected_category: str | None = None) -> Expense:
   
    
        

   
    current_user= UserRepository.get_user_by_username(db,username)
    if current_user is None:
        logger.warning("user not found: %s",username)
        raise ValueError("User not found")
    
    
    
 
    new_expense=Expense(
    user_id=current_user.id,
    text= text,
    category=corrected_category or predicted_category,
    amount=amount,
    feedback_verified=True,
    merchant=extract_merchant(text)
    )
    
    ExpenseRepository.create_expense(db,new_expense)

    if should_retrain(db):

        retrain_model(db)
        logger.info("madel has been retrained due to new data")

    

    logger.info("New expense added: %s", new_expense)
    return new_expense
