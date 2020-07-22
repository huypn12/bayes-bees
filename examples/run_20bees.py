import logging
import datetime
import timeit
from sklearn.metrics import mean_squared_error
from math import sqrt

from scripts import config
from scripts.bayesian_mcmc import BayesianMcmc
from scripts.models.bees_model import BeesModel
from examples.base_experiment import BaseExperiment


def setup_logging():
    now_str = str(datetime.datetime.now()).replace(' ', '_')
    filename = 'run_20bees_' + now_str + '.log'
    logfile = 'examples/logs/{}'.format(filename)
    logging.basicConfig(level=logging.DEBUG, filename=logfile)


class TwentyBees(BaseExperiment):
    def __init__(self, model_file):
        self.model_file = model_file
        config.models['use_uniform_prior'] = True
        config.models['use_sympy'] = True
        config.models['use_bounded_run'] = True

    # overriden
    def print_log(self, mesg):
        logging.info(mesg)

    # overriden
    def load_files(self, ):
        self.data_model = BeesModel.from_model_file(self.model_file)
        assert self.data_model.bscc_eval_mode == BeesModel.BSCC_MODE_CHAIN_RUN
        self.print_log("Loaded model file: {}".format(self.model_file))
        self.print_log(len(self.data_model.state_labels))
        self.print_log(len(self.data_model.bscc_labels))

    def init(self, ):
        self.load_files()
        self.gen_p_true()
        self.p_true = [
            0.012, 0.023, 0.032, 0.045, 0.051,
            0.132, 0.156, 0.197, 0.221, 0.251,
            0.372, 0.395, 0.461, 0.491, 0.512,
            0.589, 0.678, 0.691, 0.732, 0.752
        ]
        self.print_log('True parameter: {}'.format(self.p_true))
        self.synthesize_data()

    def do_experiment(self, ):
        self.init()
        mcmc = BayesianMcmc(self.data_model)
        mcmc.data_model.chainruns_count = 1000
        mcmc.mh_params['chain_length'] = 250
        self.print_log('Start inferencing, MCMC chain len {}'.format(1000))
        m = self.syn_data['mult']
        # start inferencing
        start_time = timeit.default_timer()
        mcmc.estimate_p(m)
        stop_time = timeit.default_timer()
        self.print_log('MCMC estimation, ETA(secs) {}'.format(stop_time - start_time))
        print(mcmc.estimated_params['P'])
        rmse = sqrt(mean_squared_error(self.p_true, mcmc.estimated_params['P']))
        self.print_log('RMSE {}'.format(rmse))
        self.print_log(mcmc.summarize())


def main():
    model_file = 'data/prism/bee_multiparam_synchronous_20.pm'
    experiment = TwentyBees(model_file)
    while True:
        try:
            experiment.do_experiment()
        except Exception as ex:
            print(ex)
            continue


if __name__ == '__main__':
    setup_logging()
    main()
    logging.shutdown()
