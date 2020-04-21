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
        self.estimated_params = {
        }
        self.hyperparams = {
            'alpha': 1,
            'beta': 1,
        }
        self.traces = []
        self.mh_params = {
            'chain_length': 1000,
        }

    # Proposed distribution: beta
    def transition(self, p):
        alpha = self.hyperparams['alpha']
        beta = self.hyperparams['beta']
        p_new = np.random.beta(alpha, beta)
        while p_new == p:
            p_new = np.random.beta(alpha, beta)
        return p_new

    def prior(self, p):
        """
        Alpha and Beta must be positive
        This function is basically a filter. Given that the transition function would always give the valid alpha and beta,
        it is questionable if this function ever returns 0
        """
        if p <= 0:
            return 0
        return 1

    # Likelihood: multinomial with parameterized P
    def log_likelihood(self, p, pfuncs, data):
        # Log likelihood of multinomial distribution
        P = [f(p) for f in pfuncs]
        N = sum(data)
        print(P)
        print(multinomial(N, P).pmf(data))
        return np.sum(np.log(multinomial(N, P).pmf(data)))

    def acceptance_rule(self, llh, llh_new):
        if llh < llh_new:
            return True
        else:
            accept = np.random.uniform(0, 1)
            print((llh_new - llh)) # nan, fix this, perhaps -Inf
            return accept < np.exp(llh_new - llh)

    def metropolis_hastings(self, pfuncs, data):
        p = self.transition(0)
        accepted = []
        rejected = []   
        for i in range(self.mh_params['chain_length']):
            p_new = self.transition(p)    
            p_llh = self.log_likelihood(p, pfuncs, data)
            p_new_llh = self.log_likelihood(p_new, pfuncs, data) 
            print(p_llh, " ", p_new_llh)
            if (self.acceptance_rule(p_llh + np.log(self.prior(p)), p_new_llh+np.log(self.prior(p_new)))):            
                p = p_new
                accepted.append(p_new)
            else:
                rejected.append(p_new)
        print(accepted)            
        return np.array(accepted), np.array(rejected)


from knuth_die.knuth_die import KnuthDie

def main():
    model = KnuthDie(p=0.1)
    (s, m, f) = model.sample(10000)
    print("Sample categorical {}".format(s))
    print("Sample multinomial {}".format(m))
    print("Sample frequency   {}".format(f))

    bayes = BayesianMcmc()
    bayes.metropolis_hastings(model.get_pfuncs(), m)

if __name__ == "__main__":
    sys.exit(main())