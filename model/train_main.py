from trainer.load_data import DataLoader
from trainer.feature_engineering import FeatureEngineering
from trainer.preprocessing import Preprocessing
from trainer.predictor import Predictor
from trainer.train.trainer import Trainer

import pickle
import os
import argparse
import logging
import json
import numpy as np
import pandas as pd
import requests


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        else:
            return super(NpEncoder, self).default(obj)


logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()

parser.add_argument("--train_name", default="testing", type=str)
parser.add_argument("--url", default="http://127.0.0.1:8000", type=str)
parser.add_argument("--start_day", default="20230427", type=str)
parser.add_argument("--end_day", default="20240427", type=str)

args = vars(parser.parse_known_args()[0])

target = "RN_mm"
api_key="3I2HmlWkQhGNh5pVpOIRng"

start_day = args["start_day"]
end_day = args["end_day"]

train_name = args["train_name"]
url = args["url"]

logging.info(f"train start : {train_name}")
logging.info(f"start day : {start_day}, end day : {end_day}")
logging.info(f"given server url : {url}")

data_loader = DataLoader(api_key=api_key)
df = data_loader.load_data(start_day, end_day)
df.to_csv("temp_data.csv", index=False)

df = pd.read_csv("temp_data.csv")
preprocessing = Preprocessing()
df, data_dist = preprocessing.run(df)

feature = FeatureEngineering()
X, y = feature.run(df, data_dist, target=target)

trainer = Trainer()
trainer.train(X.to_numpy(), y.to_numpy(), col_names=list(X.columns), n_iter=10)

output_path = ""
predictor = Predictor(data_dist, target, trainer.best_model)
pkl_file_path = os.path.join(output_path, "predictor.pkl")
pkl_file = open(pkl_file_path, "wb")
pickle.dump(predictor, pkl_file)

str_dist_info = json.dumps(predictor.dist_info, cls=NpEncoder)
str_model_info = json.dumps(trainer.report(), cls=NpEncoder)

# trained_model 생성
create_url = url + "/trained_model/"

data = {
    "train_name": train_name,
    "name": predictor.model.model_name,
    "data_distribution": str_dist_info,
    "trained_model_info": str_model_info
}

response = requests.post(create_url, headers={"Content-Type": "application/json"}, data=json.dumps(data))

ret_id = response.json()["id"]

with open(pkl_file_path, "rb") as file:
    url2 = url + f"/trained_model/{ret_id}/upload"
    response = requests.put(url2, files={"trained_model_pkl": file})

logging.info(response.status_code)

