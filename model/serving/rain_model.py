from typing import Dict
import logging

import kserve
import pickle
import os

from ..trainer.load_data import DataLoader
from ..trainer.feature_engineering import FeatureEngineering
from ..trainer.preprocessing import Preprocessing
from ..trainer.predictor import Predictor


class RainModel(kserve.Model):
    def __init__(self, name: str, model_dir: str):
        super().__init__(name)
        self.model_dir = model_dir
        self.predictor = None
        self.ready = False

    def load(self) -> bool:
        model_path = kserve.Storage.download(self.model_dir)
        for file in os.listdir(model_path):
            file_path = os.path.join(model_path, file)
            if os.path.isfile(file_path) and file_path.endswith("pkl"):
                with open(file_path, "rb") as f:
                    self.predictor = pickle.load(f)
                    self.ready = True
                    break
        return self.ready

    def predict(self, payload: Dict, headers: Dict[str, str] = None) -> Dict:
        given = payload["instances"]
        try:
            api_key = "3I2HmlWkQhGNh5pVpOIRng"
            start_day = given
            end_day = given
            data_loader = DataLoader(api_key=api_key)
            df = data_loader.load_data(start_day, end_day)
            input_dict, y_hat, y_proba, y_true, = self.predictor.predict(df)
            return {
                "predictions": {
                    "y_hat": y_hat,
                    "y_true": y_true,
                    "y_proba": y_proba,
                    "input": input_dict
                }
            }
        except Exception as e:
            raise Exception(f"Failed to predict : {e}")
