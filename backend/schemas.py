from pydantic import BaseModel

class TrainCreate(BaseModel):
    name: str
    cpu_size: str
    memory_size: str
    start_day: str
    end_day: str

class Train(TrainCreate):
    id: int
    created_at: str
    finished_at: str | None
    status: str

    class Config:
        orm_mode = True

class TrainedModel(BaseModel):
    id: int
    train_id: int
    name: str
    data_distribution: str
    model_info: str
    model_pkl: object
    class Config:
        orm_mode = True

class CreateServingModel(BaseModel):
    train_id: str