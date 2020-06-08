## Experiment: Parse Prism result rational functions,
## Measure run time of evaluation


import sys
sys.setrecursionlimit(10**8)

import timeit
import logging
logging.basicConfig(filename='experiment_b.log',level=logging.INFO)

from models.bees_model import BeesModel

from bayesian_mcmc import BayesianMcmc

def summarize_data(sample: (list, list, list)):
    (s, m, f) = sample
    logging.info("Data multinomial: {}".format(m))
    logging.info("Data histogram: {}".format(f))

def summarize_inference_result(model):
    logging.info('MCMC chain length: {}'.format(model.mh_params['chain_length']))
    logging.info('Estimated parameter: {}'.format(model.estimated_params['P']))
    logging.info('Highest posterior density interval: {}'.format(model.estimated_params['HPD']))
    logging.info('Log likelihood: {}'.format(model.estimated_params['log_llh']))
    logging.info('AIC: {}'.format(model.estimated_params['AIC']))

def do_experiment(model, p_true, chain_samples):
    # pass model in to get BSCC parameterized functions
    logging.info('\n\n{}'.format('#'* 80))
    logging.info('Model: {}'.format(model.get_name()))
    logging.info('True parameters: {}'.format(p_true))
    (s, m, f) = model.sample(params=p_true, trials_count=10000)
    summarize_data((s, m, f))
    mcmc = BayesianMcmc(model)
    start_time = timeit.default_timer()
    mcmc.estimate_p(m)
    stop_time = timeit.default_timer()
    elapsed_time = stop_time - start_time
    logging.info('Finished in {} seconds'.format(elapsed_time))
    summarize_inference_result(mcmc)

def rand_increasing_sequence():
    pass

def mm_3params():
    dtmc_filepath = 'models/prism_utils/bee_multiparam_synchronous_3.pm'
    bscc_filepath = 'models/prism_utils/bee_multiparam_synchronous_3.txt'
    model = BeesModel.from_files(dtmc_filepath, bscc_filepath)
    p_true = [0.1, 0.2, 0.3]
    do_experiment(model, p_true)  

def mm_5params():
    dtmc_filepath = 'models/prism_utils/bee_multiparam_synchronous_5.pm'
    bscc_filepath = 'models/prism_utils/bee_multiparam_synchronous_5.txt'
    model = BeesModel.from_files(dtmc_filepath, bscc_filepath)
    p_true = [0.1, 0.2, 0.3]
    do_experiment(model, p_true)

def mm_10params():
    dtmc_filepath = 'models/prism_utils/bee_multiparam_synchronous_10.pm'
    bscc_filepath = 'models/prism_utils/bee_multiparam_synchronous_10.txt'
    model = BeesModel.from_files(dtmc_filepath, bscc_filepath)
    p_true = [0.1, 0.2, 0.3]
    do_experiment(model, p_true)  

def mm_15params():
    dtmc_filepath = 'models/prism_utils/bee_multiparam_synchronous_15.pm'
    bscc_filepath = 'models/prism_utils/bee_multiparam_synchronous_15.txt'
    model = BeesModel.from_files(dtmc_filepath, bscc_filepath)
    p_true = [0.1, 0.2, 0.3]
    do_experiment(model, p_true)  


def main():
    knuth_die_experiment()
    bees_2_experiment()
    bees_5_experiment()
    bees_10_experiment()

if __name__ == "__main__":
    sys.exit(main())