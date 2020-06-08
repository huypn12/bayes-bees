import numpy as np
from scipy.stats import multinomial
from scipy.stats import beta

from bayesian_mcmc import BayesianMcmc


class BayesianMcmcSigmoidal(BayesianMcmc):
    def __init__(self, model):
        super().__init__(model)


    def transition(self):
        # TODO
        return super().transition()
