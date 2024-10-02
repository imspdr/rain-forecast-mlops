from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import  models, schemas
from .db import SessionLocal, engine

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "MySQL DDL script executed!"}
