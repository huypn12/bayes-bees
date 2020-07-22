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
from asteval import Interpreter


def setup_logging():
    now_str = str(datetime.datetime.now()).replace(' ', '_')
    filename = 'run_oldmodels_' + now_str + '.log'
    logfile = 'examples/logs/{}'.format(filename)
    logging.basicConfig(level=logging.DEBUG, filename=logfile)


class RunOldBees(BaseExperiment):
    def __init__(self, model_file, bscc_file):
        super().__init__(model_file, bscc_file)

    def init(self, ):
        config.models['use_old_model'] = True
        super().load_files()
        self.data_model.bscc_eval_mode = BeesModel.BSCC_MODE_PFUNCS
        print(self.data_model.bscc_eval)
        super().gen_p_true()
        super().synthesize_data()

    def print_log(self, mesg):
        logging.info(mesg)

    def create_model(self, ):
        mcmc = BayesianMcmc(self.data_model)
        mcmc.hyperparams['alpha'] = 2
        mcmc.hyperparams['beta'] = 5
        mcmc.mh_params['chain_length'] = 2000
        mcmc.data_model.bscc_eval_mode = BeesModel.BSCC_MODE_PFUNCS
        return mcmc

    def run_inference(self,):
        self.print_log('Start inferencing')
        m = self.syn_data['mult']
        start_time = timeit.default_timer()
        mcmc = self.create_model()
        mcmc.estimate_p(m)
        stop_time = timeit.default_timer()
        self.print_log('Finish inferencing,ETA(secs) {}'.format(
            stop_time - start_time))
        print('Estimated params: P={}'.format(mcmc.estimated_params['P']))
        print('True params: P_true={}'.format(self.p_true))
        rmse = sqrt(mean_squared_error(self.p_true,
                                       mcmc.estimated_params['P']))
        self.print_log('RMSE {}'.format(rmse))
        self.print_log('Inference summary')
        self.print_log(mcmc.summarize())

    def do_experiment(self, ):
        self.init()
        self.run_inference()


def main():
    file_pairs = [
        ('data/prism/multiparam_synchronous_3.pm',
         'data/prism/multiparam_synchronous_3.txt'),
        ('data/prism/multiparam_synchronous_10.pm',
         'data/prism/multiparam_synchronous_10.txt'),
        ('data/prism/synchronous_10.pm',
         'data/prism/synchronous_10.txt'),
    ]
    for model_file, bscc_file in file_pairs:
        experiment = RunOldBees(model_file, bscc_file)
        experiment.do_experiment()


if __name__ == "__main__":
    setup_logging()
    main()
    logging.shutdown()
