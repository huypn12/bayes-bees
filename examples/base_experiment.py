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

    def gen_p_true(self):
        dim = self.data_model.get_params_count()
        p = [random.uniform(0, 1) for i in range(0, dim)]
        if not config.models['use_old_model']:
            p = sorted(p)
        self.p_true = p

    def synthesize_data(self, trials_count=10000):
        self.gen_p_true()
        m, d = self.data_model.sample(params=self.p_true,
                                      trials_count=trials_count)
        self.print_log("Data multinomial: {}".format(m))
        self.print_log("Data histogram: {}".format(d))

    def print_log(self, mesg):
        # @override
        print(mesg)

