from pydantic import BaseModel,Field

class ExpenseRequest(BaseModel):
    
    text: str=Field(min_length=4,max_length=300)
    amount: float=Field(gt=0,le=10000000)
    date: str
    predicted_category: str
    corrected_category: str | None = None

class RegRequest(BaseModel):
    username: str=Field(min_length=3,max_length=30)
    password: str=Field(min_length=7,max_length=150)
    
class LoginRequest(BaseModel):
    username: str=Field(min_length=3,max_length=30)
    password: str=Field(min_length=7,max_length=150)

class SummaryRequest(BaseModel):
    summary_type: str