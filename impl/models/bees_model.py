from .data_model import DataModel
from .prism_utils.prism_bscc_parser import PrismBsccParser
from .prism_utils.prism_dtmc_parser import PrismDtmcParser

import numpy as np
from asteval import Interpreter


class BeesModel(DataModel):
    def __init__(self):
        super().__init__()
        self.aeval = Interpreter()
        self.state_labels = None
        self.init_ast_pfuncs = None    
        self.trans_ast_pfuncs = None
        self.bscc_labels = None
        self.bscc_ast_pfuncs = None
        self.is_evaluated = False
        self.bscc_eval = None
        self.init_eval = None
        self.trans_eval = None
        self.params_count = 0
        

    def get_params_count(self,):
        return self.params_count


    def get_bscc_pfuncs(self, ):
        return self.bscc_ast_pfuncs


    @staticmethod
    def from_model_file(prism_model_filepath):
        parser = PrismDtmcParser(prism_model_filepath)
        parser.process()
        return parser.get_pmc_desc()
        

    @staticmethod
    def from_result_file(prism_result_filepath):
        parser = PrismBsccParser(prism_result_filepath)
        parser.process()
        return parser.get_bscc_desc()


    @staticmethod
    def from_files(prism_model_filepath, prism_result_filepath):
        pmc_desc = BeesModel.from_model_file(prism_model_filepath)
        bscc_desc = BeesModel.from_result_file(prism_result_filepath)
        bees_model = BeesModel()
        bees_model.state_labels = pmc_desc['state_labels']
        bees_model.init_ast_pfuncs = pmc_desc['init_ast_pfuncs']
        bees_model.trans_ast_pfuncs = pmc_desc['trans_ast_pfuncs']
        bees_model.bscc_labels = bscc_desc['bscc_labels']
        bees_model.bscc_ast_pfuncs = bscc_desc['bscc_ast_pfuncs']
        return bees_model

    def eval_bscc_pfuncs(self, p):
        self.aeval.symtable['r'] = p
        return [aeval.run(p) for f in self.bscc_pfuncs]


    def sample(self, params, trials_count: int = 1000):
        # Sampling given BSCC functions
        P = self.eval_bscc_pfuncs(params)
        bins_count = len(P)
        categorical = np.random.choice(bins_count, trials_count, p=P)
        multinomial = [0] * bins_count
        for it in categorical:
            multinomial[it] += 1
        norm = sum(multinomial) * 1.0
        frequency = [v / norm for v in multinomial]
        return (categorical, multinomial, frequency)


    def run_chain(self, ):
        pass


    def sample_run_chain(self, p):
        # Sampling by running the parametric chain
        assert(is_evaluated)

## UNIT TEST ##
import sys

def test_bscc_label_match():
    dtmc_parser = PrismDtmcParser('models/prism_utils/bee_multiparam_synchronous_3.pm')
    bscc_parser = PrismBsccParser('models/prism_utils/bee_multiparam_synchronous_3.txt')
    dtmc_parser.process()
    bscc_parser.process()
    pmc = dtmc_parser.get_pmc_desc()
    bscc = bscc_parser.get_bscc_desc()
    #size matching
    assert(len(pmc['bscc_labels']) == len(bscc['bscc_labels']))
    #index matching
    for i in range(0, len(pmc['bscc_labels'])):
        assert(pmc['bscc_labels'][i] == bscc['bscc_labels'][i])


def test_static_ctor():
    dtmc_filepath = 'models/prism_utils/bee_multiparam_synchronous_3.pm'
    bscc_filepath = 'models/prism_utils/bee_multiparam_synchronous_3.txt'
    bees_model = BeesModel.from_files(dtmc_filepath, bscc_filepath)
    assert(len(bees_model.state_labels) == 11)
    assert(len(bees_model.init_ast_pfuncs) == 11)
    assert(len(bees_model.trans_ast_pfuncs) == 11)
    assert(len(bees_model.bscc_labels) == 4)
    assert(len(bees_model.bscc_ast_pfuncs) == 4)


def test_bscc_sample():
    dtmc_filepath = 'models/prism_utils/bee_multiparam_synchronous_3.pm'
    bscc_filepath = 'models/prism_utils/bee_multiparam_synchronous_3.txt'
    bees_model = BeesModel.from_files(dtmc_filepath, bscc_filepath)
    (s, m, f) = bees_model.sample(
        params=[0.1, 0.2, 0.3],
        trials_count=10000
        )
    print("Simplex assert:    {}".format(np.sum(bees_model.eval_bscc_pfuncs([0.1, 0.2, 0.3]))))
    print("Sample categorical {}".format(s))
    print("Sample multinomial {}".format(m))
    print("Sample frequency   {}".format(f))


def main():
    test_bscc_label_match()
    test_static_ctor()

if __name__ == "__main__":
    sys.exit(main())