from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from . import models, schemas, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Expense & Budget Management App")

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(username=user.username, salary=user.salary)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/expenses/", response_model=schemas.ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == expense.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db_expense = models.Expense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@app.get("/expenses/{user_id}", response_model=list[schemas.ExpenseResponse])
def list_expenses(user_id: int, category: str = None, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    query = db.query(models.Expense).filter(models.Expense.user_id == user_id)
    if category:
        query = query.filter(models.Expense.category == category)
    return query.all()

@app.get("/totals/{user_id}", response_model=schemas.TotalsResponse)
def get_totals(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

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
