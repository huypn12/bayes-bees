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
            'alpha': 5,
            'beta': 1,
        }
        self.mh_params = {'chain_length': 500, 'hpd_alpha': 0.95}

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
        log_llh = self.np_llh(self.data_model.sample_run_chain(
            p_hat, max_trials=1000), data)
        return p_hat, log_llh


## UNIT TEST ##


def test_3bees():
    max_trials = 1000
    print('Metropolis-Hasting, sampling with chain run, {} trials'.format(max_trials))
    dtmc_filepath = 'models/prism_utils/bee_multiparam_synchronous_3.pm'
    bscc_filepath = 'models/prism_utils/bee_multiparam_synchronous_3.txt'
    bees_model = BeesModel.from_files(dtmc_filepath, bscc_filepath)
    r = [0.1, 0.2, 0.3]
    print('True parameters: {}'.format(r))
    (s, m, f) = bees_model.sample(params=r, trials_count=1000)
    print('Synthetic data {}'.format(m))
    mcmc = BayesianMcmcSim(bees_model)
    start_time = timeit.default_timer()
    mcmc.estimate_p(m)
    stop_time = timeit.default_timer()
    print('Finished in {} seconds, chain length {}'.format(
        stop_time - start_time, mcmc.mh_params['chain_length']))
    print('Estimated parameter: {}'.format(mcmc.estimated_params['P']))
    print('Highest posterior density interval: {}'.format(bees_model.estimated_params['HPD']))
    print('Log likelihood: {}'.format(mcmc.estimated_params['log_llh']))
    print('AIC: {}\n'.format(mcmc.estimated_params['AIC']))


def main():
    test_3bees()


if __name__ == "__main__":
    sys.exit(main())
