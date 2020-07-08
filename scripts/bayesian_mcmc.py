from scripts import config

import sys
# from pymc3.stats import hpd
import numpy as np
import scipy as sp
import math
from scipy.stats import multinomial
from scipy.stats import beta


class BayesianMcmc(object):
    def __init__(self, model):
        super().__init__()
        self.hyperparams = {
            'alpha': 2,
            'beta': 2,
        }
        self.mh_params = {
            'chain_length': 1000,
            'hpd_alpha': 0.95
        }
        self.traces = []
        self.traces_bscc_dist = []
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
        # Old model p, q0, q1,...,qk-1
        if not config.models['use_old_model']:
            return sorted(p_new)
        # New model r0_,r_1,...,r_k
        return p_new

    def prior(self, p):
        eps = 1e-18
        if np.product(p) <= eps:
            return 0
        return 1

    def llh(self, bscc_dist, data):
        likelihood = 0
        for it in zip(bscc_dist, data):
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
            # h = hpd(np.asarray(trace), credible_interval=0.95)
            h = self._compute_hpd(np.asarray(trace), 0.95)
            params_hpd.append(h)
        return params_hpd

    def _compute_hpd(self, x, alpha):
        """
        Code was taken from PyMC3 project
        """

        n = len(x)
        cred_mass = alpha
        x = np.sort(np.asarray(x))
        interval_idx_inc = int(np.floor(cred_mass*n))
        n_intervals = n - interval_idx_inc
        interval_width = x[interval_idx_inc:] - x[:n_intervals]

        if len(interval_width) == 0:
            raise ValueError('Too few elements for interval calculation')

        min_idx = np.argmin(interval_width)
        hdi_min = x[min_idx]
        hdi_max = x[min_idx+interval_idx_inc]
        return hdi_min, hdi_max

    # E[p] = SUM(p * likelihood(p) * prior(p)) / SUM(likelihood(p) * prior(p))
    def posterior_mean(self, data):
        N = np.sum(data)
        p_hat = np.zeros(self.data_model.get_params_count())
        margin = 0
        for p, bscc_dist in zip(self.traces, self.traces_bscc_dist):
            # P = self.data_model.eval_bscc(p)
            prior = 1
            for p_i in p:
                prior *= beta(self.hyperparams['alpha'],
                              self.hyperparams['beta']).pdf(p_i)
            # llh = multinomial(N, P).pmf(data)
            llh = multinomial(N, bscc_dist).pmf(data)
            margin += llh * prior
            p_hat += np.array(p) * llh * prior
        p_hat = p_hat / margin
        log_llh = self.np_llh(self.data_model.eval_bscc(p_hat), data)
        return p_hat, log_llh

    def metropolis_hastings(self, data):
        p = self.transition()
        bscc_dist = self.data_model.eval_bscc(p)
        for i in range(self.mh_params['chain_length']):
            cur_llh = self.llh(bscc_dist, data)
            if math.isnan(cur_llh) or np.isinf(cur_llh):
                p = self.transition()
                bscc_dist = self.data_model.eval_bscc(p)
                i -= 1
                continue
            p_new = self.transition()
            bscc_dist_new = self.data_model.eval_bscc(p_new)
            new_llh = self.llh(bscc_dist_new, data)
            if math.isnan(new_llh) or np.isinf(new_llh):
                i -= 1
                continue
            if (self.is_accepted(cur_llh + np.log(self.prior(p)),
                                 new_llh + np.log(self.prior(p_new)))):
                p = p_new
                bscc_dist = bscc_dist_new
                self.traces.append(p_new)
                self.traces_bscc_dist.append(bscc_dist)

    def summarize(self, ):
        summary = ''
        summary += 'Data model: \n' + self.data_model.summarize() + '\n'
        summary += 'Prior: Beta(alpha={},beta={})\n'.format(self.hyperparams['alpha'],
                                                            self.hyperparams['beta'])
        summary += 'Chain length: {}\n'.format(self.mh_params['chain_length'])
        summary += 'Estimated parameters: \n'
        i = 0
        for it in zip(self.estimated_params['P'], self.estimated_params['HPD']):
            p = it[0],
            l_hpd, u_hpd = it[1]
            summary += '\t P[{}] {} ; HPD ({} {})\n'.format(i, p, l_hpd, u_hpd)
            i += 1
        summary += 'Log-likelihood: {}\n'.format(self.estimated_params['log_llh'])
        summary += 'AIC: {}'.format(self.estimated_params['AIC'])
        return summary
