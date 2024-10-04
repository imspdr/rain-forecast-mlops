from venv import create

from fastapi import Depends, FastAPI, HTTPException, File, UploadFile

from .services import *
from .schemas import *
from .db import SessionLocal, Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/train/")
async def create_train_api(train_create: TrainCreate, db: Session = Depends(get_db)):
    db_train_named = get_train_by_name(db, train_create.name)
    if db_train_named:
        raise HTTPException(status_code=400, detail="Train name already exists")
    db_train = create_train(db, train_create)
    return db_train

@app.get("/train/all/")
def get_train_all_api(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return get_train_all(db, skip, limit)

@app.post("/trained_model/")
async def create_trained_model_api(trained_model: TrainedModel, db: Session = Depends(get_db)):
    created_model = create_trained_model(db, trained_model)
    return created_model


@app.put("/trained_model/{id}/upload/")
async def upload_trained_model(id: int, trained_model_pkl:UploadFile ,db: Session = Depends(get_db)):
    trained_model = get_trained_model(db, id)
    if trained_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    trained_model.trained_model_pkl = await trained_model_pkl.read()
    db.commit()
    db.refresh(trained_model)
    return trained_model.id


@app.get("/trained_model/all/")
def get_trained_model_all_api(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return get_trained_model_all(db, skip, limit)