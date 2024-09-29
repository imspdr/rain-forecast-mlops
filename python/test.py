import pandas as pd
import lightgbm as lgb

from trainer.load_data import DataLoader
from trainer.feature_engineering import FeatureEngineering
from trainer.preprocessing import Preprocessing

# api_key="3I2HmlWkQhGNh5pVpOIRng"
# start_day = "20240427"
# end_day = "20240909"
# data_loader = DataLoader(api_key=api_key)
# df = data_loader.load_data(start_day, end_day)
df = pd.read_csv("temp_data.csv")
#
preprocessing = Preprocessing()
df, data_dist = preprocessing.run(df)

target = "RN_mm"
feature = FeatureEngineering(target=target)
new_df = feature.run(df, data_dist)

from trainer.train.trainer import Trainer

y = new_df["label"]
X = new_df.drop(columns=["label"])

import logging

# Set logging level to INFO
logging.basicConfig(level=logging.INFO)
trainer = Trainer()
trainer.train(X.to_numpy(), y.to_numpy(), col_names=X.columns)

print(trainer.report())



