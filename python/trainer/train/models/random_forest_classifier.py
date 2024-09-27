from sklearn.ensemble import RandomForestClassifier


class CustomRandomForestClassifier:
    def __init__(self, **kwargs):
        self.n_estimators = kwargs["n_estimators"]
        self.max_features = kwargs["max_features"]
        self.name = "RandomForestClassifier"
        self.model = RandomForestClassifier(n_estimators=self.n_estimators, max_features=self.max_features)
        self.col_names = None

    def fit(self, X, y, col_names):
        self.model.fit(X, y)
        self.col_names = col_names
        return self

    def predict(self, X):
        return self.model.predict(X)

    def feature_importance(self):
        return {"value": self.model.feature_importances_, "label": self.col_names}
