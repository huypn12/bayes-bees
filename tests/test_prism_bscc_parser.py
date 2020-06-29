from scripts.models.prism_utils.prism_bscc_parser import PrismBsccParser

import numpy as np
from asteval import Interpreter
import pytest


@pytest.fixture
def parser():
    parser = PrismBsccParser("data/prism/bee_multiparam_synchronous_3.txt")
    return parser


def test_bscc_eval(parser):
    parser.process()
    bscc_ast_pfuncs = parser.bscc_ast_pfuncs
    bscc_str_pfuncs = parser.bscc_str_pfuncs
    assert len(bscc_ast_pfuncs) != 0
    assert len(bscc_str_pfuncs) != 0
    for f in bscc_str_pfuncs:
        assert f is not None
        assert len(f) != 0
    r = [0.11, 0.22, 0.33]
    aeval = Interpreter()
    aeval.symtable['r'] = r
    eval_bscc = [aeval.run(f) for f in bscc_ast_pfuncs]
    assert not np.isnan(np.sum(eval_bscc))
