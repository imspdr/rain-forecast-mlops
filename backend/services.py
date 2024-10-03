from sqlalchemy.orm import Session

from . import models, schemas


# train CRUD

def create_train(db: Session, train_create: schemas.TrainCreate):
    pass

def get_train_by_id(db: Session, id: int):
    return db.query(models.Train).filter(models.Train.id == id).first()

def get_train_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Train).offset(skip).limit(limit).all()

def update_train_status(db: Session, id: int, status: str):
    pass

def update_train_finished_at(db: Session, id: int, finished_at: str):
    pass

def delete_train_by_ids(db: Session, ids: [int]):
    pass


# trained model CRD

def create_trained_model(db: Session, trained_model: schemas.TrainedModel):
    pass

def get_trained_model(db: Session, id: int):
    return db.query(models.TrainedModel).filter(models.TrainedModel.id == id).first()

def get_trained_model_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TrainedModel).offset(skip).limit(limit).all()

def delete_trained_model_by_ids(db: Session, ids: [int]):
    pass