import sys

import numpy as np
import scipy as sp
from scipy.stats import multinomial

import matplotlib.pyplot as plt
import matplotlib as mpl

isLogging = False

class BayesianMcmc(object):
    def __init__(self):
        super().__init__()
        self.hyperparams = {
            'alpha': 1,
            'beta': 1,
        }
        self.mh_params = {
            'chain_length': 1000,
        }
        self.traces = None
        self.estimated_params = {}

    # Proposed distribution: beta
    def transition(self, p):
        alpha = self.hyperparams['alpha']
        beta = self.hyperparams['beta']
        p_new = [0] * len(p)
        for i in range(0, len(p)):
            p_new[i] = np.random.beta(alpha, beta)
        return p_new

    def prior(self, p):
        eps = 1e-12
        if np.product(p) <= eps:
            return 0
        return 1

    # Likelihood: multinomial with parameterized P
    def log_likelihood(self, p, pfuncs, data):
        # Log likelihood of multinomial distribution
        P = [f(p) for f in pfuncs]
        N = sum(data)
        return np.sum(np.log(multinomial(N, P).pmf(data)))

    def acceptance_rule(self, llh, llh_new):
        if llh < llh_new:
            return True
        else:
            accept = np.random.uniform(0, 1)
            return accept < np.exp(llh_new - llh)

    def metropolis_hastings(self, pfuncs, data):
        p = self.transition(0)
        accepted = []
        for i in range(self.mh_params['chain_length']):
            p_new = self.transition(p)
            p_llh = self.log_likelihood(p, pfuncs, data)
            p_new_llh = self.log_likelihood(p_new, pfuncs, data) 
            if (self.acceptance_rule(p_llh + np.log(self.prior(p)), p_new_llh+np.log(self.prior(p_new)))):            
                p = p_new
                accepted.append(p_new)
        self.trace = np.array(accepted)



### Unit test
from models.knuth_die import KnuthDie

def main():
    model = KnuthDie(p=0.5)
    (s, m, f) = model.sample(10000)
    print("Sample categorical {}".format(s))
    print("Sample multinomial {}".format(m))
    print("Sample frequency   {}".format(f))

    bayes = BayesianMcmc()
    bayes.metropolis_hastings(model.get_pfuncs(), m)

if __name__ == "__main__":
    sys.exit(main())