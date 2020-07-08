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

from scripts import config
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
    filename = 'compare_chainruns_trial' + now_str + '.log'
    logfile = 'examples/logs/{}'.format(filename)
    logging.basicConfig(level=logging.DEBUG, filename=logfile)


class CompareChainrunsTrials(BaseExperiment):
    def __init__(self, model_file, bscc_file):
        super().__init__(model_file, bscc_file)

    def print_log(self, mesg):
        logging.info(mesg)

    def init(self,):
        super().load_files()
        super().synthesize_data()

    def create_model(self, mcmc_chainlen):
        mcmc = BayesianMcmc(self.data_model)
        mcmc.hyperparams['alpha'] = 2
        mcmc.hyperparams['beta'] = 5
        mcmc.mh_params['chain_length'] = mcmc_chainlen
        return mcmc

    def run_inference(self, factor, mcmc_chainlen=2000):
        self.print_log('Start inferencing, MCMC chain len {}'.format(mcmc_chainlen))
        m = self.syn_data['mult']
        start_time = timeit.default_timer()
        mcmc = self.create_model(mcmc_chainlen)
        #bscc_count = mcmc.data_model.bscc_count
        mcmc.data_model.chainruns_count = factor #* bscc_count
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
        model_chainrun_factor_list = [100, 200, 400, 600, 800, 1000,
                                      1200, 1400, 1600, 1800, 2000,
                                      2200, 2400, 2600, 2800, 3000]
        for factor in model_chainrun_factor_list:
            self.run_inference(factor)

    def do_manual_experiment(self,):
        self.init()
        self.p_true = [
            0.033788049511423,
            0.10332722593522348,
            0.547648536701964,
            0.7270400092393097,
            0.7977882851122897
        ]
        self.syn_data['mult'] = [8303, 1181, 53, 83, 125, 255]
        self.syn_data['dist'] = [0.8303, 0.1181, 0.0053, 0.0083, 0.0125, 0.0255]
        model_chainrun_factor_list = [200, 600]
        for factor in model_chainrun_factor_list:
            self.run_inference(factor)


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
    model_file, bscc_file = file_pairs[1]
    cmc = CompareChainrunsTrials(model_file, bscc_file)
    cmc.do_experiment()
    logging.shutdown()


if __name__ == '__main__':
    setup_logging()
    try:
        main()
    finally:
        logging.shutdown()

