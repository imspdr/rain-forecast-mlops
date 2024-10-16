from fastapi import Depends, FastAPI, HTTPException, UploadFile, File, Response
from datetime import datetime
from sqlalchemy.orm import Session
from infra.schemas import *
from infra.models import *
from infra.db import *
from infra.k8s_operations import *
from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException
import pytz

kst = pytz.timezone('Asia/Seoul')

Base.metadata.create_all(bind=engine)

try:
    config.load_incluster_config()
except ConfigException as e:
    print(f"Failed to load kube-config: {e}")

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
    create_train_pod(train_create.name, train_create.start_day, train_create.end_day)
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
async def upload_trained_model(id: int, trained_model_pkl: UploadFile = File(...), db: Session = Depends(get_db)):
    trained_model = db.query(RainTrainedModel).filter(RainTrainedModel.id == id).first()
    if trained_model is None:
        raise HTTPException(status_code=404, detail="Trained model not found")
    trained_model.trained_model_pkl = await trained_model_pkl.read()

    db.commit()
    db.refresh(trained_model)
    return trained_model.id


@app.get("/trained_model/all/")
def get_trained_model_all_api(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    all_trained_model = db.query(RainTrainedModel).offset(skip).limit(limit).all()
    return list(map(lambda tm: {
        "id": tm.id,
        "train_name": tm.train_name,
        "name": tm.name,
        "deployed": tm.deployed
    }, all_trained_model))

@app.get("/trained_model/all/deployed")
def get_trained_model_all_deployed(db: Session = Depends(get_db)):
    all_trained_model = db.query(RainTrainedModel).filter(RainTrainedModel.deployed == "true").all()
    return list(map(lambda tm: {
        "id": tm.id,
        "train_name": tm.train_name,
        "name": tm.name,
        "deployed": tm.deployed
    }, all_trained_model))

@app.get("/trained_model/{train_name}")
def get_trained_model_by_train_name(train_name: str, db: Session = Depends(get_db)):
    tm = db.query(RainTrainedModel).filter(RainTrainedModel.train_name == train_name).first()
    if tm:
        return {
            "id": tm.id,
            "train_name": tm.train_name,
            "name": tm.name,
            "data_distribution": tm.data_distribution,
            "trained_model_info": tm.trained_model_info,
            "deployed": tm.deployed
        }
    else:
        raise HTTPException(status_code=404, detail="Model not found")

@app.delete("/trained_model/{id}")
async def delete_trained_model(id: int, db: Session = Depends(get_db)):
    trained_model = db.query(RainTrainedModel).filter(RainTrainedModel.id == id).first()
    if trained_model:
        db.delete(trained_model)
        db.commit()
        return {"message": f"trained_model {id} has been deleted."}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/trained_model/name/{train_name}")
async def delete_trained_model_by_train_name(train_name: str, db: Session = Depends(get_db)):
    trained_model = db.query(RainTrainedModel).filter(RainTrainedModel.train_name == train_name).first()
    if trained_model:
        db.delete(trained_model)
        db.commit()
        try:
            delete_trained_model_crd(trained_model.train_name)
        except Exception as e:
            pass
        return {"message": f"trained_model named {train_name} has been deleted."}
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get("/trained_model/download/{id}/predictor.pkl")
async def download_file(id: int, db: Session = Depends(get_db)):
    trained_model = db.query(RainTrainedModel).filter(RainTrainedModel.id == id).first()
    if trained_model and trained_model.trained_model_pkl:
        content = trained_model.trained_model_pkl
        filename = "predictor.pkl"
        headers = {
                   "Content-Disposition": f"attachment; filename={filename}"
                   }
        return Response(content, headers=headers, media_type="application/octet-stream")
    else:
        raise HTTPException(status_code=404, detail="Model not found or no pkl file available")

@app.put("/trained_model/deploy/{id}")
async def deploy_trained_model(id: int, db: Session = Depends(get_db)):
    num_deployed = len(db.query(RainTrainedModel).filter(RainTrainedModel.deployed == "true").all())
    if num_deployed > 9:
        raise HTTPException(status_code=400, detail="Resource Not Enough")
    trained_model = db.query(RainTrainedModel).filter(RainTrainedModel.id == id).first()
    if trained_model:
        try:
            create_trained_model_crd(trained_model.train_name, BACKEND_URL + f"/trained_model/download/{id}/predictor.pkl")

            trained_model.deployed = "true"
            db.commit()
            db.refresh(trained_model)
        except Exception as e:
            return e
        return trained_model.train_name
    else:
        raise HTTPException(status_code=404, detail="Model not found")

@app.put("/trained_model/undeploy/{id}")
async def undeploy_trained_model(id: int, db: Session = Depends(get_db)):
    trained_model = db.query(RainTrainedModel).filter(RainTrainedModel.id == id).first()
    if trained_model:
        try:
            trained_model.deployed = "false"
            db.commit()
            db.refresh(trained_model)
            delete_trained_model_crd(trained_model.train_name)
        except Exception as e:
            return e
        return trained_model.train_name
    else:
        raise HTTPException(status_code=404, detail="Model not found")