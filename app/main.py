from fastapi import FastAPI,status,Depends
from . import models,schemas
from .database import sessionmaker,engine,SessionLocal,Base
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/users/',status_code=status.HTTP_201_CREATED)
def create_user(db:Session = Depends((get_db))):
    pass