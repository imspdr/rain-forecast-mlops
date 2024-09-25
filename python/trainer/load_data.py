import pandas as pd
import requests
from dateutil import parser
from datetime import datetime
import time

class DataLoader:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://apihub.kma.go.kr/api/typ01/url/kma_sfctm3.php"
    def get_columns(self):
        # 고정된 날짜 호출하여 칼럼 정보만 추출

        params = {
            "tm1": "202409250000",
            "tm2": "202409250300",
            "stn": "119",
            "authKey": self.api_key
        }
        response = requests.get(self.url, params=params)
        columns = []
        if response.status_code == 200:
            for i, res in enumerate(response.text.split("\n")):
                if len(res) > 0:
                    if res[0] == "#":
                        if len(res) > 1 and res[1] == " ":
                            # 칼럼명 처리
                            cols = res.split()[1:]
                            if len(columns) > 0:
                                for i, col in enumerate(cols):
                                    columns[i] += (("_" + col) if not "-" in col else "")
                            else:
                                for i, col in enumerate(cols):
                                    columns.append(col)
                            continue
                        else:
                            continue
                if i > 5:
                    break
        return columns

    def load_data_using_api(self, start_ts, end_ts):
        start_day = datetime.fromtimestamp(start_ts).strftime('%Y%m%d')
        end_day = datetime.fromtimestamp(end_ts).strftime('%Y%m%d')
        params = {
            "tm1": start_day + "0000",
            "tm2": end_day + "2300",
            "stn": "119",
            "authKey": self.api_key
        }
        response = requests.get(self.url, params=params)

        day_data = []
        if response.status_code == 200:
            for i, res in enumerate(response.text.split("\n")):
                if len(res) > 0:
                    if res[0] == "#":
                        continue
                    day_data.append(res.split())
        return day_data

    def load_data(self, start_day, end_day):
        # api 최대 길이가 한달 분량의 데이터이므로 20일씩 끊어서 로드
        start = time.mktime(parser.parse(start_day).timetuple())
        end = time.mktime(parser.parse(end_day).timetuple())
        DAY = 3600 * 24
        day_len = (end - start) / 3600 / 24
        num_loop = int(day_len // 20 + 1)

        total_data = []
        now_start = start
        for i in range(num_loop):
            now_end = now_start + DAY * 20
            if now_end < end:
                data_list = self.load_data_using_api(now_start, now_end)
                now_start = now_end
            else:
                data_list = self.load_data_using_api(now_start, end)
                now_start = end
            for data in data_list:
                total_data.append(data)
        col_names = self.get_columns()
        ret = pd.DataFrame(total_data)
        ret.columns = col_names
        return ret
