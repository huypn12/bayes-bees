from scripts.models.bees_model import BeesModel
from scripts import config
import random


class BaseExperiment(object):
    def __init__(self, model_file, bscc_file):
        self.model_file = model_file
        self.bscc_file = bscc_file
        self.data_model = None
        self.p_true = None
        self.syn_data = None

    def load_files(self, ):
        self.data_model = BeesModel.from_files(self.model_file, self.bscc_file)
        assert self.data_model.bscc_eval_mode == BeesModel.BSCC_MODE_CHAIN_RUN
        self.print_log("Loaded model file: {}".format(self.model_file))
        self.print_log('Loaded BSCCs file: {}'.format(self.bscc_file))

    def gen_p_true(self):
        dim = self.data_model.get_params_count()
        p = [random.uniform(0, 1) for i in range(0, dim)]
        self.p_true = p if config.models['use_old_model'] else sorted(p)
        self.print_log('True parameter: {}'.format(self.p_true))

    def synthesize_data(self, trials_count=10000):
        m, d = self.data_model.sample(chain_params=self.p_true,
                                      trials_count=trials_count)
        self.syn_data = {
            'mult': m,
            'dist': d
        }
        self.print_log("Data multinomial: {}".format(m))
        self.print_log("Data histogram: {}".format(d))

    def set_syn_data(self, p_true, syn_data):
        self.p_true = p_true
        self.syn_data = syn_data

    def print_log(self, mesg):
        # @override
        print(mesg)
