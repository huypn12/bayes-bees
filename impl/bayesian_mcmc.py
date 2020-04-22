import sys
import numpy as np
import scipy as sp
from scipy.stats import multinomial

class BayesianMcmc(object):
    def __init__(self, model):
        super().__init__()
        self.hyperparams = {
            'alpha': 1,
            'beta': 1,
        }
        self.mh_params = {
            'chain_length': 50000,
        }
        self.traces = None
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
        return p_new

    def prior(self, p):
        eps = 1e-12
        if np.product(p) <= eps:
            return 0
        return 1

    # Likelihood: multinomial with parameterized P
    def log_likelihood(self, p, data):
        # Log likelihood of multinomial distribution
        P = self.data_model.eval_bscc_pfuncs(p)
        N = sum(data)
        return np.sum(np.log(multinomial(N, P).pmf(data)))

    def llh(self, p, data):
        P = self.data_model.eval_bscc_pfuncs(p)

    def acceptance_rule(self, llh, llh_new):
        if llh < llh_new:
            return True
        else:
            accept = np.random.uniform(0, 1)
            return accept < np.exp(llh_new - llh)

    def metropolis_hastings(self, data):
        p = self.transition()
        accepted = []
        for i in range(self.mh_params['chain_length']):
            p_new = self.transition()
            p_llh = self.log_likelihood(p, data)
            p_new_llh = self.log_likelihood(p_new, data) 
            if (self.acceptance_rule(p_llh + np.log(self.prior(p)), p_new_llh + np.log(self.prior(p_new)))):            
                p = p_new
                accepted.append(p_new)
        self.traces = np.array(accepted)

    def compute_hpd(self, data, alpha):
        pass


## UNIT TEST ##
from models.knuth_die import KnuthDie
from models.bees2 import Bees2

def knuth_die_experiment():
    model = KnuthDie()
    (s, m, f) = model.sample(
        params=[0.3],
        sample_size=10000
        )
    mcmc = BayesianMcmc(model) # pass model in to get BSCC parameterized functions
    mcmc.metropolis_hastings(m)
    print(mcmc.traces)

def bees_2_experiment():
    model = Bees2()
    (s, m, f) = model.sample(
        params=[0.1, 0.2],
        sample_size=10000
        )
    mcmc = BayesianMcmc(model) 
    mcmc.metropolis_hastings(m)
    print(mcmc.traces)

def main():
    bees_2_experiment()

if __name__ == "__main__":
    sys.exit(main())