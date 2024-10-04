import numpy as np

class Preprocessing:
    def __init__(self):
        self.data_dist = []

        self.UNIQUE_THRESHOLD = 5
        self.REMOVE_CATEGORICAL_THRESHOLD = 100

    def run(self, df):
        for col_name in df.columns:
            col = df[col_name]
            if col_name == "YYMMDDHHMI_KST":
                col_type = "datetime"
                self.data_dist.append({
                    "col_name": col_name,
                    "col_type": col_type,
                    "distribution": []
                })
                continue
            col_dtype = col.dtype
            if col_dtype in ["int64", "float64"]:
                col_type = "numeric"
            else:
                col_type = "categorical"

            unique_values = col.unique()
            if len(unique_values) == 1:
                col_type = "remove(only one value)"
            elif len(unique_values) < self.UNIQUE_THRESHOLD:
                col_type = "categorical"
            elif len(unique_values) > self.REMOVE_CATEGORICAL_THRESHOLD and col_type == "categorical":
                col_type = "remove(too sparse data)"


            if col_type == "numeric":

                # minmax, mean, histogram
                min = col.min()
                max = col.max()
                mean = col.mean()

                counts, bin_edges = np.histogram(col, bins=12)
                distribution_data = {
                    "minmax": {
                        "min": min,
                        "max": max,
                        "mean": mean
                    },
                    "histogram": {
                        "counts": counts,
                        "bins": list(map(lambda num: num.round(4), bin_edges))
                    }
                }
            elif col_type == "categorical":
                value_percentage = col.value_counts(normalize=True).round(4) * 100

                value_percentage_json = value_percentage.to_dict()
                distribution_data = {
                    "value_percentage": []
                }
                for k, v in value_percentage_json.items():
                    distribution_data["value_percentage"].append({
                        "name": str(k),
                        "value": v
                    })
            else:
                distribution_data = []

            self.data_dist.append({
                "col_name": col_name,
                "col_type": col_type,
                "distribution": distribution_data
            })
        return df, self.data_dist

