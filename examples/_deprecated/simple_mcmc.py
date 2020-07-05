import sys
sys.setrecursionlimit(10**8)

import timeit
import logging
logging.basicConfig(filename='experiment_b.log',level=logging.INFO)

from models.knuth_die import KnuthDie
from models.semisync_2bees import Semisync2bees
from models.semisync_5bees import Semisync5bees
from models.semisync_10bees import Semisync10bees

from bayesian_mcmc import BayesianMcmc

def summarize_data(sample):
    (s, m, f) = sample
    logging.info("Multinomial data: {}".format(m))
    logging.info("Distribution: {}".format(f))

def summarize_inference_result(model):
    logging.info('MCMC chain length: {}'.format(model.mh_params['chain_length']))
    logging.info('Estimated parameter: {}'.format(model.estimated_params['P']))
    logging.info('Highest posterior density interval: {}'.format(model.estimated_params['HPD']))
    logging.info('Log likelihood: {}'.format(model.estimated_params['log_llh']))
    logging.info('AIC: {}'.format(model.estimated_params['AIC']))

def do_experiment(model, p_true):
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

def knuth_die_experiment():
    model = KnuthDie()
    p_true = [0.3]
    do_experiment(model, p_true)

def bees_2_experiment():
    model = Semisync2bees()
    p_true = [0.1, 0.2]
    do_experiment(model, p_true)  

def bees_5_experiment():
    model = Semisync5bees()
    p_true = [0.1, 0.2, 0.4, 0.5, 0.6]
    do_experiment(model, p_true)

def bees_10_experiment():
    model = Semisync10bees()
    p_true = [0.1, 0.2, 0.4, 0.5, 0.6, 0.1, 0.2, 0.4, 0.5, 0.6]
    do_experiment(model, p_true)

def main():
    knuth_die_experiment()
    bees_2_experiment()
    bees_5_experiment()
    bees_10_experiment()

if __name__ == "__main__":
    sys.exit(main())