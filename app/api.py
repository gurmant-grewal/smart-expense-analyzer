from fastapi import FastAPI
from app.schemas import ExpenseRequest,RegRequest,LoginRequest
from app.services.auth_services import (
    registration as registration_service,
    login as login_service
)
from app.services.summary import get_summary
from app.services.expense_services import add_expense
from database_session import get_db
from sqlalchemy.orm import Session  
from fastapi import Depends
from app.services.expense_services import analyze_expense
from app.security.auth import get_current_user
from fastapi import HTTPException



app= FastAPI()

@app.get("/")
def home():
    return {
        "message": "Smart Expense Analyzer API",
        "docs": "/docs"
    }


@app.post("/expenses/analyze")
def analyze(request: ExpenseRequest):

    return analyze_expense(
        text=request.text,
        amount=request.amount
    )

@app.post("/expenses")
def save_expense(

    request: ExpenseRequest,

    db: Session = Depends(get_db),

   username: str = Depends(get_current_user)

):

    expense = add_expense(
        db=db,
        username=username,
        text=request.text,
        amount=request.amount,
        predicted_category=request.predicted_category,
        corrected_category=request.corrected_category
    )

    return {
        "message": "Expense added.",
        "expense_id": expense.id
    }



@app.get("/summary/{summary_type}")
def summary( db: Session = Depends(get_db),
            username: str = Depends(get_current_user),
            summary_type: str = ["daily", "weekly", "monthly"]
        ):
    try:
        summary_data = get_summary(db, summary_type, username)

        return {
        "summary_type":"daily",
        "data":summary_data
        }
    
    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    

@app.post("/register")
def registration(reg_request: RegRequest, db: Session = Depends(get_db)):
    try:
        return registration_service(
        username=reg_request.username,
        password=reg_request.password,
        db=db)
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))

    
@app.post("/login")
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    
    try:

        return login_service(
            username=login_request.username,
            password=login_request.password,
            db= db)
    
    except ValueError as e:

        if str(e) == "User not found.":

            raise HTTPException(

                status_code=404,
                detail=str(e)

            )

        elif str(e) == "Invalid password.":

            raise HTTPException(

                status_code=401,
                detail=str(e)

            )

        raise HTTPException(

            status_code=400,
            detail=str(e)

        )












