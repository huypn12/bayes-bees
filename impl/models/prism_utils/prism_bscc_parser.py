import re
from asteval import Interpreter


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
        self.params_count = 0 


    def get_bscc_desc(self, ):
        return {
            'bscc_labels': self.bscc_labels,
            'bscc_ast_pfuncs': self.bscc_ast_pfuncs,
            'params_count': self.params_count
        }


    def process(self,):
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
                    bscc_expr = aeval.parse(bscc_str)
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
        pattern = re.compile("(r)\[(\d*)\]")
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


    def replace_var(self, bscc_str):
        # adapted to new model r_0, ..., r_n
        #bscc_str = bscc_str.replace('p', r'p[0]')
        pattern = re.compile(r'([r])_(\d*)')
        bscc_str = pattern.sub(r"r[\2]", bscc_str)
        return bscc_str


    def replace_implicit_op(self, bscc_str):
        pattern = re.compile(r'(\d|\)) ([a-z])')
        bscc_str = pattern.sub(r"\1 * \2", bscc_str)
        return bscc_str


    def process_bscc_str(self, bscc_str):
        bscc_str = self.replace_ops(bscc_str)
        bscc_str = self.replace_var(bscc_str)
        bscc_str = self.replace_implicit_op(bscc_str)
        param_idx = self.get_max_param_idx(bscc_str)
        return param_idx, bscc_str
    

## UNIT TEST ##
import resource, sys 
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(10**9)

def eval_bscc_ast_pfuncs(bscc_ast_pfuncs, r):
    aeval = Interpreter()
    aeval.symtable['r'] = r
    return [aeval.run(f) for f in bscc_ast_pfuncs]

def test_15bees():
    parser = PrismBsccParser("bee_multiparam_synchronous_15.txt")
    parser.process()
    bscc_ast_pfuncs = parser.bscc_ast_pfuncs
    bscc_str_pfuncs = parser.bscc_str_pfuncs
    print(parser.params_count)
    r = [
        0.01, 0.02, 0.03, 0.04, 0.05,
        0.06, 0.07, 0.08, 0.09, 0.1,
        0.11, 0.12, 0.13, 0.14, 0.15
    ]
    eval_bscc = eval_bscc_ast_pfuncs(bscc_ast_pfuncs, r)
    print(eval_bscc)

def test_stress():
    parser = PrismBsccParser("synchronous_40.txt")
    try:
        parser.process()
    except Exception as ex:
        raise ex
    bscc_ast_pfuncs = parser.bscc_ast_pfuncs
    bscc_str_pfuncs = parser.bscc_str_pfuncs
    print(bscc_str_pfuncs[0])
    aeval = Interpreter()
    aeval.symtable['p'] = 0.3
    aeval.symtable['q'] = 0.7
    for i in range(0, len(bscc_ast_pfuncs)):
        try:
            print(aeval.run(bscc_ast_pfuncs[i]))
        except Exception as ex:
            print(i)


def main():
    test_15bees()
    test_stress()

if __name__ == "__main__":
    sys.exit(main())


