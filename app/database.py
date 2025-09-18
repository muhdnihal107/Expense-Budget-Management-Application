from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(DATABASE_URL,connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=True,autoflush=True,blind = engine)

Base = declarative_base()