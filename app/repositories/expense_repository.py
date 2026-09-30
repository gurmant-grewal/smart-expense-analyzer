from sqlalchemy.orm import Session
from app.models import Expense
from sqlalchemy import func, extract
from datetime import datetime, timedelta


class ExpenseRepository:
   
    @staticmethod
    def get_expense_by_user(db: Session, user_id: int):
        return db.query(Expense).filter(Expense.user_id == user_id).all()

    @staticmethod
    def create_expense(db: Session, expense: Expense):
        db.add(expense)
        db.commit()
        db.refresh(expense)
        return expense
    
    @staticmethod
    def verify_expense_count(db: Session):
        return db.query(Expense).filter(Expense.feedback_verified == True).count()
    
    @staticmethod
    def get_verified_expenses(db: Session):
        return db.query(Expense).filter(Expense.feedback_verified == True).all()
    
    @staticmethod
    def get_users_merchant_data(db: Session, user_id: int):
        return  db.query(
                Expense.merchant,
                func.sum(Expense.amount)
            ).filter(
                Expense.user_id == user_id,
                Expense.merchant != None
            ).group_by(Expense.merchant).all()
    
    @staticmethod
    def summary_by_month(db: Session, user_id: int):
        start= datetime.now()-timedelta(days=30)
        return db.query(
            Expense.category,
            func.sum(Expense.amount)).filter(
            extract("year", Expense.date) >= start.year,
            extract("month", Expense.date) >= start.month,
            Expense.user_id == user_id
        ).group_by(Expense.category).all()


    @staticmethod
    def summary_by_week(db: Session, user_id: int):
        start= datetime.now()-timedelta(days=7)
        return db.query(
            Expense.category,
            func.sum(Expense.amount)).filter(
                Expense.date>=start,
                Expense.user_id == user_id
        ).group_by(Expense.category).all()
    
    @staticmethod
    def summary_by_day(db: Session, user_id: int):
        today= datetime.now().date()
        return db.query(
            Expense.category,
            func.sum(Expense.amount)).filter(
                Expense.date==today,
                Expense.user_id == user_id
        ).group_by(Expense.category).all()
            