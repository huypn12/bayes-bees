from .data_model import DataModel
from .prism_utils.prism_bscc_parser import PrismBsccParser
from .prism_utils.prism_dtmc_parser import PrismDtmcParser
from scripts import config

import math
import multiprocessing as mp
import numpy as np
from asteval import Interpreter


class BeesModel(DataModel):

    BSCC_MODE_CHAIN_RUN = 0
    BSCC_MODE_PFUNCS = 1

    def __init__(self):
        super().__init__()
        self.state_labels = None
        self.state_count = 0
        self.params = None
        self.params_count = 0
        self.is_params_increasing = True
        self.init_ast_pfuncs = None
        self.trans_ast_pfuncs = None
        self.bscc_labels = None
        self.bscc_ast_pfuncs = None
        self.bscc_count = 0
        self.is_evaluated = False
        self.bscc_eval = None
        self.init_eval = None
        self.trans_eval = None
        self.bscc_eval_mode = BeesModel.BSCC_MODE_CHAIN_RUN
        self.chainruns_count = config.models['chainruns_factor']

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
        bees_model.chainruns_count = config.models['chainruns_factor'] * bees_model.bscc_count
        return bees_model

    def get_params(self, ):
        return self.params

    def set_params(self, chain_params):
        self.params = chain_params

    def get_params_count(self,):
        return self.params_count

    def get_bscc_count(self,):
        return self.bscc_count

    def get_bscc_pfuncs(self, ):
        return self.bscc_ast_pfuncs

    def set_chainruns_count(self, c):
        self.chainruns_count = c

    def eval_bscc_pfuncs(self,):
        aeval = Interpreter()
        if config.models['use_old_model']:
            aeval.symtable['p'] = self.params
        else:
            aeval.symtable['r'] = self.params
        return [aeval.run(f) for f in self.bscc_ast_pfuncs]

    def eval_bscc(self, chain_params):
        self.set_params(chain_params)
        bscc_dist = None
        if self.bscc_eval_mode == BeesModel.BSCC_MODE_PFUNCS:
            bscc_dist = self.eval_bscc_pfuncs()
        else:
            _, bscc_dist = self.eval_bscc_chainrun()
        self.bscc_eval = bscc_dist
        return bscc_dist

    def sample_bscc_pfuncs(self, trials_count=1000):
        bins_count = len(self.bscc_eval)
        categorical = np.random.choice(bins_count,
                                       trials_count,
                                       p=self.bscc_eval)
        multinomial = [0] * bins_count
        for it in categorical:
            multinomial[it] += 1
        norm = sum(multinomial) * 1.0
        dist = [v / norm for v in multinomial]
        return (multinomial, dist)

    def eval_pmc_pfuncs(self, ):
        aeval = Interpreter()
        if config.models['use_old_model']:
            aeval.symtable['p'] = self.params
        else:
            aeval.symtable['r'] = self.params
        for i in range(0, self.state_count):
            self.init_eval[i] = aeval.run(self.init_ast_pfuncs[i])
        for i in range(0, self.state_count):
            for j in range(0, self.state_count):
                self.trans_eval[i][j] = aeval.run(self.trans_ast_pfuncs[i][j])

    def do_bounded_chainrun(self,):
        steps_count = math.ceil(math.log2(self.state_count)) + 5
        state_idx = np.random.choice(self.state_count, 1, p=self.init_eval)[0]
        for i in range(0, steps_count):
            p_next = self.trans_eval[state_idx]
            state_idx = np.random.choice(self.state_count, 1, p=p_next)[0]
        state_label = self.state_labels[state_idx]
        bscc_idx = self.bscc_labels.index(state_label)
        return bscc_idx

    def do_unbounded_chainrun(self,):
        bscc_idx = -1
        state_idx = np.random.choice(self.state_count, 1, p=self.init_eval)[0]
        max_steps = int(1e6)
        for i in range(0, max_steps):
            label = self.state_labels[state_idx]
            if label in self.bscc_labels:
                bscc_idx = self.bscc_labels.index(label)
                break
            p_next = self.trans_eval[state_idx]
            state_idx = np.random.choice(self.state_count, 1, p=p_next)[0]
        return bscc_idx

    def _do_task_chainrun(self, _count):
        multinomial = [0] * self.bscc_count
        for i in range(0, _count):
            # idx = self.do_unbounded_chainrun()
            idx = self.do_bounded_chainrun()
            multinomial[idx] += 1
        return multinomial

    def eval_bscc_chainrun(self,):
        # Sampling by running the parametric chain
        self.eval_pmc_pfuncs()
        multinomial = [0] * self.bscc_count
        """ sequential code
        for i in range(0, self.chainruns_count):
            idx = self.do_unbounded_chainrun()
            multinomial[idx] += 1
        """
        total, quant = self.chainruns_count, 500
        p, q = divmod(total, quant)
        tasks = [quant] * p + [q] if q != 0 else [quant] * p
        with mp.Pool(processes=(mp.cpu_count() + 1)) as ppool:
            results = ppool.map(self._do_task_chainrun, tasks)
            multinomial = [sum(x) for x in zip(*results)]
        norm = sum(multinomial) * 1.0
        dist = [c / norm for c in multinomial]
        return (multinomial, dist)

    def sample_bscc_chainrun(self, trials_count):
        self.chainruns_count = trials_count
        # For chainrun scheme:
        #   the evaluation itself contains a multinomial sample
        return self.eval_bscc_chainrun()

    def sample(self, chain_params, trials_count):
        sample = None
        self.set_params(chain_params)
        if self.bscc_eval_mode == BeesModel.BSCC_MODE_PFUNCS:
            self.eval_bscc(chain_params, trials_count)
            sample = self.sample_bscc_pfuncs(trials_count)
        else:
            sample = self.sample_bscc_chainrun(trials_count)
        return sample

    def summarize(self, ):
        summary = ''
        summary += 'Markov population model of: \n\t {} states \n\t {} BSCCs\n'.format(self.state_count, self.bscc_count)
        summary += 'P(BSCC) evaluation mode: ' + \
            ('Rational functions' if self.bscc_eval_mode == BeesModel.BSCC_MODE_PFUNCS else \
             'Chainrun of {} trials'.format(self.chainruns_count)) + '\n'
        return summary
