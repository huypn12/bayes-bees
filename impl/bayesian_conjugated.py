import sys

import numpy as np
import scipy as sp


class BayesianConjugated(object):
    def __init__(self, N, P):
        super().__init__()
        self.estimated_params = {'P': P}
        self.traces = []

    def bayes(self, data, alpha):
        new_alpha = [sum(x) for x in zip(alpha, data)]
        estimated_p = alpha / sum(alpha)
        return (new_alpha, estimated_p)

    def estimate(self, data):
        estimated_p = self.estimated_params['P']
        alpha = np.ones(len(estimated_p))
        for sample in data:
            alpha, estimated_p = bayes(data, alpha)
            self.traces.append((alpha, estimated_p))
        self.estimated_params['P'] = estimated_p


## UNIT TEST ##
import timeit

from models.bees2 import Bees2

def bees_2_experiment():
    model = Bees2()
    (s, m, f) = model.sample(params=[0.1, 0.2], sample_size=5)
    bc = BayesianConjugated()
    n_iter = 100
    for i in range(0, n_iter):
        pass



def main():
    bees_2_experiment()


if __name__ == "__main__":
    sys.exit(main())