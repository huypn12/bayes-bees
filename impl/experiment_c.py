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
        ('models/prism/bee_multiparam_synchronous_3.pm',
         'models/prism/bee_multiparam_synchronous_3.txt'),
        # 5 bees
        ('models/prism/bee_multiparam_synchronous_5.pm',
         'models/prism/bee_multiparam_synchronous_5.txt'),
        # 10 bees
        ('models/prism/bee_multiparam_synchronous_10.pm',
         'models/prism/bee_multiparam_synchronous_10.txt'),
        # 10 bees
        ('models/prism/bee_multiparam_synchronous_15.pm',
         'models/prism/bee_multiparam_synchronous_15.txt')
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
    logging.info('...')
    logging.info(
        'Metropolis Hastings, get BSCC by rational function evaluation')
    mcmc = BayesianMcmc(model)
    mcmc.mh_params['chain_length'] = mh_chain_length
    mcmc.hyperparams = {
        'alpha': 1.5,
        'beta': 1.5,
    }
    start_time = timeit.default_timer()
    mcmc.estimate_p(data_m)
    stop_time = timeit.default_timer()
    elapsed_time = stop_time - start_time
    logging.info('Finished in {} seconds'.format(elapsed_time))
    summarize_inference_result(mcmc)


def do_experiment_chainrun(model, data_m, mh_chain_length, mh_chain_run_factor):
    logging.info('...')
    logging.info('Metropolis Hastings, get BSCC stats by chain running')
    mcmc = BayesianMcmcSim(model)
    mcmc.mh_params['chain_length'] = mh_chain_length
    mcmc.max_trials = mh_chain_run_factor * model.get_bscc_count()
    mcmc.hyperparams = {
        'alpha': 1.5,
        'beta': 1.5,
    }
    start_time = timeit.default_timer()
    mcmc.estimate_p(data_m)
    stop_time = timeit.default_timer()
    elapsed_time = stop_time - start_time
    logging.info('Finished in {} seconds'.format(elapsed_time))
    logging.info(
        '#(chain runs) per one estimation: {}'.format(mcmc.max_trials))
    summarize_inference_result(mcmc)


def rand_increasing_sequence(dim):
    seq = [random.uniform(0, 1) for i in range(0, dim)]
    return sorted(seq)


def do_experiment(model, p_true, trials_count, mh_chain_length, mh_chain_run_factor):
    logging.info('True parameters: {}'.format(p_true))
    (s, m, f) = model.sample(params=p_true, trials_count=trials_count)
    summarize_data((s, m, f))
    do_experiment_rational(model, m, mh_chain_length)
    do_experiment_chainrun(model, m, mh_chain_length, mh_chain_run_factor)


def test_mm3params():
    logging.info('SINGLE TEST, 3 BEES')
    dtmc_filepath = 'models/prism/bee_multiparam_synchronous_3.pm'
    bscc_filepath = 'models/prism/bee_multiparam_synchronous_3.txt'
    model = BeesModel.from_files(dtmc_filepath, bscc_filepath)
    p_true = rand_increasing_sequence(model.get_params_count())
    do_experiment(model, p_true, 1000, 500, 100)


def test_mm10params():
    logging.info('SINGLE TEST, 15 BEES')
    dtmc_filepath = 'models/prism/bee_multiparam_synchronous_10.pm'
    bscc_filepath = 'models/prism/bee_multiparam_synchronous_10.txt'
    model = BeesModel.from_files(dtmc_filepath, bscc_filepath)
    p_true = rand_increasing_sequence(model.get_params_count())
    do_experiment(model, p_true, 1000, 500, 100)


def small_batch():
    logging.info('SMALL BATCH, TEST FOR CORRECT MODEL PROCESSING')
    model_files = [
        # 3 bees
        ('models/prism/bee_multiparam_synchronous_3.pm',
         'models/prism/bee_multiparam_synchronous_3.txt'),
        # 5 bees
        ('models/prism/bee_multiparam_synchronous_5.pm',
         'models/prism/bee_multiparam_synchronous_5.txt')
    ]
    mh_chain_length = [100, 200]
    mh_chain_run_factor = [100, 200]
    synthetic_data_trials = [100, 200]
    for setting in itertools.product(model_files, synthetic_data_trials, mh_chain_length):
        files, trials_count, mh_chainLength = setting
        logging.info('{}'.format('-' * 80))
        logging.info('MODEL INFO')
        logging.info('Model DTMC file {}'.format(files[0]))
        logging.info('Model BSCC file {}'.format(files[1]))
        model = BeesModel.from_files(*files)
        logging.info('#params {}, # BSCCs{}'.format(
            model.get_params_count(), model.get_bscc_count()))
        p_true = rand_increasing_sequence(model.get_params_count())
        logging.info('True parameters: {}'.format(p_true))
        (s, m, f) = model.sample(params=p_true, trials_count=trials_count)
        summarize_data((s, m, f))
        do_experiment_rational(model, m, mh_chainLength)
        for chain_run_factor in mh_chain_run_factor:
            do_experiment_chainrun(model, m, mh_chainLength, chain_run_factor)


