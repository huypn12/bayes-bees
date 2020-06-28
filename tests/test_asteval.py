import pytest
from asteval import Interpreter
import sys


class DeepRecursionCtx():
    kExtendedLimit = 10**9
    def __init__(self, ):
        self.limit = kExtendedLimit
        self.old_limit = sys.getrecursionlimit()

    def __enter__(self):
        sys.setrecursionlimit(self.limit)

    def __exit__(self, type, value, tb):
        sys.setrecursionlimit(self.old_limit)

def test_eval(expr_str):
    aeval = Interpreter()
    expr_str = "r[0]**4 * r[1]**2" + r[2]
    with DeepRecursionCtx:
        
         
