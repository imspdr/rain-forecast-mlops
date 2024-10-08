from .feature_engineering import FeatureEngineering

class Predictor:
    def __init__(self, dist_info, target, model):
        self.dist_info = dist_info
        self.target = target
        self.model = model

    def predict(self, df):
        X, y = FeatureEngineering().run(df, self.dist_info, self.target, train=False)
        proba = list(map(lambda arr: arr[1].round(4),self.model.inference_proba(X.to_numpy())))
        return list(self.model.inference(X.to_numpy())), proba, list(y.to_numpy())