def large_batch():
    logging.info('LARGE BATCH, SETTINGS TEST')
    model_files = [
        # 3 bees
        ('models/prism/bee_multiparam_synchronous_3.pm',
         'models/prism/bee_multiparam_synchronous_3.txt'),
        # 5 bees
        ('models/prism/bee_multiparam_synchronous_5.pm',
         'models/prism/bee_multiparam_synchronous_5.txt'),
        # 10 bees
        ('models/prism/bee_multiparam_synchronous_10.pm',
         'models/prism/bee_multiparam_synchronous_10.txt'),
        # 15 bees
        ('models/prism/bee_multiparam_synchronous_15.pm',
         'models/prism/bee_multiparam_synchronous_15.txt')
    ]
    mh_chain_length = [500, 1000]
    mh_chain_run_factor = [100, 500]
    synthetic_data_trials = [100, 10000]
    for setting in itertools.product(model_files, synthetic_data_trials, mh_chain_length):
        files, trials_count, mh_chainLength = setting
        logging.info('{}'.format('-' * 80))
        logging.info('MODEL INFO')
        logging.info('Model DTMC file {}'.format(files[0]))
        logging.info('Model BSCC file {}'.format(files[1]))
        model = BeesModel.from_files(*files)
        logging.info('#params={}, #BSCCs={}'.format(
            model.get_params_count(), model.get_bscc_count()))
        p_true = rand_increasing_sequence(model.get_params_count())
        logging.info('True parameters: {}'.format(p_true))
        (s, m, f) = model.sample(params=p_true, trials_count=trials_count)
        logging.info(
            'Synthetic data, number of trials: {}'.format(trials_count))
        summarize_data((s, m, f))
        do_experiment_rational(model, m, mh_chainLength)
        for chain_run_factor in mh_chain_run_factor:
            do_experiment_chainrun(model, m, mh_chainLength, chain_run_factor)


def evaluation_time():
    logging.info('LARGE BATCH, SETTINGS TEST')
    model_files = [
        # 3 bees
        ('models/prism/bee_multiparam_synchronous_3.pm',
         'models/prism/bee_multiparam_synchronous_3.txt'),
        # 5 bees
        ('models/prism/bee_multiparam_synchronous_5.pm',
         'models/prism/bee_multiparam_synchronous_5.txt'),
        # 10 bees
        ('models/prism/bee_multiparam_synchronous_10.pm',
         'models/prism/bee_multiparam_synchronous_10.txt'),
        # 15 bees
        ('models/prism/bee_multiparam_synchronous_15.pm',
         'models/prism/bee_multiparam_synchronous_15.txt')
    ]
    mh_chain_run_factor = [100, 500, 1000]
    max_trials = [100, 500, 1000, 10000]
    for file in model_files:
        logging.info('{}'.format('-' * 80))
        logging.info('EVALUATION TIME')
        logging.info('Model DTMC file {}'.format(file[0]))
        logging.info('Model BSCC file {}'.format(file[1]))
        model = BeesModel.from_files(*file)
        logging.info('#params={}, #BSCCs={}'.format(
            model.get_params_count(), model.get_bscc_count()))
        p_true = rand_increasing_sequence(model.get_params_count())
        logging.info('True parameters: {}'.format(p_true))

        for trials_count in max_trials:
            logging.info('Sample with BSCC Evaluation')
            start_time = timeit.default_timer()
            (s, m, f) = model.sample(params=p_true, trials_count=trials_count)
            stop_time = timeit.default_timer()
            elapsed_time = stop_time - start_time
            logging.info('Finished in {} seconds'.format(elapsed_time))
            logging.info(
                'Synthetic data, number of trials: {}'.format(trials_count))
            summarize_data((s, m, f))

        logging.info('...')

        for factor in mh_chain_run_factor:
            logging.info('Sample with chain run')
            start_time = timeit.default_timer()
            h = model.sample_run_chain(p_true, max_trials=1000)
            stop_time = timeit.default_timer()
            elapsed_time = stop_time - start_time
            logging.info('Finished in {} seconds'.format(elapsed_time))
            logging.info(
                'Synthetic data, number of trials: {}'.format(trials_count))
            logging.info('Data histogram: {}'.format(f))


def main():
    test_mm10params()
    # small_batch()
    #evaluation_time()
    #large_batch()


if __name__ == "__main__":
    sys.exit(main())
