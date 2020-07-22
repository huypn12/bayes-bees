from examples.base_experiment import BaseExperiment
from examples.rmse import rmse

from scripts import config
from scripts.bayesian_mcmc import BayesianMcmc
from scripts.models.bees_model import BeesModel

import logging
import datetime
import timeit
import random


def setup_logging():
    now_str = str(datetime.datetime.now()).replace(' ', '_')
    filename = 'compare_data_quality_' + now_str + '.log'
    logfile = 'examples/logs/{}'.format(filename)
    logging.basicConfig(level=logging.DEBUG, filename=logfile)


gUseChainRun = False


class CompareDataQuality(BaseExperiment):
    def __init__(self, model_file, bscc_file):
        super().__init__(model_file, bscc_file)
        config.models['use_sympy'] = False
        config.models['use_uniform_prior'] = True

    def print_log(self, mesg):
        logging.info(mesg)

    def init(self,):
        super().load_files()
        self.p_true = [
            0.003186578075742741, 0.1529147183576044, 0.38326481740434626,
            0.38770819078363106, 0.426928113401854, 0.5791164913034477,
            0.7401949229822984, 0.7893002782182501, 0.8139393399312541,
            0.8194092726880179]

    def gen_data(self, trials_count):
        self.print_log('Number of trials in data synthesize: {}'.format(
            trials_count))
        super().synthesize_data(trials_count=trials_count)

    def do_experiment(self,):
        self.print_log('PFUNCS MODE')
        self.data_model.bscc_eval_mode = BeesModel.BSCC_MODE_PFUNCS
        mcmc = BayesianMcmc(self.data_model)
        mcmc_chainlen = 500
        mcmc.mh_params['chain_length'] = mcmc_chainlen
        self.print_log('Start inferencing, MCMC chain len {}'.format(
            mcmc_chainlen))
        m = self.syn_data['mult']
        start_time = timeit.default_timer()
        mcmc.estimate_p(m)
        stop_time = timeit.default_timer()
        self.print_log('MCMC estimation, ETA(secs) {}'.format(
            stop_time - start_time))
        print(mcmc.estimated_params['P'])
        _rmse = rmse(self.p_true, mcmc.estimated_params['P'])
        self.print_log('RMSE {}'.format(_rmse))
        self.print_log(mcmc.summarize())


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
    fp = ('data/prism/bee_multiparam_synchronous_10.pm',
          'data/prism/bee_multiparam_synchronous_10.txt')
    tc = [60, 60*5, 60*10, 60*15, 60*20]
    experiment = CompareDataQuality(*fp)
    experiment.init()
    for _tc in tc:
        experiment.gen_data(_tc)
        experiment.do_experiment()


if __name__ == '__main__':
    setup_logging()
    main()
    logging.shutdown()
