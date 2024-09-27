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

y = new_df[target]
X = new_df.drop(columns=[target])

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create LightGBM dataset for training
train_data = lgb.Dataset(X_train, label=y_train)

# Set parameters for LightGBM
params = {
    'objective': 'regression',
    'metric': 'rmse',
    'boosting_type': 'gbdt',
    'learning_rate': 0.1,
    'num_leaves': 31
}

# Train the model
lgb_regressor = lgb.train(params, train_data, num_boost_round=100)

# Predict on the test set
y_pred = lgb_regressor.predict(X_test)

print(y_test[:10])
print(y_pred[:10])
# Calculate and print Mean Squared Error
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse:.4f}")



