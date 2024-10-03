from fastapi import Depends, FastAPI, HTTPException, File, UploadFile
from sqlalchemy.orm import Session

from services import *
from schemas import *
from db import SessionLocal

app = FastAPI()

url = "http://127.0.0.1:8000/"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/train/")
async def create_train_api(train_create: TrainCreate, db: Session = Depends(get_db)):
    db_train = get_train_by_name(db, train_create.name)
    if db_train:
        raise HTTPException(status_code=400, detail="Train name already exists")
    return {"message": "train created"}

@app.get("/train/all/")
def get_train_all_api(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return get_train_all(db, skip, limit)

@app.post("/trained_model/")
async def create_trained_model_api(
    train_name: str,
    name: str,
    data_distribution: str,
    model_info: str,
    model_pkl: UploadFile = File(...),
    db: Session = Depends(get_db)):

    model_pkl_data = model_pkl.file.read()

    trained_model = TrainedModel(
        train_name=train_name,
        name=name,
        data_distribution=data_distribution,
        model_info=model_info,
    )
    create_trained_model(db, trained_model, model_pkl_data)

    return {"message": "trained model created"}

@app.get("/trained_model/all/")
def get_trained_model_all_api(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return get_trained_model_all(db, skip, limit)