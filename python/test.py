import pandas as pd
import numpy as np
import requests
import trainer.load_data
from python.trainer.load_data import DataLoader
from dateutil import parser
from datetime import datetime
import time

data_loader = DataLoader(api_key="3I2HmlWkQhGNh5pVpOIRng")

start_day = "20240902"
end_day = "20240909"

print(data_loader.load_data(start_day, end_day))

def cat_percent(col, unique_val):
    percent_dict = {}
    for v in unique_val:
        total_count = len(col)
        count = 0.0
        for x in col:
            if str(v) == str(x):
                count += 1
        percent_dict[str(v)] = round(count / total_count * 100, 4)
    return percent_dict


# count percentage for categorical data
def one_hot_percent(x):
    total_count = 0.0
    one_count = 0.0
    for v in x:
        if v == 1:
            one_count += 1
        total_count += 1
    return round(one_count / total_count * 100, 4)


# calculate mean, min, max of column containing nan
def nan_mean_min_max(col):
    total_sum = 0
    total_num = 0
    now_min = np.inf
    now_max = -np.inf
    for v in col:
        v = float(v)
        if not is_nan(v):
            total_sum += v
            total_num += 1
            if v < now_min:
                now_min = v
            if v > now_max:
                now_max = v

    return (
        round(total_sum / (total_num if total_num > 0 else 1), 4),
        round(now_min, 4),
        round(now_max, 4),
    )


# determine the value is number or not
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
