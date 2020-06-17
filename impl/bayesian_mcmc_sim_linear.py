from .bayesian_mcmc_sim import BayesianMcmcSim

import numpy as np

class BayesianMcmcSimLinear(BayesianMcmcSim):

    def transition(self):
        alpha = self.hyperparams['alpha']
        beta = self.hyperparams['beta']
        params_count = self.data_model.get_params_count()
        p_new = [0] * params_count
        for i in range(0, params_count):
            p_new[i] = np.random.beta(alpha, beta)
        return p_new

    
    def log_likelihood(self, p, data):
        chain_p = self.data_model.eval_chain_params(p)
        llh = super().log_likelihood(chain_p, data)
        return llh



## UNIT TEST ##
