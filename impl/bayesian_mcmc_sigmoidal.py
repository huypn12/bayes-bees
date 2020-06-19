import numpy as np
from scipy.stats import multinomial
from scipy.stats import beta

from bayesian_mcmc import BayesianMcmc


class BayesianMcmcRegression(BayesianMcmc):
    def __init__(self, model, domain, regression_funcs):
        super().__init__(model)
        self.domain = domain

    def prior(self, p):
        return super().prior(p)

    def transition(self):
        # TODO
        return super().transition()
