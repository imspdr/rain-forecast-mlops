from sklearn.ensemble import RandomForestClassifier


class CustomRandomForestClassifier:
    def __init__(self, **kwargs):
        self.name = "RandomForestClassifier"
        self.model = RandomForestClassifier(
            class_weight = 'balanced', **kwargs)
        self.col_names = None

    def fit(self, X, y, col_names):
        self.model.fit(X, y)
        self.col_names = col_names
        return self

    def predict(self, X):
        return self.model.predict(X)

    def feature_importance(self):
        return {"value": self.model.feature_importances_, "label": self.col_names}
