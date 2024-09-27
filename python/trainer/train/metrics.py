from sklearn.metrics import f1_score, accuracy_score, confusion_matrix, mean_squared_error
import numpy as np


def evaluate_rmse(y_test, y_hat):
    return np.sqrt(mean_squared_error(y_test, y_hat))


def evaluate_smape(y_test, y_hat):
    smape = np.abs(y_hat - y_test) / np.maximum(np.abs(y_test) + np.abs(y_hat), 0.0001)
    return np.average(smape, axis=0)


def evaluate_mape(y_test, y_hat):
    mape = np.abs(y_hat - y_test) / np.maximum(np.abs(y_test), 0.0001)
    return np.average(mape, axis=0)


def evaluate_f1_score(y_test, y_hat):
    not_nan = y_test != -1
    return f1_score(y_test[not_nan], y_hat[not_nan], average="weighted")


def evaluate_accuracy_score(y_test, y_hat):
    not_nan = y_test != -1
    return accuracy_score(y_test[not_nan], y_hat[not_nan])


def my_confusion_matrix(y_test, y_hat):
    uniques = np.unique(y_hat)
    class_value = confusion_matrix(y_test, y_hat, labels=uniques)
    return class_value, uniques
