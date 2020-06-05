import numpy as np
from scipy.stats import multinomial
from scipy.stats import beta

from .bayesian_mcmc import BayesianMcmc


class BayesianMcmcSim(BayesianMcmc):
    def log_likelihood(self, p, data):
        P = self.data_model.sample_run_chain(p, max_trials=1000)
        return self.llh(P, data)

    def posterior_mean(self, data):
        N = np.sum(data)
        p_hat = np.zeros(self.data_model.get_params_count())
        margin = 0
        for p in self.traces:
            P = self.data_model.sample_run_chain(p, max_trials=1000)
            prior = 1
            for p_i in p:
                prior *= beta(self.hyperparams['alpha'],
                              self.hyperparams['beta']).pdf(p_i)
            llh = multinomial(N, P).pmf(data)
            margin += llh * prior
            p_hat = p_hat + np.array(p) * llh * prior
        p_hat = p_hat / margin
        log_llh = self.np_llh(self.data_model.sample_run_chain(p_hat, max_trials=1000), data)
        return p_hat, log_llh