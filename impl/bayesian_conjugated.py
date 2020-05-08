import sys

import numpy as np
import scipy as sp
import pymc3 as pm

import math

# Distance function
def rmse(p, p_hat):
    s = 0
    for it in zip(p, p_hat):
        diff = it[0] - it[1]
        s += diff * diff
    return math.sqrt(s / len(p))


class BayesianConjugated(object):
    def __init__(self):
        super().__init__()

    # Bayes interval
    def bayes_step(self, data, alpha):
        new_alpha = [sum(x) for x in zip(alpha, data)]
        estimated_p = alpha / sum(alpha)
        return (new_alpha, estimated_p)

    def bayes(self, data):
        K = len(data)
        alpha = np.ones(K)
        estimated_p = np.zeros(K)
        # traces = []
        for i in range(0, len(data)):
            # inference
            alpha, estimated_p = bayes_step(data[i], alpha)
            # traces.append((alpha, estimated_p))
        return (alpha, estimated_p)

# Frequentist interval
class FrequentistInterval(object):
    def __init__(self):
        super().__init__()

    def get_interval(d, N):
        intervals = []
        for di in d:
            z_a2 = 1.96
            margin = z_a2 * math.sqrt(di* (1 - di) / N)
            intervals.append((ub, lb))
        return intervals



def synthesize_data(n_samples, N):
    data = []
    p_tscc_true = model.eval_bscc_pfuncs(p_true)
    for i in range(0, n_samples):
        s = model.sample(params=p_true, sample_size=N)
        data.append(s)
    return data, p_tscc_true

def estimate_params(N):
    n_samples = 10
    data, p_tscc_true = synthesize_data(n_samples, N)
    freq_intervals = []
    for d in data:
        freq_sample = d[2]
        freq_intervals = get_interval(freq_sample, N)
    bayes_intervals = []
    multinomial_samples = [d[1] for d in data]
    alpha_hat, p_hat = bayes(multinomial_samples)
    posterior_sample = np.random.dirichlet(alpha_hat, 1000)
    bayes_intervals = pm.stats.hpd(posterior_sample)
    return (freq_intervals, bayes_intervals, p_hat, p_tscc_true)