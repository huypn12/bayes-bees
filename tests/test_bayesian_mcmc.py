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
from scripts.bayesian_mcmc import BayesianMcmc
from scripts.models.bees_model import BeesModel

import pytest


@pytest.fixture
def mcmc():
    dtmc_filepath = 'data/prism/bee_multiparam_synchronous_3.pm'
    bscc_filepath = 'data/prism/bee_multiparam_synchronous_3.txt'
    model = BeesModel.from_files(dtmc_filepath, bscc_filepath)
    mcmc = BayesianMcmc(model)
    assert model.bscc_eval_mode == BeesModel.BSCC_MODE_CHAIN_RUN
    return mcmc


@pytest.fixture
def bees_data():
    dtmc_filepath = 'data/prism/bee_multiparam_synchronous_3.pm'
    bscc_filepath = 'data/prism/bee_multiparam_synchronous_3.txt'
    model = BeesModel.from_files(dtmc_filepath, bscc_filepath)
    p_true = [0.2, 0.5, 0.7]
    m, d = model.sample(chain_params=p_true, trials_count=10000)
    return (m, d)


def test_simplex_syndata(mcmc, bees_data):
    assert mcmc.data_model.bscc_eval_mode == BeesModel.BSCC_MODE_CHAIN_RUN
    m, d = bees_data
    assert sum(m) == 10000
    assert sum(d) - 1.0 < 1e-9


def test_estimate_by_pfuncs(mcmc, bees_data):
    m, _ = bees_data
    mcmc.data_model.bscc_eval_mode = BeesModel.BSCC_MODE_PFUNCS
    mcmc.estimate_p(m)
    for p in mcmc.estimated_params['P']:
        assert 0 <= p and p <= 1
    log_llh = mcmc.estimated_params['log_llh']
    print(log_llh)
    aic = mcmc.estimated_params['AIC']
    assert -100 < log_llh and log_llh < 0
    assert 6 < aic and aic < 200


def test_estimate_by_chainruns(mcmc, bees_data):
    m, _ = bees_data
    mcmc.data_model.set_chainruns_count(1000 *
                                        mcmc.data_model.get_bscc_count())
    mcmc.estimate_p(m)
    for p in mcmc.estimated_params['P']:
        assert p > 0
    log_llh = mcmc.estimated_params['log_llh']
    aic = mcmc.estimated_params['AIC']
    assert -100 < log_llh and log_llh < 0
    assert 6 < aic and aic < 200


"""
def test_3bees(mcmc, bees_data):
    print("Data multinomial: {}".format(m))
    print("Data histogram: {}".format(f))
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
"""
