from .feature_engineering import FeatureEngineering

class Predictor:
    def __init__(self, dist_info, target, model):
        self.dist_info = dist_info
        self.target = target
        self.model = model

    def predict(self, df):
        X, y = FeatureEngineering().run(df, self.dist_info, self.target, train=False)
        return self.model.inference(X.to_numpy()), y

