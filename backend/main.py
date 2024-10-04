from fastapi import Depends, FastAPI, HTTPException, UploadFile
from datetime import datetime
from sqlalchemy.orm import Session
from .schemas import *
from .models import *
from .db import SessionLocal, Base, engine
from .k8s_operations.create_train_pod import create_train_pod
import pytz

kst = pytz.timezone('Asia/Seoul')

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# train

@app.post("/train/")
async def create_train_api(train_create: TrainCreate, db: Session = Depends(get_db)):
    db_train_named = db.query(RainTrain).filter(RainTrain.name == train_create.name).first()
    if db_train_named:
        raise HTTPException(status_code=400, detail="Train name already exists")
    db_train = RainTrain(**train_create.dict(), created_at=datetime.now(kst))
    db.add(db_train)
    db.commit()
    db.refresh(db_train)
    create_train_pod(train_create.name, train_create.start_day, train_create.end_day, train_create.cpu_size, train_create.memory_size)
    return db_train

@app.get("/train/all/")
def get_train_all_api(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(RainTrain).offset(skip).limit(limit).all()


@app.delete("/train/{id}")
async def delete_train(id: int, db: Session = Depends(get_db)):
    train = db.query(RainTrain).filter(RainTrain.id == id).first()
    if train:
        db.delete(train)
        db.commit()
        return {"message": f"train {id} has been deleted."}
    else:
        raise HTTPException(status_code=404, detail="Item not found")



@app.put("/train/{name}/status/{status}")
async def update_status(name: str, status: str, db: Session = Depends(get_db)):
    train = db.query(RainTrain).filter(RainTrain.name == name).first()
    if train is None:
        raise HTTPException(status_code=404, detail="Train not found")
    train.status = status
    if status == "complete":
        train.finished_at = datetime.now(kst)
    db.commit()
    db.refresh(train)
    return train.status




# trained_model

@app.post("/trained_model/")
async def create_trained_model_api(trained_model: TrainedModel, db: Session = Depends(get_db)):
    db_trained_model = RainTrainedModel(
        train_name=trained_model.train_name,
        name=trained_model.name,
        trained_model_info=trained_model.trained_model_info,
        data_distribution=trained_model.data_distribution,
    )
    db.add(db_trained_model)
    db.commit()
    db.refresh(db_trained_model)
    return db_trained_model


@app.put("/trained_model/{id}/upload/")
async def upload_trained_model(id: int, trained_model_pkl: UploadFile, db: Session = Depends(get_db)):
    trained_model = db.query(RainTrainedModel).filter(RainTrainedModel.id == id).first()
    if trained_model is None:
        raise HTTPException(status_code=404, detail="Trained model not found")
    trained_model.trained_model_pkl = await trained_model_pkl.read()
    db.commit()
    db.refresh(trained_model)
    return trained_model.id


@app.get("/trained_model/all/")
def get_trained_model_all_api(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(RainTrainedModel).offset(skip).limit(limit).all()


@app.delete("/trained_model/{id}")
async def delete_trained_model(id: int, db: Session = Depends(get_db)):
    trained_model = db.query(RainTrainedModel).filter(RainTrainedModel.id == id).first()
    if trained_model:
        db.delete(trained_model)
        db.commit()
        return {"message": f"train {id} has been deleted."}
    else:
        raise HTTPException(status_code=404, detail="Item not found")