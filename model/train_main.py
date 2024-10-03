from trainer.load_data import DataLoader
from trainer.feature_engineering import FeatureEngineering
from trainer.preprocessing import Preprocessing
from trainer.predictor import Predictor
from trainer.train.trainer import Trainer

import pickle
import os
import argparse
import logging

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()

parser.add_argument("--start_day", default="20230427", type=str)
parser.add_argument("--end_day", default="20240427", type=str)

args = vars(parser.parse_known_args()[0])

target = "RN_mm"
api_key="3I2HmlWkQhGNh5pVpOIRng"

start_day = args["start_day"]
end_day = args["end_day"]

data_loader = DataLoader(api_key=api_key)
df = data_loader.load_data(start_day, end_day)
#df.to_csv("temp_data.csv", index=False)
preprocessing = Preprocessing()
df, data_dist = preprocessing.run(df)

feature = FeatureEngineering()
X, y = feature.run(df, data_dist, target=target)


trainer = Trainer()
trainer.train(X.to_numpy(), y.to_numpy(), col_names=X.columns, n_iter=1)

output_path = ""
predictor = Predictor(data_dist, target, trainer.best_model)
pkl_file = open(os.path.join(output_path, "predictor.pkl"), "wb")
pickle.dump(predictor, pkl_file)

