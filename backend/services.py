from sqlalchemy.orm import Session
from .models import *
from .schemas import *
from .k8s_operations.create_train_pod import create_train_pod


# train CRUD

def create_train(db: Session, train_create: TrainCreate):
    db_train = RainTrain(
        name=train_create.name,
        cpu_size=train_create.cpu_size,
        memory_size=train_create.memory_size,
        start_day=train_create.start_day,
        end_day=train_create.end_day,
    )
    db.add(db_train)
    db.commit()
    db.refresh(db_train)
    create_train_pod(train_create.name, train_create.start_day, train_create.end_day)
    return db_train

def get_train_by_name(db: Session, name: str):
    return db.query(RainTrain).filter(RainTrain.name == name).first()

def get_train_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(RainTrain).offset(skip).limit(limit).all()

def update_train_status(db: Session, id: int, status: str):
    pass

def update_train_finished_at(db: Session, id: int, finished_at: str):
    pass

def delete_train_by_ids(db: Session, ids: [int]):
    pass


# trained model CRD

def create_trained_model(db: Session, trained_model: TrainedModel, model_pkl: any):
    db_trained_model = RainTrainedModel(
        train_name=trained_model.train_name,
        name=trained_model.name,
        model_info=trained_model.model_info,
        model_pkl=model_pkl,
        data_distribution=trained_model.data_distribution
    )
    db.add(db_trained_model)
    db.commit()
    db.refresh(db_trained_model)
    return db_trained_model

def get_trained_model(db: Session, id: int):
    return db.query(RainTrainedModel).filter(RainTrainedModel.id == id).first()

def get_trained_model_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(RainTrainedModel).offset(skip).limit(limit).all()

def delete_trained_model_by_ids(db: Session, ids: [int]):
    pass