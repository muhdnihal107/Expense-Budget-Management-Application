from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, salary=user.salary)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def create_expense(db: Session, expense: schemas.ExpenseCreate):
    db_expense = models.Expense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def get_expenses(db: Session, user_id: int, category: str = None):
    query = db.query(models.Expense).filter(models.Expense.user_id == user_id)
    if category:
        query = query.filter(models.Expense.category == category)
    return query.all()

def get_totals(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        return None

    total_expense = db.query(func.sum(models.Expense.amount))\
                      .filter(models.Expense.user_id == user_id).scalar() or 0

    category_data = db.query(models.Expense.category, func.sum(models.Expense.amount))\
                      .filter(models.Expense.user_id == user_id)\
                      .group_by(models.Expense.category).all()

    category_breakdown = {cat: amt for cat, amt in category_data}

    return {
        "total_expense": total_expense,
        "total_salary": user.salary,
        "remaining_amount": user.salary - total_expense,
        "category_breakdown": category_breakdown
    }
