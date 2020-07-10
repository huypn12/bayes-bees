from examples.base_experiment import BaseExperiment

from scripts import config
from scripts.bayesian_mcmc_linear import BayesianMcmcLinear
from scripts.models.bees_linear_model import BeesLinearModel

import sys
import timeit
import datetime
import logging
from sklearn.metrics import mean_squared_error
from math import sqrt


def setup_logging():
    now_str = str(datetime.datetime.now()).replace(' ', '_')
    filename = 'run_linear_' + now_str + '.log'
    logfile = 'examples/logs/{}'.format(filename)
    logging.basicConfig(level=logging.DEBUG, filename=logfile)


def run_linear_3bees():
    dtmc_filepath = 'data/prism/bee_multiparam_synchronous_3.pm'
    bscc_filepath = 'data/prism/bee_multiparam_synchronous_3.txt'
    logging.info(dtmc_filepath)
    logging.info(bscc_filepath)
    model = BeesLinearModel.from_files(dtmc_filepath, bscc_filepath)
    model.bscc_eval_mode = BeesLinearModel.BSCC_MODE_PFUNCS
    p_true = [0.1, 0.2]
    logging.info('P true: {}'.format(p_true))
    m, f = model.sample(chain_params=p_true, trials_count=10000)
    logging.info("Data multinomial: {}".format(m))
    logging.info("Data histogram: {}".format(f))
    # pass model in to get BSCC parameterized functions
    mcmc = BayesianMcmcLinear(model)
    mcmc.mh_params['chain_length'] = 2000
    mcmc.hyperparams = {
        'alpha': 1,
        'beta': 10,
    }
    start_time = timeit.default_timer()
    mcmc.estimate_p(m)
    stop_time = timeit.default_timer()
    logging.info('Finished in {} seconds'.format(stop_time - start_time))
    logging.info(mcmc.summarize())


def main():
    setup_logging()
    run_linear_3bees()
    logging.shutdown()


if __name__ == "__main__":
    sys.exit(main())
