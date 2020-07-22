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
    filename = 'run_normal_' + now_str + '.log'
    logfile = 'examples/logs/{}'.format(filename)
    logging.basicConfig(level=logging.DEBUG, filename=logfile)


gUseChainRun = False


class RunNormal(BaseExperiment):
    def __init__(self, model_file, bscc_file):
        super().__init__(model_file, bscc_file)
        config.models['use_sympy'] = False
        config.models['use_uniform_prior'] = True

    def print_log(self, mesg):
        logging.info(mesg)

    def init(self,):
        super().load_files()
        super().gen_p_true()
        super().synthesize_data()

    def do_experiment_pfuncs(self,):
        self.print_log('PFUNCS MODE')
        self.data_model.bscc_eval_mode = BeesModel.BSCC_MODE_PFUNCS
        mcmc = BayesianMcmc(self.data_model)
        mcmc_chainlen = 500
        mcmc.mh_params['chain_length'] = mcmc_chainlen
        self.print_log('Start inferencing, MCMC chain len {}'.format(mcmc_chainlen))
        m = self.syn_data['mult']
        start_time = timeit.default_timer()
        mcmc.estimate_p(m)
        stop_time = timeit.default_timer()
        self.print_log('MCMC estimation, ETA(secs) {}'.format(stop_time - start_time))
        print(mcmc.estimated_params['P'])
        _rmse = rmse(self.p_true, mcmc.estimated_params['P'])
        self.print_log('RMSE {}'.format(_rmse))
        self.print_log(mcmc.summarize())

    def do_experiment_sim(self, ):
        self.print_log('DTMC SAMPLING MODE')
        self.data_model.bscc_eval_mode = BeesModel.BSCC_MODE_CHAIN_RUN
        self.data_model.chainruns_count = 1000
        mcmc = BayesianMcmc(self.data_model)
        mcmc_chainlen = 500
        mcmc.mh_params['chain_length'] = mcmc_chainlen
        self.print_log('Start inferencing, MCMC chain len {}'.format(mcmc_chainlen))
        m = self.syn_data['mult']
        start_time = timeit.default_timer()
        mcmc.estimate_p(m)
        stop_time = timeit.default_timer()
        self.print_log('MCMC estimation, ETA(secs) {}'.format(stop_time - start_time))
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
    for fp in file_pairs:
        experiment = RunNormal(*fp)
        experiment.init()
        experiment.do_experiment_pfuncs()
        experiment.do_experiment_sim()


def manual():
    fp = ('data/prism/bee_multiparam_synchronous_15.pm',
          'data/prism/bee_multiparam_synchronous_15.txt')
    experiment = RunNormal(*fp)
    experiment.init()
    experiment.p_true = [
        0.00356327975634263, 0.012762721458134396, 0.019079006325324,
        0.19381550281284, 0.37313840781833507, 0.569942814556756,
        0.6369906204548853, 0.7112844933684676, 0.7293173054153359,
        0.7461703706617847, 0.776667630517512, 0.7925775383081012,
        0.8337539922976562, 0.839744827603057, 0.8482724116142761]
    experiment.syn_data = {
        'mult': [9473, 447, 68, 3, 1, 0, 0, 0, 0, 0, 1, 0, 0, 3, 3, 1],
        'dist': [0.9473, 0.0447, 0.0068, 0.0003, 0.0001, 0.0, 0.0, 0.0,
                 0.0, 0.0, 0.0001, 0.0, 0.0, 0.0003, 0.0003, 0.0001]
    }
    logging.info('----------------MANUAL RUN--------------------')
    logging.info('True params: {}'.format(experiment.p_true))
    logging.info('Data, m: {}'.format(experiment.syn_data['mult']))
    logging.info('Data, d: {}'.format(experiment.syn_data['dist']))
    experiment.do_experiment_sim()


if __name__ == '__main__':
    setup_logging()
    manual()
    logging.shutdown()
