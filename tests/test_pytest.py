import pytest

from scripts.bayesian_mcmc import BayesianMcmc


@pytest.fixture
def mcmc():
    return BayesianMcmc()
