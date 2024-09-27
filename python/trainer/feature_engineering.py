import pandas as pd
from dateutil import parser
from datetime import datetime
import time

def timefeature_from_str(v, format):
    ts = time.mktime(parser.parse(str(v)).timetuple())
    return int(datetime.fromtimestamp(ts).strftime(format))

class FeatureEngineering:
    def __init__(self, one_hot_percentage_threshold=1, target="RN_mm"):
        self.one_hot_percentage_threshold = one_hot_percentage_threshold
        self.target = target
    def run(self, df, data_dist):
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

            elif dist["col_type"] == "datetime":
                time_col = df[dist["col_name"]]

                date_dict = {"year": "%Y", "month": "%m", "day": "%d", "hour": "%H"}
                datetime_features = pd.DataFrame()
                for time_feature, format in date_dict.items():
                    datetime_features[dist["col_name"] + "-" + time_feature] = time_col.apply(
                        lambda v: timefeature_from_str(v, format))

                df = pd.concat([df, datetime_features], axis=1)
            elif dist["col_type"] == "numeric":
                col_name = dist["col_name"]
                df[col_name] = df[col_name].replace(-9, 0)

        df["label"] = df[self.target].shift(-1)
        df = df.drop(df.index[-1])
        return df