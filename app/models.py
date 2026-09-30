from sqlalchemy import Integer,Float,Column,String,Boolean,DateTime
from database import Base
from sqlalchemy import ForeignKey
from datetime import datetime 
from sqlalchemy.orm import relationship

class Expense(Base):
    __tablename__ = "expenses"
    id= Column(Integer, primary_key=True, index=True)
    user_id= Column(Integer,ForeignKey("users.id"),nullable=False)
    date= Column(DateTime, nullable=False, default=datetime.now)
    text= Column(String, nullable=False)
    category= Column(String, nullable=False)
    amount= Column(Float, nullable=False)
    feedback_verified=Column(Boolean,default=False)
    merchant = Column(String, nullable=True)
    user=relationship(
        "User",
        back_populates="expenses"
    )

class User(Base):
    __tablename__ = "users"
    id= Column(Integer, primary_key=True, index=True)
    username= Column(String,unique=True, index=True)
    password= Column(String)
    expenses= relationship(
        "Expense",
        back_populates="user",
        cascade="all, delete-orphan"
    )