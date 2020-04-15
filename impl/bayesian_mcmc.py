import sys

import pymc3 as pm
import numpy as np
import scipy as sp
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib as mpl

isLogging = False
"""
Data synthesizer
"""


class KnuthDie(object):
    def __init__(self, p=None):
        super().__init__()
        self.p = p if p is not None else 0.5
        self.bscc_pdist = self.init_bscc_pdist()
        self.bscc_dist = self.eval_bscc_pdist(self.bscc_pdist)

    def init_bscc_pdist(self, ):
        # parameterized distribution of being in BSCCs
        pdist = [
            'p**2 / (p + 1)',
            '(( -1 )*p**2 + p) / (p + 1)',
            '(p**2) / (p + 1)',
            '(( -1 )* p**2 + p) / (p + 1)',
            '(p**2 - 2*p + 1)  / (p + 1)',
            '(( -1 )* p**2 + p) / (p + 1)',
        ]
        return pdist

    def eval_bscc_pdist(self, pdist):
        dist = []
        for expr in self.bscc_pdist:
            val = eval(expr, None, {'p': self.p})
            dist.append(val)
            # print("Expression {} evaluated to {}".format(expr, val))
        # print("Sum = {}".format(sum(dist)))
        return dist

    def sample(self, sample_size: int = 1000):
        """
        Sample by categorical distribution
        Later can be transformed into multinomial sample
        """
        categorical = np.random.choice(len(self.bscc_dist),
                                       sample_size,
                                       p=self.bscc_dist)
        multinomial = [0] * len(self.bscc_dist)
        for it in categorical:
            multinomial[it] += 1
        norm = sum(multinomial) * 1.0
        frequency = [v / norm for v in multinomial]
        return (categorical, multinomial, frequency)


"""
Interval solver
Given:
    p_1,...,p_k \in R
    f(p_1,...,p_k) is a rational function
Find
    l_i <= p_i <= u_i for i in 1...k
Constraint:
    a <= f(p_1,...,p_k) <= b
"""


class IntervalSolver(object):
    def __init__(self):
        super().__init__()


"""
Parameter inference using Bayesian conjugation.
From pymc3 only hpd is used. Easier to implement from scratch
"""


class BayesianMultinomialConjugated(object):
    def __init__(self, ):
        super().__init__()
        self.estimated_params = {'alpha': None}
        self.traces = None
        self.data_source = KnuthDie(0.4)

    def bayes(self, data, alpha):
        new_alpha = [sum(x) for x in zip(alpha, data)]
        estimated_p = alpha / sum(alpha)
        return (new_alpha, estimated_p)

    def estimate(self, data):
        n_iter = 100
        alpha = np.ones(K)
        estimated_p = np.zeros(K)
        traces = []
        for sample in data:
            alpha, estimated_p = bayes(data, alpha)
            traces.append((alpha, estimated_p))

    """
    TODO: point and interval estimation
    1. Point estimation: given estimated parameter P{BSCC = i}, estimate p (z3)
    2. Interval estimation: given estimated HPD of P{BSCC = i}, estimate interval of p (space sampling/refining)
    """


"""
Parametre inference without Ba
"""


class BayesianMc(object):
    def __init__(self):
        super().__init__()
        self.estimated_params = {'alpha': None}
        self.traces = []

    def my_prior(self, p):
        llk = [
            p**2 / (p + 1),
            ((-1) * p**2 + p) / (p + 1),
            (p**2) / (p + 1),
            ((-1) * p**2 + p) / (p + 1),
            (p**2 - 2 * p + 1) / (p + 1),
            ((-1) * p**2 + p) / (p + 1),
        ]
        return llk

    def estimate(self, data):
        with pm.Model() as model:
            p = pm.Beta('p', alpha=2, beta=2)
            props = self.my_prior(p)
            model = pm.Multinomial('likelihood', n=6, p=props, observed=data)
            step = pm.Metropolis()
            trace = pm.sample(5000, step=step, tune=10000)
            self.traces.append(trace)
            print(pm.summary(trace))


def test_experiment():
    experiment = KnuthDie(p=0.1)
    (s, m, f) = experiment.sample(10000)
    print("Sample categorical {}".format(s))
    print("Sample multinomial {}".format(m))
    print("Sample frequency   {}".format(f))
    bayes = BayesianMc()
    bayes.estimate(data=m)


def main():
    test_experiment()


if __name__ == "__main__":
    sys.exit(main())