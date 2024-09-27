import pandas as pd
import numpy as np
import requests
from dateutil import parser
from datetime import datetime
import time

from trainer.load_data import DataLoader
from trainer.feature_engineering import FeatureEngineering
from trainer.preprocessing import Preprocessing

api_key="3I2HmlWkQhGNh5pVpOIRng"
start_day = "20240427"
end_day = "20240909"
# data_loader = DataLoader()
# df = data_loader.load_data(start_day, end_day)
df = pd.read_csv("temp_data.csv")
preprocessing = Preprocessing()
preprocessing.run(df)

feature = FeatureEngineering()
new_df = feature.run(df, preprocessing.data_dist)
