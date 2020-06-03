import re
from asteval import Interpreter


class PrismDtmcParser(object):
    def __init__(self, prism_model_file):
        super().__init__()
        self.prism_model_file = prism_model_file
        self.state_list = []
        self.edge_list = []
        self.bscc_list = []


    def process(self,):
        self.extract_adj_list()


    def process_state_label(self, sstate):
        sstate = sstate.replace('(', '').replace(')', '')
        tokens = sstate.split('&')
        is_bscc = False
        if 'b=0' in tokens:
            tokens.remove('b=0')
        elif 'b=1' in tokens:
            tokens.remove('b=1')
            is_bscc = True
        state_label = ','.join(tokens)
        return state_label, is_bscc
    

    def process_expression(self, expr_str):
        pattern = re.compile(r'([r])_(\d*)')
        expr_str = pattern.sub(r"r[\2]", expr_str)
        return expr_str


    def replace_select_op(self, a_gcmd_str):
        # Replace '+' as successor state separation by '$' for easier parsing
        # since '+' is also used in symbolic expression
        gcmd_str = a_gcmd_str
        gcmd_str_end = len(gcmd_str) - 1
        i = 0
        while i <= gcmd_str_end:
            if gcmd_str[i] == ':':
                j = 1
                while i + j <= gcmd_str_end:
                    if gcmd_str[i + j] == "+":
                        gcmd_str = gcmd_str[:i + j] + "$" + gcmd_str[i + j + 1:] 
                        i += j
                        break
                    j += 1
            i += 1
        return gcmd_str


    def process_gcommand_line(self, gcmd_str):
        """
        [] a -> x : a' + y : a"
        """
        gcmd_str = self.clean_gcommand_line(gcmd_str)
        tokens = gcmd_str.split('->')
        sstate = tokens[0]
        state_label, is_bscc = self.process_state_label(sstate)
        if state_label not in self.state_list:
            self.state_list.append(state_label)
        for i in range(1, len(tokens)):
            ttokens = tokens[i].split('$')
            for ii in range(0, len(ttokens)):
                next = ttokens[ii].split(':')
                if len(next) == 1: #bscc lines
                    next_state_label, is_bscc = self.process_state_label(next[0])
                    if is_bscc: # redundant, just for clarity
                        self.bscc_list.append(next_state_label)
                    continue
                expr_str = self.process_expression(next[0])
                next_state_label , _= self.process_state_label(next[1])
                self.edge_list.append((state_label, next_state_label, expr_str))


    def clean_gcommand_line(self, gcmd_line):
        gcmd_line = self.replace_select_op(gcmd_line)
        gcmd_line = gcmd_line\
            .replace(';', '')\
            .replace('[]', '')\
            .replace('\'', '')\
            .replace(' ', '')
        return gcmd_line


    def extract_adj_list(self, ):
        lines = []
        with open(self.prism_model_file) as model_file:
            lines = model_file.readlines()
        adj_list = {}
        for line in lines:
            line = line.rstrip().lstrip()
            if line[0:2] == '[]':
                self.process_gcommand_line(line)


    def to_trans_matrix(self, adj_list):
        return []


## UNIT TEST ##
import sys 


def test_gcmd_cleanup():
    parser = PrismDtmcParser("")
    gcmd_str = """a0 = 3 & a1 = 3  & a2 = 3  & b = 0 -> 1.0*r_0*r_0*r_0: (a0'=1) & (a1'=1) & (a2'=1) + 3.0*r_0*r_0*(1-r_0): (a0'=1) & (a1'=1) & (a2'=0) + 3.0*r_0*(1-r_0)*(1-r_0): (a0'=1) & (a1'=0) & (a2'=0) + 1.0*(1-r_0)*(1-r_0)*(1-r_0): (a0'=0) & (a1'=0) & (a2'=0);"""
    gcmd_str = gcmd_str.rstrip().lstrip()
    gcmd_str = parser.clean_gcommand_line(gcmd_str)
    gcmd_str = parser.replace_select_op(gcmd_str)
    assert(gcmd_str == 'a0=3&a1=3&a2=3&b=0->1.0*r_0*r_0*r_0:(a0=1)&(a1=1)&(a2=1)$3.0*r_0*r_0*(1-r_0):(a0=1)&(a1=1)&(a2=0)$3.0*r_0*(1-r_0)*(1-r_0):(a0=1)&(a1=0)&(a2=0)$1.0*(1-r_0)*(1-r_0)*(1-r_0):(a0=0)&(a1=0)&(a2=0)')


def test_state_label():
    parser = PrismDtmcParser("")
    sstate = 'a0 = 3 & a1 = 3  & a2 = 3  & b = 0'
    sstate = parser.clean_gcommand_line(sstate)
    state_label, _ = parser.process_state_label(sstate)
    assert(state_label == 'a0=3,a1=3,a2=3')
    sstate = "(a0'=1) & (a1'=1) & (a2'=1)"
    sstate = parser.clean_gcommand_line(sstate)
    state_label, _ = parser.process_state_label(sstate)
    assert(state_label == 'a0=1,a1=1,a2=1')


def test_expr():
    parser = PrismDtmcParser("")
    expr_str = '3.0*r_0*r_0*(1-r_0)'
    assert(parser.process_expression(expr_str) == '3.0*r[0]*r[0]*(1-r[0])')


def test_extract_state():
    parser = PrismDtmcParser("bee_multiparam_synchronous_3.pm")
    parser.process()
    print(parser.state_list)
    print(parser.bscc_list)
    for b in parser.bscc_list:
        assert(b in parser.state_list)
    for e in parser.edge_list:
        print(e)

def main():
    test_gcmd_cleanup()
    test_state_label()
    test_expr()
    test_extract_state()


if __name__ == "__main__":
    sys.exit(main())