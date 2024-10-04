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
async def create_trained_model_api(
    train_name: str,
    name: str,
    data_distribution: str,
    trained_model_info: str,
    trained_model_pkl: UploadFile = File(...),
    db: Session = Depends(get_db)):

    trained_model_pkl_data = trained_model_pkl.file.read()

    trained_model = TrainedModel(
        train_name=train_name,
        name=name,
        data_distribution=data_distribution,
        trained_model_info=trained_model_info,
    )
    create_trained_model(db, trained_model, trained_model_pkl_data)

    return {"message": "trained model created"}

@app.get("/trained_model/all/")
def get_trained_model_all_api(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return get_trained_model_all(db, skip, limit)