from scripts.models.bees_model import BeesModel

import timeit
import pytest


@pytest.fixture
def bees_model():
    dtmc_filepath = 'models/prism/bee_multiparam_synchronous_3.pm'
    bscc_filepath = 'models/prism/bee_multiparam_synchronous_3.txt'
    bees_model = BeesModel.from_files(dtmc_filepath, bscc_filepath)
    return bees_model


def test_size(bees_model):
    assert(len(bees_model.state_labels) == 11)
    assert(len(bees_model.init_ast_pfuncs) == 11)
    assert(len(bees_model.trans_ast_pfuncs) == 11)
    assert(len(bees_model.bscc_labels) == 4)
    assert(len(bees_model.bscc_ast_pfuncs) == 4)


def test_eval(bees_model):
    pass

def test_bscc_pfuncs_sample(bees_model):
    (s, m, f) = bees_model.sample(
        params=[0.1, 0.2, 0.3],
        trials_count=10000
    )
    print('Sampling with BSCC rational function.')
    start_time = timeit.default_timer()
    bscc_eval = bees_model.eval_bscc_pfuncs([0.1, 0.2, 0.3])
    stop_time = timeit.default_timer()
    print('Finished evaluation in {} seconds'.format(
        stop_time - start_time))
    print("\tSimplex assert:    {}".format(
        np.sum(bscc_eval)))
    print("\tcategorical {}".format(s))
    print("\tmultinomial {}".format(m))
    print("\tfrequency   {}".format(f))

def test_chain_run():
    print('Sampling with chain run')
    dtmc_filepath = 'models/prism/bee_multiparam_synchronous_3.pm'
    bscc_filepath = 'models/prism/bee_multiparam_synchronous_3.txt'
    bees_model = BeesModel.from_files(dtmc_filepath, bscc_filepath)
    r = [0.1, 0.2, 0.3]
    start_time = timeit.default_timer()
    h = bees_model.sample_run_chain(r, max_trials=1000)
    stop_time = timeit.default_timer()
    print('Finished in {} seconds, chain length {}'.format(
        stop_time - start_time, 1000))
    assert(sum(h) - 1.0 < 1e-5)
    print('\tSample frequency:', h)
