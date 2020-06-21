import sys
from .data_model import DataModel
from .prism_utils.prism_bscc_parser import PrismBsccParser
from .prism_utils.prism_dtmc_parser import PrismDtmcParser

import numpy as np
from asteval import Interpreter


class BeesModel(DataModel):
    BSCC_CHAINRUN = 0
    BSCC_RFUNCS = 1


    def __init__(self):
        super().__init__()
        self.state_labels = None
        self.state_count = 0
        self.init_ast_pfuncs = None
        self.trans_ast_pfuncs = None
        self.bscc_labels = None
        self.bscc_ast_pfuncs = None
        self.bscc_count = 0
        self.is_evaluated = False
        self.bscc_eval = None
        self.init_eval = None
        self.trans_eval = None
        self.params_count = 0
        self.bscc_eval_mode = BSCC_CHAINRUN

    def get_params_count(self,):
        return self.params_count

    def get_bscc_count(self,):
        return self.bscc_count

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
        bees_model.state_count = len(pmc_desc['state_labels'])
        bees_model.init_ast_pfuncs = pmc_desc['init_ast_pfuncs']
        bees_model.init_eval = [0] * bees_model.state_count
        bees_model.trans_ast_pfuncs = pmc_desc['trans_ast_pfuncs']
        bees_model.trans_eval = [
            [0] * bees_model.state_count
            for i in range(0, bees_model.state_count)
        ]
        bees_model.bscc_labels = bscc_desc['bscc_labels']
        bees_model.bscc_ast_pfuncs = bscc_desc['bscc_ast_pfuncs']
        bees_model.bscc_count = len(bscc_desc['bscc_labels'])
        bees_model.params_count = bscc_desc['params_count']
        return bees_model

    def eval_bscc_pfuncs(self, r):
        aeval = Interpreter()
        aeval.symtable['r'] = r
        return [aeval.run(f) for f in self.bscc_ast_pfuncs]

    def eval_bscc_sample(self, runs_count):
        pass

    
    def eval_bscc(self, chain_params=None, runs_count=None):
        if self.bscc_eval_mode == BeesModel.BSCC_RFUNCS:
            assert(chain_params != None)
            return self.eval_bscc_pfuncs(chain_params)
        return self.eval_bscc_sample(runs_count)

    def sample(self, params, trials_count: int = 1000):
        # Sampling given BSCC functions
        P = self.eval_bscc_pfuncs(params)
        self.bscc_eval = P
        bins_count = len(P)
        categorical = np.random.choice(bins_count, trials_count, p=P)
        multinomial = [0] * bins_count
        for it in categorical:
            multinomial[it] += 1
        norm = sum(multinomial) * 1.0
        frequency = [v / norm for v in multinomial]
        return (categorical, multinomial, frequency)

    def eval_pmc_pfuncs(self, r):
        aeval = Interpreter()
        aeval.symtable['r'] = r
        for i in range(0, self.state_count):
            self.init_eval[i] = aeval.run(self.init_ast_pfuncs[i])
        for i in range(0, self.state_count):
            for j in range(0, self.state_count):
                self.trans_eval[i][j] = aeval.run(self.trans_ast_pfuncs[i][j])

    def run_chain(self, max_steps=100):
        bscc_label = ''
        bscc_idx = -1
        curr_state_idx = np.random.choice(self.state_count, 1, p=self.init_eval)[0]
        for i in range(0, max_steps):
            label = self.state_labels[curr_state_idx]
            if label in self.bscc_labels:
                bscc_label = label
                bscc_idx = self.bscc_labels.index(label)
                break
            p_next = self.trans_eval[curr_state_idx]
            curr_state_idx = np.random.choice(self.state_count, 1, p=p_next)[0]
        return bscc_label, bscc_idx

    def sample_run_chain(self, r, max_trials):
        # Sampling by running the parametric chain
        self.eval_pmc_pfuncs(r)
        bins = [0] * self.bscc_count
        for i in range(0, max_trials):
            try:
                label, idx = self.run_chain()
            except Exception as ex:
                print(self.init_eval)
                print(self.trans_eval)
            if idx == -1: # discard the run
                continue
            bins[idx] += 1
        norm = sum(bins) * 1.0
        hist = [c / norm for c in bins]
        return hist


## UNIT TEST ##
import sys, timeit

def test_bscc_label_match():
    dtmc_parser = PrismDtmcParser(
        'models/prism/bee_multiparam_synchronous_3.pm')
    bscc_parser = PrismBsccParser(
        'models/prism/bee_multiparam_synchronous_3.txt')
    dtmc_parser.process()
    bscc_parser.process()
    pmc = dtmc_parser.get_pmc_desc()
    bscc = bscc_parser.get_bscc_desc()
    # size matching
    assert(len(pmc['bscc_labels']) == len(bscc['bscc_labels']))
    # index matching
    for i in range(0, len(pmc['bscc_labels'])):
        assert(pmc['bscc_labels'][i] == bscc['bscc_labels'][i])


def test_static_ctor():
    dtmc_filepath = 'models/prism/bee_multiparam_synchronous_3.pm'
    bscc_filepath = 'models/prism/bee_multiparam_synchronous_3.txt'
    bees_model = BeesModel.from_files(dtmc_filepath, bscc_filepath)
    assert(len(bees_model.state_labels) == 11)
    assert(len(bees_model.init_ast_pfuncs) == 11)
    assert(len(bees_model.trans_ast_pfuncs) == 11)
    assert(len(bees_model.bscc_labels) == 4)
    assert(len(bees_model.bscc_ast_pfuncs) == 4)


def test_bscc_sample():
    dtmc_filepath = 'models/prism/bee_multiparam_synchronous_3.pm'
    bscc_filepath = 'models/prism/bee_multiparam_synchronous_3.txt'
    bees_model = BeesModel.from_files(dtmc_filepath, bscc_filepath)
    (s, m, f) = bees_model.sample(
        params=[0.1, 0.2, 0.3],
        trials_count=10000
    )
    print('Sampling with BSCC rational function.')
    start_time = timeit.default_timer()
    bscc_eval = bees_model.eval_bscc_pfuncs([0.1, 0.2, 0.3])
    stop_time = timeit.default_timer()
    print('Finished evaluation in {} seconds'.format(
        stop_time - start_time))
    print("\tSimplex assert:    {}".format(
        np.sum(bscc_eval)))
    print("\tSample categorical {}".format(s))
    print("\tSample multinomial {}".format(m))
    print("\tSample frequency   {}".format(f))

def test_chain_run():
    print('Sampling with chain run')
    dtmc_filepath = 'models/prism/bee_multiparam_synchronous_3.pm'
    bscc_filepath = 'models/prism/bee_multiparam_synchronous_3.txt'
    bees_model = BeesModel.from_files(dtmc_filepath, bscc_filepath)
    r = [0.1, 0.2, 0.3]
    start_time = timeit.default_timer()
    h = bees_model.sample_run_chain(r, max_trials=1000)
    stop_time = timeit.default_timer()
    print('Finished in {} seconds, chain length {}'.format(
        stop_time - start_time, 1000))
    assert(sum(h) - 1.0 < 1e-5)
    print('\tSample frequency:', h)

def main():
    test_bscc_label_match()
    test_static_ctor()
    test_bscc_sample()
    test_chain_run()

if __name__ == "__main__":
    sys.exit(main())
