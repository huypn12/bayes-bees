from sklearn.metrics import mean_squared_error
from math import sqrt


def rmse(y_hat, y):
    return sqrt(mean_squared_error(y_hat, y))
