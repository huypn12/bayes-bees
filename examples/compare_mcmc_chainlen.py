"""
Compare different parameters that would affect the Bayesian Confidence Interval.
Result quality measurement:
1. Accuracy: distance between estimated parameters to true parameters
2. Precision: width of HPD
3. Cost: physical runtime

In a chainrun scheme, the following parameters affect the resu
1. Number of MCMC smaple points (MCMC chain length)
2. Number of chainruns per trial
3. Quality of data
"""

from examples.base_experiment import BaseExperiment

from scripts.bayesian_mcmc import BayesianMcmc
from scripts.models.bees_model import BeesModel

import sys
import timeit
import datetime
import logging
from sklearn.metrics import mean_squared_error
from math import sqrt


def setup_logging():
    now_str = str(datetime.datetime.now()).replace(' ', '_')
    filename = 'compare_mcmc_chainlen' + now_str + '.log'
    logfile = 'examples/logs/{}'.format(filename)
    logging.basicConfig(level=logging.DEBUG, filename=logfile)


class CompareMcmcChainlen(BaseExperiment):
    def __init__(self, model_file, bscc_file):
        super().__init__(model_file, bscc_file)

    def print_log(self, mesg):
        logging.info(mesg)

    def init(self,):
        super().load_files()
        super().synthesize_data()
        self.data_model.bscc_eval_mode = BeesModel.BSCC_MODE_PFUNCS

    def create_model(self, mcmc_chainlen):
        mcmc = BayesianMcmc(self.data_model)
        mcmc.hyperparams['alpha'] = 2
        mcmc.hyperparams['alpha'] = 2
        mcmc.mh_params['chain_length'] = mcmc_chainlen
        return mcmc

    def run_inference(self, mcmc_chainlen):
        self.print_log('Start inferencing, MCMC chain len {}'.format(mcmc_chainlen))
        m = self.syn_data['mult']
        start_time = timeit.default_timer()
        mcmc = self.create_model(mcmc_chainlen)
        mcmc.estimate_p(m)
        stop_time = timeit.default_timer()
        self.print_log('MCMC estimation, ETA(secs) {}'.format(stop_time - start_time))
        print(mcmc.estimated_params['P'])
        rmse = sqrt(mean_squared_error(self.p_true, mcmc.estimated_params['P']))
        self.print_log('RMSE {}'.format(rmse))
        self.print_log(mcmc.summarize())

    def do_experiment(self,):
        # Same setup of MCMC and data, different number of MCMC chainrun
        self.init()
        # last 1000 is to force dumping the log... sorry
        mcmc_chainlen_lst = [1000, 2000, 3000, 4000, 5000,
                             6000, 7000, 8000, 9000, 100000, 1000]
        for mcmc_chainlen in mcmc_chainlen_lst:
            self.run_inference(mcmc_chainlen)


def main():
    file_pairs = [
        ('data/prism/bee_multiparam_synchronous_3.pm',
         'data/prism/bee_multiparam_synchronous_3.txt'),
        ('data/prism/bee_multiparam_synchronous_5.pm',
         'data/prism/bee_multiparam_synchronous_5.txt'),
        ('data/prism/bee_multiparam_synchronous_10.pm',
         'data/prism/bee_multiparam_synchronous_10.txt'),
        ('data/prism/bee_multiparam_synchronous_15.pm',
         'data/prism/bee_multiparam_synchronous_15.txt'),
    ]
    model_file, bscc_file = file_pairs[2]
    cmc = CompareMcmcChainlen(model_file, bscc_file)
    cmc.do_experiment()
    logging.shutdown()


if __name__ == '__main__':
    setup_logging()
    try:
        main()
    finally:
        logging.shutdown()
