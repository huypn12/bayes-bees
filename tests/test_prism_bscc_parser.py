from scripts.models.prism_utils.prism_bscc_parser import PrismBsccParser

import numpy as np
from asteval import Interpreter
import pytest


@pytest.fixture
def parser():
    parser = PrismBsccParser("data/prism/bee_multiparam_synchronous_10.txt")
    try:
        parser.process()
    except Exception as ex:
        raise ex
    return parser


@pytest.fixture
def sparser():
    parser = PrismBsccParser("data/prism/synchronous_40.txt")
    try:
        parser.process()
    except Exception as ex:
        raise ex
    return parser


def test_10bees(parser):
    bscc_ast_pfuncs = parser.bscc_ast_pfuncs
    bscc_str_pfuncs = parser.bscc_str_pfuncs
    for f in bscc_str_pfuncs:
        assert f is not None
        assert len(f) != 0
    r = [
        0.01, 0.02, 0.03, 0.04, 0.05,
        0.06, 0.07, 0.08, 0.09, 0.1,
        0.11, 0.12, 0.13, 0.14, 0.15
    ]
    aeval = Interpreter()
    aeval.symtable['r'] = r
    eval_bscc = [aeval.run(f) for f in bscc_ast_pfuncs]
    assert not np.isnan(np.sum(eval_bscc))


def test_stress(sparser):
    bscc_ast_pfuncs = sparser.bscc_ast_pfuncs
    bscc_str_pfuncs = sparser.bscc_str_pfuncs
    for f in bscc_str_pfuncs:
        assert f is not None
        assert len(f) != 0
    aeval = Interpreter()
    aeval.symtable['p'] = 0.3
    aeval.symtable['q'] = 0.7
    for i in range(0, len(bscc_ast_pfuncs)):
        try:
            val = aeval.run(bscc_ast_pfuncs[i])
        except Exception as ex:
            raise ex
        assert not np.isnan(val)

