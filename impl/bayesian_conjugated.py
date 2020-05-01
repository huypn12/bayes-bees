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

