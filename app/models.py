from sqlalchemy import String,Integer,Column,Float,ForeignKey,Enum,DateTime
from .database import Base
from datetime import datetime,timezone

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,unique=True,nullable=False)
    salary = Column(Float,default=0.0)


class Expense_Category(str,Enum):
    FOOD = "Food"
    TRANSPORT = "Transport"
    ENTERTAINMENT = "Entertainment"
    UTILITIES = "Utilities"
    OOTHER = "Other"

class Expense(Base):
    __tablename__ = 'expences'
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(ForeignKey('users.id'),)
    name = Column(String,nullable=False)
    amount = Column(Float)
    category = Column(Enum(Expense_Category),nullable=False)
    created_at=Column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc))


