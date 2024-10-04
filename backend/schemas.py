from pydantic import BaseModel

class TrainCreate(BaseModel):
    name: str
    cpu_size: str
    memory_size: str
    start_day: str
    end_day: str

class TrainedModel(BaseModel):
    id: int
    train_name: str
    name: str
    data_distribution: str
    trained_model_info: str
    class Config:
        orm_mode = True

class Train(TrainCreate):
    id: int
    created_at: str
    finished_at: str | None
    status: str
    class Config:
        orm_mode = True

class ServingModel(BaseModel):
    id: int
    trained_model_id: int
    hostname: str
    url: str