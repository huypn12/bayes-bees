from asteval import Interpreter

import sys

class RecursionLimit:
    def __init__(self, limit):
        self.limit = limit
        self.old_limit = sys.getrecursionlimit()

    def __enter__(self):
        sys.setrecursionlimit(self.limit)

    def __exit__(self, type, value, tb):
        sys.setrecursionlimit(self.old_limit)

def test_eval(expr_str):
    extended_rlimit = 10 ** 8
    with RecursionLimit(extended_rlimit):
         pass