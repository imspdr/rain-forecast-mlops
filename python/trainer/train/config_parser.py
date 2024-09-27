import ConfigSpace as CS
from .configuration import model_dict


class ConfigParser:
    """
    for parsing config space from configuration.py
    Provide 2 methods

    1. build_config :
        make config space for BOHB optimization module
        from given configuration in configuration.py

    2. config2pipe_param :
        convert configuration generated configuration
        from BOHB optimization module
        to parameters for Pipeline object
    """

    def __init__(self, custom_model):
        self.model_dict = model_dict
        self.custom_model = custom_model

    ##################################################################################
    # option : BOHB
    ##################################################################################
    def build_bohb_config(self):
        config_space = CS.ConfigurationSpace()
        hp = CS.CategoricalHyperparameter("model-name", list(self.custom_model.keys()))
        config_space.add_hyperparameter(hp)

        for model, params in self.custom_model.items():
            for param, param_space in params.items():
                param_type = self.model_dict[model]["params"][param]["type"]
                if param_type in [0, "0"]:
                    hp = CS.CategoricalHyperparameter(model + "-" + param, param_space["values"])
                    config_space.add_hyperparameter(hp)
                elif param_type in [1, "1"]:
                    hp = CS.UniformIntegerHyperparameter(
                        model + "-" + param, param_space["min"], param_space["max"]
                    )
                    config_space.add_hyperparameter(hp)
                elif param_type in [2, "2"]:
                    hp = CS.UniformFloatHyperparameter(
                        model + "-" + param, param_space["min"], param_space["max"]
                    )
                    config_space.add_hyperparameter(hp)
                else:
                    hp = None

                config_space.add_condition(
                    CS.InCondition(hp, config_space.get_hyperparameter("model-name"), [model])
                )

        return config_space

    def bohb_config2pipe_param(self, conf):
        """
        conf : config dict from configuration space
        grid_param : grid search iteration params
        """
        pipe_param = {}

        for key in conf:
            names = key.split("-")
            step_name = names[0]
            param_name = names[1]
            if step_name == "model":
                pipe_param[conf[key]] = {}
                pipe_param[conf[key]]["step"] = self.model_dict[conf[key]]["class"]
                pipe_param[conf[key]]["params"] = {}
                pipe_param[conf[key]]["index"] = 100
            else:
                pipe_param[step_name]["params"][param_name] = conf[key]

        return pipe_param
