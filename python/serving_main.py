import kserve
from serving.model_repository import ModelRepository

kserve.ModelServer(registered_models=ModelRepository()).start([])
