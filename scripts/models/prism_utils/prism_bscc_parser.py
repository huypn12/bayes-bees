from scripts import config

import sys
import threading
import re
import sympy
from asteval import Interpreter

import os
if os.name == 'posix':
    import resource
    resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))


class DeepRecursionCtx(object):
    kRecursionLimit = 10**4
    kThrStacksize = 2**29

    def __init__(self, ):
        self.old_recursion_limit = sys.getrecursionlimit()
        self.old_thr_stacksize = threading.stack_size()
        self.recursion_limit = DeepRecursionCtx.kRecursionLimit
        self.thr_stacksize = DeepRecursionCtx.kThrStacksize

    def __enter__(self):
        sys.setrecursionlimit(self.recursion_limit)
        threading.stack_size(self.thr_stacksize)

    def __exit__(self, type, value, tb):
        sys.setrecursionlimit(self.old_recursion_limit)
        threading.stack_size(self.old_thr_stacksize)


class PrismBsccParser(object):
    """
    PRISM model checker, symbolic model checking result interpretation
    into Python expressions
    """

    def __init__(self, prism_result_file):
        super().__init__()
        self.prism_result_file = prism_result_file
        self.bscc_labels = []
        self.bscc_str_pfuncs = []
        self.bscc_ast_pfuncs = []
        self.can_simplify = False
        self.params_count = 0

    def get_bscc_desc(self, ):
        return {
            'bscc_labels': self.bscc_labels,
            'bscc_ast_pfuncs': self.bscc_ast_pfuncs,
            'params_count': self.params_count
        }

    def process(self,):
        with DeepRecursionCtx():
            print(sys.getrecursionlimit())
            thr = threading.Thread(target=self._process)
            thr.start()
            thr.join()

    def _process(self,):
        with open(self.prism_result_file, "r") as fptr:
            lines = fptr.readlines()
        max_param_idx = 0
        aeval = Interpreter()
        for line in lines:
            if len(line) > 7:
                if line[0:6] == 'Result':
                    param_idx, bscc_str = self.process_result_line(line)
                    if param_idx > max_param_idx:
                        max_param_idx = param_idx
                    try:
                        bscc_expr = aeval.parse(bscc_str)
                    except Exception as ex:
                        raise(ex)
                        # sys.exit(ex)
                    self.bscc_str_pfuncs.append(bscc_str)
                    self.bscc_ast_pfuncs.append(bscc_expr)
                elif line[0:30] == 'Parametric model checking: P=?':
                    pattern = re.compile(r'\[ F (.*?)\]')
                    sbscc = re.search(pattern, line).group(1)
                    sbscc = sbscc.rstrip().lstrip()
                    bscc_label, _ = self.process_bscc_label(sbscc)
                    self.bscc_labels.append(bscc_label)
        self.params_count = max_param_idx + 1

    def process_bscc_label(self, sbscc):
        sbscc = sbscc.replace('(', '').replace(')', '')
        tokens = sbscc.split('&')
        is_bscc = False
        if 'b=1' in tokens:
            is_bscc = True
        bscc_label = ','.join(tokens)
        return bscc_label, is_bscc

    def process_result_line(self, line):
        res_str = line.split(':')[2].rstrip("\n").lstrip(" ")
        return self.process_bscc_str(res_str)

    def get_max_param_idx(self, pfunc_str):
        max_param_idx = 0
        pattern = re.compile(r"(r)\[(\d*)\]")
        for pp in re.finditer(pattern, pfunc_str):
            idx = int(pp.group(2))
            if idx > max_param_idx:
                max_param_idx = idx
        return max_param_idx

    def process_division(self, bscc_str):
        if '|' not in bscc_str:
            return bscc_str
        bscc_str = bscc_str.replace('|', r')/(')
        bscc_str = '({})'.format(bscc_str)
        return bscc_str

    def replace_ops(self, bscc_str):
        bscc_str = bscc_str.replace('{', r'(')
        bscc_str = bscc_str.replace('}', r')')
        bscc_str = bscc_str.replace('^', r'**')
        bscc_str = self.process_division(bscc_str)
        return bscc_str

    def replace_var_old_bees(self, bscc_str):
        bscc_str = bscc_str.replace('p', r'p[0]')
        bscc_str = re.sub(r'([q])(\d*)',
                          lambda match: 'p' + '[' + str(int(match.group(2))) + ']', bscc_str)
        return bscc_str

    def replace_var(self, bscc_str):
        if config.models['use_old_model']:
            return self.replace_var_old_bees(bscc_str)
        bscc_str = re.sub(r'([r])_(\d*)',
                          lambda match: 'r' + '[' + str(int(match.group(2))) + ']', bscc_str)
        return bscc_str

    def replace_implicit_ops(self, bscc_str):
        pattern = re.compile(r'(\d|\)) ([a-z])')
        bscc_str = pattern.sub(r"\1 * \2", bscc_str)
        return bscc_str

    def simplify(self, bscc_str):
        if self.can_simplify:
            return sympy.factor(bscc_str)
        return bscc_str

    def process_bscc_str(self, bscc_str):
        bscc_str = self.replace_ops(bscc_str)
        bscc_str = self.replace_implicit_ops(bscc_str)
        bscc_str = self.simplify(bscc_str)
        bscc_str = self.replace_var(bscc_str)
        param_idx = self.get_max_param_idx(bscc_str)
        return param_idx, bscc_str
