from scripts import config
from scripts.models.bees_model import BeesModel

from examples.base_experiment import BaseExperiment

import timeit
import datetime
import logging


def setup_logging():
    now_str = str(datetime.datetime.now()).replace(' ', '_')
    filename = 'compare_eval_methods' + now_str + '.log'
    logfile = 'examples/logs/{}'.format(filename)
    logging.basicConfig(level=logging.DEBUG, filename=logfile)


setup_logging()


class CompareEvals(BaseExperiment):
    def __init__(self, model_file, bscc_file):
        super().__init__(model_file, bscc_file)

    def init(self, ):
        start = timeit.default_timer()
        super().load_files()
        stop = timeit.default_timer()
        self.print_log('Parsing files, ETA {}'.format(stop - start))
        super().gen_p_true()

    def print_log(self, mesg):
        logging.info(mesg)

    def eval_pfuncs(self, ):
        assert self.data_model is not None
        self.data_model.bscc_eval_mode = BeesModel.BSCC_MODE_PFUNCS
        self.data_model.eval_bscc(self.p_true)

    def eval_chainrun(self, factor):
        assert self.data_model is not None
        self.data_model.bscc_eval_mode = BeesModel.BSCC_MODE_CHAIN_RUN
        self.data_model.chainruns_count = factor
        self.data_model.eval_bscc(self.p_true)

    def do_compare(self, ):
        self.init()
        self.print_log('P true: {}'.format(self.p_true))
        start = timeit.default_timer()
        self.eval_pfuncs()
        stop = timeit.default_timer()
        self.print_log('Rational functions, ETA {}'.format(stop - start))
        self.print_log('Rational functions evals to {}'.format(self.data_model.bscc_eval))
        chainruns = [2000, 4000, 8000, 10000]
        for c in chainruns:
            start = timeit.default_timer()
            self.eval_chainrun(c)
            stop = timeit.default_timer()
            self.print_log('#chainrun={} , ETA {}'.format(c, stop - start))
            self.print_log('Rational functions evals to {}'.format(self.data_model.bscc_eval))
        """
        start = timeit.default_timer()
        self.eval_chainrun(1000)
        stop = timeit.default_timer()
        self.print_log('#chainrun=1000, ETA {}'.format(stop - start))
        self.print_log('Rational functions evals to {}'.format(self.data_model.bscc_eval))
        """


def do_experiment():
    logging.info('COMPARISION OF BSCC EVALUATION TIME')
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
    for model_file, bscc_file in file_pairs:
        logging.info('Model file: ' + model_file)
        logging.info('BSCC file: ' + bscc_file)
        experiment = CompareEvals(model_file, bscc_file)
        experiment.init()
        experiment.do_compare()


if __name__ == '__main__':
    logging.info('EXPERIMENT SET, USING SYMPY: {}'.format(config.models['use_sympy']))
    do_experiment()
    config.models['use_sympy'] = True
    logging.info('EXPERIMENT SET, USING SYMPY: {}'.format(config.models['use_sympy']))
    do_experiment()
