from pydantic import BaseModel,Field
from typing import Optional
from .models import Expense_Category
from datetime import datetime



class UserBase(BaseModel):
    username: str
    salary: Optional[float] = 0.0

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    user_id: int
    class Config:
        orm_mode = True



class ExpenseBase(BaseModel):
    name: str
    amount: float = Field(gt=0, description="Amount must be greater than 0")
    category: Expense_Category

class ExpenseCreate(ExpenseBase):
    user_id: int

class ExpenseResponse(ExpenseBase):
    expense_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class TotalsResponse(BaseModel):
    total_expense: float
    total_salary: float
    remaining_amount: float
    category_breakdown: dict