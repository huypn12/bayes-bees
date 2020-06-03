from models.data_model import DataModel
from models.prism_utils.prism_bscc_parser import PrismBsccParser
from models.prism_utils.prism_dtmc_parser import PrismDtmcParser

import numpy as np


class BeesModel(DataModel):
    def __init__(self):
        super().__init__()
        self.bscc_ast_pfuncs = None
        self.bscc_eval = None
        self.pmc = None

    @staticmethod
    def from_model_file(prism_model_filepath):
        pass

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

    def sample():
        pass