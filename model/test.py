import pickle
import os
import json

from trainer.load_data import DataLoader
from trainer.feature_engineering import FeatureEngineering
from trainer.preprocessing import Preprocessing
from trainer.predictor import Predictor

import numpy as np
target = "RN_mm"

###################data##############################
# api_key="3I2HmlWkQhGNh5pVpOIRng"
# start_day = "20210101"
# end_day = "20240909"
# data_loader = DataLoader(api_key=api_key)
# df = data_loader.load_data(start_day, end_day)
# df.to_csv("temp_data.csv", index=False)

##################train####################################3
# df = pd.read_csv("temp_data.csv")
# preprocessing = Preprocessing()
# df, data_dist = preprocessing.run(df)
#
#
# feature = FeatureEngineering()
# X, y = feature.run(df, data_dist, target=target)
#
# from trainer.train.trainer import Trainer
#
#
# import logging
#
# # Set logging level to INFO
# logging.basicConfig(level=logging.INFO)
# trainer = Trainer()
# trainer.train(X.to_numpy(), y.to_numpy(), col_names=X.columns, n_iter=1)
#
# output_path = ""
# predictor = Predictor(data_dist, target, trainer.best_model)
# pkl_file = open(os.path.join(output_path, "predictor.pkl"), "wb")
# pickle.dump(predictor, pkl_file)

###################serving##############################


pkl_file = open("predictor.pkl", "rb")
predictor = pickle.load(pkl_file)

api_key="3I2HmlWkQhGNh5pVpOIRng"
start_day = "20240912"
end_day = "20240912"
data_loader = DataLoader(api_key=api_key)
df = data_loader.load_data(start_day, end_day)
print(predictor.predict(df))

# print(predictor.model.get_config())
#
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
# print(predictor.model.model_name)
# test_dist = json.dumps(predictor.dist_info, cls=NpEncoder)
# print(type(test_dist))
# fi = predictor.model.get_model().feature_importance()
# for i, name in enumerate(fi["label"]):
#     print(name)
#     print(fi["value"][i])

################3 SHAP #############################
# processed_data = FeatureEngineering().run(df, predictor.dist_info, predictor.target, train=False)[0]
# explainer = shap.TreeExplainer(predictor.model.get_model().model, feature_names=processed_data.columns)
# shap_values = explainer(processed_data.to_numpy())
# import matplotlib
# shap_line = shap_values[15]
# if predictor.model.model_name == "RandomForestClassifier":
#     shap_line.values = shap_line.values[:, 1]
#     shap_line.base_values = shap_line.base_values[1]
# # print(shap_line)
# shap.plots.waterfall(shap_line)

