class ModelRunner:
    def __init__(self, **conf):
        self.configuration = conf
        self.col_names = None
        self.model = None
        self.steps = []
        for key in conf:
            self.steps.append((key, conf[key]["step"](**conf[key]["params"])))

    def run(self, X, y, col_names):
        # run model_runner
        self.steps[-1][1].fit(X, y, col_names)
        y = self.steps[-1][1].predict(X)
        self.model = self.steps[-1][1]
        return X, y

    def inference(self, X):
        y = self.steps[-1][1].predict(X)
        return y

    def get_model(self):
        return self.model

    def get_col_names(self):
        return self.col_names

    def get_config(self):
        ret_dict = []
        for key in self.configuration:
            # ret_dict[key] = self.configuration[key]["params"]
            ret_dict.append({"name": key, "params": self.configuration[key]["params"]})
        return ret_dict
