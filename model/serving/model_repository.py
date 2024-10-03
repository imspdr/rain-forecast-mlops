from kserve.model_repository import ModelRepository, MODEL_MOUNT_DIRS
from .rain_model import RainModel

import logging
import os


class ModelRepository(ModelRepository):
    def __init__(selfself, model_dir: str=MODEL_MOUNT_DIRS):
        super().__init__(model_dir)
        logging.basicConfig(level=logging.INFO)

    async def load(self, name: str) -> bool:
        logging.info(f"name: {name}, model_dir: {self.models_dir}")

        for root, dirs, files in os.walk(os.path.join(self.models_dir, name)):
            for file in files:
                logging.info(f"filename: {file}")
                if file.endswith(".pkl"):
                    model = RainModel(name=name, model_dir=root)
        if model.load():
            self.update(model)
        return model.ready