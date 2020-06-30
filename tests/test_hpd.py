from scripts.bayesian_mcmc import BayesianMcmc

import pytest
import numpy as np
import pickle


@pytest.fixture
def data():
    with open('tests/test_hpd.pickle', 'rb') as f:
        data = pickle.load(f)
    return data


def test_hpd(data):
    sample, expected_hpd = data
    mcmc = BayesianMcmc(None)
    hpd = mcmc._compute_hpd(sample, 0.95)
    print(hpd)
    for i in range(0, len(hpd)):
        assert hpd[i] - expected_hpd[i] < 1e-9
