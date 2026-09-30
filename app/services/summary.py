from datetime import datetime
from database import SessionLocal
from app.repositories.expense_repository import ExpenseRepository
from sqlalchemy.orm import Session


def get_summary(db: Session, summary_type: str, username:str):
    from app.repositories.user_repository import UserRepository

    current_user = UserRepository.get_user_by_username(
    db,
    username
    )

    if current_user is None:
        raise ValueError("User not found")

    if summary_type=="daily":
        return ExpenseRepository.summary_by_day(db, current_user.id)
    
        
    elif summary_type=="weekly":
        return ExpenseRepository.summary_by_week(db, current_user.id)
    
    elif summary_type=="monthly":
        return ExpenseRepository.summary_by_month(db, current_user.id)
    
    else:
       
        raise ValueError("Invalid summary type. Choose from 'daily', 'weekly', or 'monthly'.")
