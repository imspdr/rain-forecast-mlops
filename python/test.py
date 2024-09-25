import pandas as pd
import numpy as np
import requests
import trainer.load_data
from python.trainer.load_data import DataLoader
from dateutil import parser
from datetime import datetime
import time

data_loader = DataLoader(api_key="3I2HmlWkQhGNh5pVpOIRng")

start_day = "20240702"
end_day = "20240909"

print(data_loader.load_data(start_day, end_day))

