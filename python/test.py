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
# {
#     "max_depth": {"type": 1, "min": 16, "max": 50},
#     "learning_rate": {"type": 2, "min": 0.03, "max": 0.3},
#     "n_estimators": {"type": 1, "min": 50, "max": 200},
# },

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

y = new_df["label"]
X = new_df.drop(columns=["label"])

count = 0
for v in y:
    if v == 1: count+=1

print(len(y))
print(count)



