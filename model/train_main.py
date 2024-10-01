import pickle
import os

from trainer.load_data import DataLoader
from trainer.feature_engineering import FeatureEngineering
from trainer.preprocessing import Preprocessing
from trainer.predictor import Predictor

import pandas as pd
import shap
target = "RN_mm"

###################data##############################
api_key="3I2HmlWkQhGNh5pVpOIRng"
start_day = "20210101"
end_day = "20240909"
data_loader = DataLoader(api_key=api_key)
df = data_loader.load_data(start_day, end_day)
df.to_csv("temp_data.csv", index=False)

#################train####################################3
df = pd.read_csv("temp_data.csv")
preprocessing = Preprocessing()
df, data_dist = preprocessing.run(df)


feature = FeatureEngineering()
X, y = feature.run(df, data_dist, target=target)

from trainer.train.trainer import Trainer


import logging

# Set logging level to INFO
logging.basicConfig(level=logging.INFO)
trainer = Trainer()
trainer.train(X.to_numpy(), y.to_numpy(), col_names=X.columns, n_iter=1)

output_path = ""
predictor = Predictor(data_dist, target, trainer.best_model)
pkl_file = open(os.path.join(output_path, "predictor.pkl"), "wb")
pickle.dump(predictor, pkl_file)
