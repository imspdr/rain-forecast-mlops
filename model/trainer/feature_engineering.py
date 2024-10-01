import pandas as pd
from dateutil import parser
from datetime import datetime
import time

def timefeature_from_str(v, format):
    ts = time.mktime(parser.parse(str(v)).timetuple())
    return int(datetime.fromtimestamp(ts).strftime(format))

class FeatureEngineering:
    def __init__(self, one_hot_percentage_threshold=1):
        self.one_hot_percentage_threshold = one_hot_percentage_threshold
    def run(self, df, data_dist, target="RN_mm", train=True):
        for dist in data_dist:
            if "remove" in dist["col_type"]:
                df = df.drop(columns=[dist["col_name"]])
            elif dist["col_type"] == "categorical":
                col_name = dist["col_name"]
                one_hot_encoding = pd.DataFrame()
                for val in dist["distribution"]["value_percentage"]:
                    if val["value"] < self.one_hot_percentage_threshold:
                        continue
                    name = val["name"]
                    one_hot_encoding[col_name + "=" + name] = (df[col_name] == name).astype(int)
                df = pd.concat([df, one_hot_encoding], axis=1)
                df = df.drop(columns=[dist["col_name"]])

            elif dist["col_type"] == "datetime":
                time_col = df[dist["col_name"]]

                date_dict = {"year": "%Y", "month": "%m", "day": "%d", "hour": "%H"}
                datetime_features = pd.DataFrame()
                for time_feature, format in date_dict.items():
                    datetime_features[dist["col_name"] + "-" + time_feature] = time_col.apply(
                        lambda v: timefeature_from_str(v, format))
                df = pd.concat([df, datetime_features], axis=1)
                df = df.drop(columns=[dist["col_name"]])

        def labeling(val):
            try:
                if float(val) > 0:
                    return 1
                else:
                    return 0
            except(TypeError, ValueError):
                return -1
        df["label"] = df[target].shift(-1).apply(labeling)
        if train:
            df = df.drop(df.index[-1])

        y = df["label"]
        X = df.drop(columns=["label"])

        return X, y