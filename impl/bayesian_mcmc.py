import sys
sys.setrecursionlimit(10**8)

from pymc3.stats import hpd
import numpy as np
import scipy as sp
from scipy.stats import multinomial
from scipy.stats import beta


class BayesianMcmc(object):
    def __init__(self, model):
        super().__init__()
        self.hyperparams = {
            'alpha': 2,
            'beta': 2,
        }
        self.mh_params = {'chain_length': 50000, 'hpd_alpha': 0.95}
        self.traces = []
        self.data_model = model
        self.estimated_params = {}

    def set_data_model(self, data_model):
        self.data_model = data_model

    # Proposed distribution: beta
    def transition(self, ):
        alpha = self.hyperparams['alpha']
        beta = self.hyperparams['beta']
        params_count = self.data_model.get_params_count()
        p_new = [0] * params_count
        for i in range(0, params_count):
            p_new[i] = np.random.beta(alpha, beta)
        # return p_new 
        return sorted(p_new) # This line is glued to new model r0_,r_1,...,r_k

    def prior(self, p):
        eps = 1e-18
        if np.product(p) <= eps:
            return 0
        return 1

    # Likelihood: multinomial with parameterized P
    def log_likelihood(self, p, data):
        P = self.data_model.eval_bscc_pfuncs(p)
        return self.llh(P, data)

    def llh(self, P, data):
        likelihood = 0
        for it in zip(P, data):
            likelihood += np.log(it[0]) * it[1]
        return likelihood

    def np_llh(self, P, data):
        N = sum(data)
        return np.sum(np.log(multinomial(N, P).pmf(data)))

    def is_accepted(self, llh, llh_new):
        if llh < llh_new:
            return True
        else:
            accept = np.random.uniform(0, 1)
            return accept < np.exp(llh_new - llh)

    def estimate_p(self, data):
        self.metropolis_hastings(data)
        p_hat, log_llh = self.posterior_mean(data)
        self.estimated_params['HPD'] = self.compute_hpd()
        self.estimated_params['P'] = p_hat
        self.estimated_params['log_llh'] = log_llh
        self.estimated_params['AIC'] = -2 * log_llh + 2 * self.data_model.get_params_count()

    def compute_hpd(self, ):
        params_count = self.data_model.get_params_count()
        params_hpd = []
        for i in range(0, params_count):
            trace = [t[i] for t in self.traces]
            h = hpd(np.asarray(trace), credible_interval=0.95)
            params_hpd.append(h)
        return params_hpd

    # E[p] = SUM(p * likelihood(p) * prior(p)) / SUM(likelihood(p) * prior(p))
    def posterior_mean(self, data):
        N = np.sum(data)
        p_hat = np.zeros(self.data_model.get_params_count())
        margin = 0
        for p in self.traces:
            P = self.data_model.eval_bscc_pfuncs(p)
            prior = 1
            for p_i in p:
                prior *= beta(self.hyperparams['alpha'],
                              self.hyperparams['beta']).pdf(p_i)
            llh = multinomial(N, P).pmf(data)
            margin += llh * prior
            p_hat = p_hat + np.array(p) * llh * prior
        p_hat = p_hat / margin
        log_llh = self.np_llh(self.data_model.eval_bscc_pfuncs(p_hat), data)
        return p_hat, log_llh

    def metropolis_hastings(self, data):
        p = self.transition()
        for i in range(self.mh_params['chain_length']):
            p_new = self.transition()
            llh = self.log_likelihood(p, data)
            new_llh = self.log_likelihood(p_new, data)
            if (self.is_accepted(llh + np.log(self.prior(p)),
                                 new_llh + np.log(self.prior(p_new)))):
                p = p_new
                self.traces.append(p_new)


"""
Some notes on complexity of this estimation scheme:
1. There are nIter iterations
2. On each iteration:
    a.
"""

"""
Experiment setup:
1. Parameters of DTMC p = (p1...pk)
2. Parameterized BSCC distribution : f = (f_1...f_n)
3. Posterior on p. Likelihood function is multinomial on f
4. Method. metropolis hastings with Beta distribution as proposal distribution
5. Setup: synthesize data from p_true. Then run the scheme to get p_hat
"""

## UNIT TEST ##
import timeit

# Deprecated models; now switch to general BeesModel
from models.knuth_die import KnuthDie
from models.semisync_2bees import Semisync2bees
from models.semisync_5bees import Semisync5bees
from models.semisync_10bees import Semisync10bees


def knuth_die_experiment():
    model = KnuthDie()
    p_true = [0.3]
    print('Experiment with Knuth Die, p_true={}'.format(p_true))
    (s, m, f) = model.sample(params=[0.3], trials_count=10000)
    # pass model in to get BSCC parameterized functions
    mcmc = BayesianMcmc(model)
    start_time = timeit.default_timer()
    mcmc.estimate_p(m)
    stop_time = timeit.default_timer()
    print('Finished in {} seconds, chain length {}'.format(
        stop_time - start_time, mcmc.mh_params['chain_length']))
    print('Estimated parameter: {}'.format(mcmc.estimated_params['P']))
    print('Log likelihood: {}'.format(mcmc.estimated_params['log_llh']))
    print('AIC: {}\n'.format(mcmc.estimated_params['AIC']))

def main():
    knuth_die_experiment()

if __name__ == "__main__":
    sys.exit(main())