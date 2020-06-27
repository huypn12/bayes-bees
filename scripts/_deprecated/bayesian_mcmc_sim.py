from models.bees_model import BeesModel

import sys
import timeit
import numpy as np
from scipy.stats import multinomial
from scipy.stats import beta

from bayesian_mcmc import BayesianMcmc


class BayesianMcmcSim(BayesianMcmc):
    def __init__(self, model):
        super().__init__(model)
        self.hyperparams = {
            'alpha': 1.5,
            'beta': 1.5,
        }
        self.mh_params = {'chain_length': 5000, 'hpd_alpha': 0.95}
        self.max_trials = 100

    def transition(self, ):
        alpha = self.hyperparams['alpha']
        beta = self.hyperparams['beta']
        params_count = self.data_model.get_params_count()
        p_new = [0] * params_count
        p_new[0] = np.random.beta(alpha, beta)
        if params_count == 1:
            return p_new
        for i in range(1, params_count):
            p_new[i] = np.random.beta(alpha, beta)
        return sorted(p_new)

    def log_likelihood(self, p, data):
        P = self.data_model.sample_run_chain(p, max_trials=self.max_trials)
        return self.llh(P, data)

    def posterior_mean(self, data):
        N = np.sum(data)
        p_hat = np.zeros(self.data_model.get_params_count())
        margin = 0
        for p in self.traces:
            P = self.data_model.sample_run_chain(p, max_trials=self.max_trials)
            prior = 1
            for p_i in p:
                prior *= beta(self.hyperparams['alpha'],
                              self.hyperparams['beta']).pdf(p_i)
            llh = multinomial(N, P).pmf(data)
            margin += llh * prior
            p_hat = p_hat + np.array(p) * llh * prior
        p_hat = p_hat / margin
        log_llh = self.np_llh(self.data_model.sample_run_chain(
            p_hat, max_trials=self.max_trials*10), data)
        return p_hat, log_llh
