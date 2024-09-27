import lightgbm as lgb
import numpy as np


class CustomLightGBMClassifier:
    def __init__(self, **kwargs):
        self.learning_rate = kwargs["learning_rate"]
        self.n_estimators = kwargs["n_estimators"]
        self.max_depth = kwargs["max_depth"]
        self.name = "LightGBMClassifier"
        self.model = lgb.LGBMClassifier(
            n_estimators=self.n_estimators,
            learning_rate=self.learning_rate,
            max_depth=self.max_depth,
            importance_type="gain",
            verbose=-1,
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
