from pyexpat import features

import lightgbm as lgb
import numpy as np


class CustomLightGBMClassifier:
    def __init__(self, **kwargs):
        self.name = "LightGBMClassifier"
        self.model = lgb.LGBMClassifier(
            importance_type="gain",
            verbose=-1,
            class_weight="balanced",
            **kwargs
        )

    def fit(self, X, y, col_names):
        self.col_names = col_names
        self.model.fit(X, y)
        return self

    def predict(self, X):
        return self.model.predict(X)

    def feature_importance(self):
        fi_sum = np.sum(self.model.feature_importances_)
        return {"label": self.col_names, "value": self.model.feature_importances_ / fi_sum}
