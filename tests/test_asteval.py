from scripts.models.prism_utils.prism_bscc_parser import DeepRecursionCtx

import pytest

import sys
import math
from asteval import Interpreter


def test_eval():
    aeval = Interpreter()
    expr_str = "r[0]**4 * r[1]**2 +" * 10000 + '2*r[2]'
    with DeepRecursionCtx():
        expr = aeval.parse(expr_str)
        aeval.symtable['r'] = [1, 2, 3]
        res = aeval.eval(expr)
        assert not math.isnan(res)
