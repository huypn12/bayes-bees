from bayesian_mcmc import BayesianMcmc
from bayesian_mcmc_sim import BayesianMcmcSim
from models.bees_model import BeesModel

import itertools
import logging
import timeit
import sys
import random
sys.setrecursionlimit(10**8)

logging.basicConfig(filename='experiment_c.log', level=logging.INFO)


def synthesize_data():
    logging.info('DATA SYNTHESIZING')
    logging.info('Note that this will run only once')
    model_files = [
        # 3 bees
        ('models/prism_utils/bee_multiparam_synchronous_3.pm',
         'models/prism_utils/bee_multiparam_synchronous_3.txt'),
        # 5 bees
        ('models/prism_utils/bee_multiparam_synchronous_5.pm',
         'models/prism_utils/bee_multiparam_synchronous_5.txt'),
        # 10 bees
        ('models/prism_utils/bee_multiparam_synchronous_10.pm',
         'models/prism_utils/bee_multiparam_synchronous_10.txt'),
        # 10 bees
        ('models/prism_utils/bee_multiparam_synchronous_15.pm',
         'models/prism_utils/bee_multiparam_synchronous_15.txt')
    ]


def summarize_data(sample: (list, list, list)):
    (s, m, f) = sample
    logging.info("Data multinomial: {}".format(m))
    logging.info("Data histogram: {}".format(f))


def summarize_inference_result(mcmc):
    logging.info('MCMC proposed prior: Beta(alpha={},beta={})'.format(
        mcmc.hyperparams['alpha'],
        mcmc.hyperparams['beta']
    ))
    logging.info('MCMC chain length: {}'.format(
        mcmc.mh_params['chain_length']))
    logging.info('Estimated parameter: {}'.format(mcmc.estimated_params['P']))
    logging.info('Highest posterior density interval: {}'.format(
        mcmc.estimated_params['HPD']))
    logging.info('Loglikelihood: {}'.format(
        mcmc.estimated_params['log_llh']))
    logging.info('AIC: {}'.format(mcmc.estimated_params['AIC']))


def do_experiment_rational(model, data_m, mh_chain_length):
    logging.info('Metropolis Hastings, get BSCC by rational function evaluation')
    mcmc = BayesianMcmc(model)
    mcmc.mh_params['chain_length'] = mh_chain_length
    start_time = timeit.default_timer()
    mcmc.estimate_p(data_m)
    stop_time = timeit.default_timer()
    elapsed_time = stop_time - start_time
    logging.info('Finished in {} seconds'.format(elapsed_time))
    summarize_inference_result(mcmc)


def do_experiment_chainrun(model, data_m, mh_chain_length, mh_chain_run_factor):
    logging.info('Metropolis Hastings, get BSCC stats by chain running')
    mcmc = BayesianMcmcSim(model)
    mcmc.mh_params['chain_length'] = mh_chain_length
    mcmc.max_trials = mh_chain_run_factor * model.get_bscc_count()
    start_time = timeit.default_timer()
    mcmc.estimate_p(data_m)
    stop_time = timeit.default_timer()
    elapsed_time = stop_time - start_time
    logging.info('Finished in {} seconds'.format(elapsed_time))
    logging.info('#(chain runs) per one estimation: {}'.format(mcmc.max_trials))
    summarize_inference_result(mcmc)


def rand_increasing_sequence(dim):
    seq = [random.randrange(1000000) for i in range(0, dim)]
    norm = sum(seq) * 1.0
    seq = [s / norm for s in seq]
    return sorted(seq)


def do_experiment(model, p_true, trials_count, mh_chain_length, mh_chain_run_factor):
    logging.info('True parameters: {}'.format(p_true))
    (s, m, f) = model.sample(params=p_true, trials_count=trials_count)
    summarize_data((s, m, f))
    do_experiment_rational(model, m, mh_chain_length)
    do_experiment_chainrun(model, m, mh_chain_length, mh_chain_run_factor)


