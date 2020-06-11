from bayesian_mcmc import BayesianMcmc
from models.bees_linear_model import BeesLinearModel

import numpy as np
from scipy.stats import multinomial
from scipy.stats import beta


class BayesianMcmcLinear(BayesianMcmc):
    def __init__(self, model: BeesLinearModel):
        super().__init__(model)
        self.hyperparams = {
            'alpha': 2,
            'beta': 5,
        }
    
    def log_likelihood(self, p, data):
        chain_p = self.data_model.eval_chain_params(p)
        return super().log_likelihood(chain_p, data)
