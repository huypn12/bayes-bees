from .data_model import DataModel
from .prism_utils.prism_bscc_parser import PrismBsccParser
from .prism_utils.prism_dtmc_parser import PrismDtmcParser

import numpy as np


class BeesModel(DataModel):
    def __init__(self):
        super().__init__()
        self.trans_ast_pfuncs = None
        self.init_ast_pfuncs = None    
        self.bscc_ast_pfuncs = None
        self.bscc_eval = None
        self.pmc = None

    @staticmethod
    def from_model_file(prism_model_filepath):
        parser = PrismBsccParser(prism_model_filepath)
        parser.process()
        

    @staticmethod
    def from_result_file(prism_result_filepath):
        parser = PrismBsccParser(prism_result_filepath)
        parser.process()
        self.bscc_ast_pfuncs = parser.bscc_ast_pfuncs

    @staticmethod
    def from_files(prism_result_filepath, prism_model_filepath):
        pass

    def simulate_bscc_pfuncs(self, p, data):
        pass

    def sample(self,):
        pass


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


def main():
    test_bscc_label_match()

if __name__ == "__main__":
    sys.exit(main())