def test_mm3params():
    logging.info('WARM UP TEST, 3 BEES')
    dtmc_filepath = 'models/prism_utils/bee_multiparam_synchronous_3.pm'
    bscc_filepath = 'models/prism_utils/bee_multiparam_synchronous_3.txt'
    model = BeesModel.from_files(dtmc_filepath, bscc_filepath)
    p_true = rand_increasing_sequence(model.get_params_count())
    do_experiment(model, p_true, 1000, 500, 100)


def test_mm15params():
    logging.info('WARM UP TEST, 3 BEES')
    dtmc_filepath = 'models/prism_utils/bee_multiparam_synchronous_15.pm'
    bscc_filepath = 'models/prism_utils/bee_multiparam_synchronous_15.txt'
    model = BeesModel.from_files(dtmc_filepath, bscc_filepath)
    p_true = rand_increasing_sequence(model.get_params_count())
    do_experiment(model, p_true, 1000, 500, 100)



def small_batch():
    logging.info('SMALL BATCH, TEST FOR CORRECT MODEL PROCESSING')
    model_files = [
        # 3 bees
        ('models/prism_utils/bee_multiparam_synchronous_3.pm',
         'models/prism_utils/bee_multiparam_synchronous_3.txt'),
        # 5 bees
        ('models/prism_utils/bee_multiparam_synchronous_5.pm',
         'models/prism_utils/bee_multiparam_synchronous_5.txt'),
        # 10 bees
        ('models/prism_utils/bee_multiparam_synchronous_10.pm',
         'models/prism_utils/bee_multiparam_synchronous_10.txt'),
        # 10 bees
        ('models/prism_utils/bee_multiparam_synchronous_15.pm',
         'models/prism_utils/bee_multiparam_synchronous_15.txt')
    ]
    
    mh_chain_length = [100, 200]
    mh_chain_run_factor = [100, 200]
    synthetic_data_trials = [100, 200]
    for setting in itertools.product(model_files, synthetic_data_trials, mh_chain_length, mh_chain_run_factor):
        files, trials_count, mh_chainLength, mh_chainRuns = setting
        logging.info('{}'.format('-' * 80))
        logging.info('Model DTMC file {}'.format(files[0]))
        logging.info('Model BSCC file {}'.format(files[1]))
        model = BeesModel.from_files(*files)
        logging.info('#params {}, # BSCCs{}'.format(model.get_params_count(), model.get_bscc_count()))
        true_params = rand_increasing_sequence(model.get_params_count())
        do_experiment(model, true_params, trials_count, mh_chainLength, mh_chainRuns)


def large_batch():
    logging.info('LARGE BATCH, SETTINGS TEST')
    model_files = [
        # 3 bees
        ('models/prism_utils/bee_multiparam_synchronous_3.pm',
         'models/prism_utils/bee_multiparam_synchronous_3.txt'),
        # 5 bees
        ('models/prism_utils/bee_multiparam_synchronous_5.pm',
         'models/prism_utils/bee_multiparam_synchronous_5.txt'),
        # 10 bees
        ('models/prism_utils/bee_multiparam_synchronous_10.pm',
         'models/prism_utils/bee_multiparam_synchronous_10.txt'),
        # 15 bees
        ('models/prism_utils/bee_multiparam_synchronous_15.pm',
         'models/prism_utils/bee_multiparam_synchronous_15.txt')
    ]

    mh_chain_length = [500, 5000, 50000]
    mh_chain_run_factor = [100, 1000]
    synthetic_data_trials = [100, 1000]
    for setting in itertools.product(model_files, synthetic_data_trials, mh_chain_length, mh_chain_run_factor):
        files, trials_count, mh_chainLength, mh_chainRuns = setting
        logging.info('Model DTMC file {}'.format(files[0]))
        logging.info('Model BSCC file {}'.format(files[1]))
        model = BeesModel.from_files(*files)
        logging.info('#params {}, # BSCCs{}'.format(model.get_params_count(), model.get_bscc_count()))
        true_params = rand_increasing_sequence(model.get_params_count())
        do_experiment(model, true_params, trials_count, mh_chainLength, mh_chainRuns)


def main():
    test_mm15params()
    # small_batch()


if __name__ == "__main__":
    sys.exit(main())
