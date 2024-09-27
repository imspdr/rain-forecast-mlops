import logging
import threading
import numpy as np
import hpbandster.core.nameserver as hpns
from hpbandster.optimizers import BOHB
from hpbandster.core.worker import Worker
from .config_parser import ConfigParser
from .model_runner import ModelRunner
from sklearn.model_selection import train_test_split


class Recorder:
    def __init__(self):
        self.lock = threading.Lock()
        self.best_loss = np.inf
        self.best_config = None

    def update(self, loss, config):
        self.lock.acquire()
        logging.info("loss : %s" % str(loss))
        logging.info("config : %s" % str(config))
        if self.best_loss > loss:
            self.best_loss = loss
            self.best_config = config
        self.lock.release()


class MyWorker(Worker):
    """
    worker object for BOHB module
    BOHB module calls worker to run 'compute' method using given config
    and 'compute' method returns loss and informations
    """

    def __init__(self, division, negative_loss, evaluate, config_parser, recorder, col_names, **kwargs):
        super().__init__(**kwargs)
        self.config_parser = config_parser
        self.division = division
        self.col_names = col_names
        self.evaluate = evaluate
        self.recorder = recorder
        self.negative_loss = negative_loss

    def compute(self, config, budget, **kwargs):
        try:
            pp = ModelRunner(**self.config_parser.bohb_config2pipe_param(config))
            k = len(self.division)
        except ValueError:
            status = "pipeline loading error"
            logging.error(status)
            return {
                "loss": -1,
                "info": {"config": config, "budget": budget},
            }
        # try:
        score = []
        for i in range(k):
            now_X_test = self.division[i][0]
            now_y_test = self.division[i][1]
            now_X_train_list = []
            now_y_train_list = []
            for j in range(k):
                if j != i:
                    now_X_train_list.append(self.division[j][0])
                    now_y_train_list.append(self.division[j][1])
            now_X_train = np.vstack(now_X_train_list)
            now_y_train = np.hstack(now_y_train_list)
            pp.run(now_X_train, now_y_train, self.col_names)
            y_hat = pp.inference(now_X_test)
            loss = self.evaluate(now_y_test, y_hat)
            if not self.negative_loss:
                loss = 1 - loss
            score.append(loss)
        mean_loss = np.mean(score)

        self.recorder.update(mean_loss, config)
        return {
            "loss": mean_loss,
            "info": {"config": config, "budget": budget},
        }


class Learner:
    """
    learner object for controlling optimization process on Pipelines.

    1. train :
        run the BOHB optimization process and save the pipeline with the best configuration

    2. inference :
        load the best pipeline and call Pipeline.inference

    """

    def __init__(
        self, negative_loss, evaluate_dict, custom_input,
    ):
        self.negative_loss = negative_loss
        self.config_parser = ConfigParser(custom_model=custom_input["custom_model"])
        self.evaluate = evaluate_dict[custom_input["metric"]]
        self.recorder = None
        self.metric = custom_input["metric"]
        self.n_worker = custom_input["n_worker"]
        self.n_iter = custom_input["n_iter"]
        self.evaluate_dict = evaluate_dict
        self.best_model = None
        self.temp_best_model = None
        self.metric_info = {}

    def train(self, X, y, col_names):
        k = 5

        logging.info("[learner] start data division")
        division = []
        for i in range(k - 1):
            X_rest, X_part, y_rest, y_part = train_test_split(X, y, test_size=1 / (k - i))
            division.append([X_part, y_part])
            X = X_rest
            y = y_rest
        division.append([X, y])

        # HPO using 4 divisions
        # one division for hold-out

        logging.info("[learner] start name server")
        self.recorder = Recorder()
        name_server = hpns.NameServer(run_id="learner", host="127.0.0.1", port=None)
        name_server.start()
        for i in range(self.n_worker):
            worker = MyWorker(
                division[:-1],
                col_names=col_names,
                negative_loss=self.negative_loss,
                evaluate=self.evaluate,
                config_parser=self.config_parser,
                recorder=self.recorder,
                run_id="learner",
                nameserver="127.0.0.1",
                id=i,
            )
            worker.run(background=True)

        logging.info("[learner] generate configspace")
        configspace = self.config_parser.build_bohb_config()

        logging.info("[learner] start bohb")
        bohb = BOHB(
            configspace=configspace,
            run_id="learner",
            nameserver="127.0.0.1",
            min_budget=1.0,
            max_budget=1.0,
            # logger=logging.getLogger("learner"),
        )
        bohb.run(n_iterations=self.n_iter)
        bohb.shutdown(shutdown_workers=True)
        name_server.shutdown()

        logging.info("[learner] train end")
        self.done = True

        logging.info("[learner] evaluate model with hold-out set")
        # first evaluate model with hold-out
        self.temp_best_model = ModelRunner(
            **self.config_parser.bohb_config2pipe_param(self.recorder.best_config)
        )
        X_train_list = []
        y_train_list = []
        for i in range(k - 1):
            X_train_list.append(division[i][0])
            y_train_list.append(division[i][1])
        X_train = np.vstack(X_train_list)
        y_train = np.hstack(y_train_list)
        X_test, y_test = division[-1]
        self.temp_best_model.run(X_train, y_train, col_names)
        y_hat = self.temp_best_model.inference(X_test)
        for key, item in self.evaluate_dict.items():
            self.metric_info[key] = item(y_test, y_hat)

        # save best_model with full data

        logging.info("[learner] save best model")
        self.best_model = ModelRunner(**self.config_parser.bohb_config2pipe_param(self.recorder.best_config))
        self.best_model.run(X, y, col_names)

    def report(self):
        # best model config
        best_config = self.recorder.best_config

        # evaluate result
        evaluate = self.metric_info

        # feature importance
        feature_importance = self.best_model.get_model().feature_importance()

        ret_message = ""
        ret_message_ko = ""
        ret_message += "number of iterations : [ %s ] \n" % (self.n_iter,)
        ret_message_ko += "평가 반복 횟수 : [ %s ] \n" % (self.n_iter,)
        ret_message += "number of workers : [ %s ] \n" % (self.n_worker,)
        ret_message_ko += "평가에 사용한 워커 수 : [ %s ] \n" % (self.n_worker,)
        ret_message += "evaluation metric : [ %s ] \n" % (self.metric,)
        ret_message_ko += "최적화 평가 기준 : [ %s ] \n" % (self.metric,)
        return {
            "best_config": best_config,
            "evaluate": evaluate,
            "feature_importance": feature_importance,
            "log": {"en": ret_message, "ko": ret_message_ko},
        }
