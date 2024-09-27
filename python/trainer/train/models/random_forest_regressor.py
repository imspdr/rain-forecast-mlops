from sklearn.ensemble import RandomForestRegressor


class CustomRandomForestRegressor:
    def __init__(self, **kwargs):
        self.n_estimators = kwargs["n_estimators"]
        self.max_features = kwargs["max_features"]
        self.name = "RandomForestRegressor"
        self.model = RandomForestRegressor(n_estimators=self.n_estimators, max_features=self.max_features)
        self.col_names = None

    def fit(self, X, y, col_names):
        self.col_names = col_names
        self.model.fit(X, y)
        return self

    def predict(self, X):
        return self.model.predict(X)

    def feature_importance(self):
        return {"value": self.model.feature_importances_, "label": self.col_names}
