from sqlalchemy import String,Integer,Column,Float,ForeignKey,Enum,DateTime,func
from .database import Base
from datetime import datetime,timezone
from sqlalchemy.orm import relationship



class Expense_Category(str,Enum):
    FOOD = "Food"
    TRANSPORT = "Transport"
    ENTERTAINMENT = "Entertainment"
    UTILITIES = "Utilities"
    OOTHER = "Other"
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    salary = Column(Float, default=0.0)

    expenses = relationship("Expense", back_populates="user")

class Expense(Base):
    __tablename__ = "expenses"

    expense_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(Enum(Expense_Category), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="expenses")


