import sys
import re
from asteval import Interpreter


class PrismDtmcParser(object):
    def __init__(self, prism_model_file):
        super().__init__()
        self.prism_model_file = prism_model_file
        self.init_symbol = '3'
        self.init_state_label = None
        self.state_list = []
        self.edge_list = []
        self.bscc_list = []
        self.init_str_pfuncs = []
        self.init_ast_pfuncs = []
        self.trans_str_pfuncs = []
        self.trans_ast_pfuncs = []

    def get_pmc_desc(self,):
        return {
            'pinit': self.init_ast_pfuncs,
            'ptrans': self.trans_ast_pfuncs,
            'state_labels': self.state_list,
            'bscc_labels': self.bscc_list
        }

    def process(self,):
        self.extract_adj_list()
        self.build_init_vector()
        self.build_trans_matrix()
        self.parse_str2ast()

    def process_state_label(self, sstate):
        sstate = sstate.replace('(', '').replace(')', '')
        tokens = sstate.split('&')
        is_bscc = False
        if 'b=1' in tokens:
            is_bscc = True
        if not any('b' in t for t in tokens):
            tokens.append('b=0')
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
                        gcmd_str = gcmd_str[:i + j] + \
                            "$" + gcmd_str[i + j + 1:]
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
        ttokens = tokens[1].split('$')
        for i in range(0, len(ttokens)):
            next = ttokens[i].split(':')
            if len(next) == 1:  # bscc lines
                next_state_label, is_bscc = self.process_state_label(next[0])
                if is_bscc:  # redundant, just for clarity
                    self.state_list.append(next_state_label)
                    self.bscc_list.append(next_state_label)
                if state_label != next_state_label:
                    self.edge_list.append((state_label, next_state_label, '1'))
                continue
            expr_str = self.process_expression(next[0])
            next_state_label, _ = self.process_state_label(next[1])
            self.edge_list.append(
                (state_label, next_state_label, expr_str))


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

    def build_init_vector(self, ):
        init_state_label = None
        init_flag = '=' + self.init_symbol
        for state_label in self.state_list:
            tokens = state_label.split(',')[:-1] #except the b flag
            if all(init_flag in s for s in tokens):
                init_state_label = state_label
                break
        self.state_list.remove(init_state_label)
        self.init_str_pfuncs = ['0'] * len(self.state_list)
        # (a,b,p) means a-[p]->b
        for edge in self.edge_list:
            if edge[0] == init_state_label:
                i = self.state_list.index(edge[1])
                self.init_str_pfuncs[i] = edge[2]
        self.init_state_label = init_state_label


    def build_trans_matrix(self, ):
        self.trans_str_pfuncs = [
            ['0'] * len(self.state_list)
            for i in range(0, len(self.state_list))
        ]
        for bscc in self.bscc_list:
            i = self.state_list.index(bscc)
            self.trans_str_pfuncs[i][i] = '1'
        for edge in self.edge_list:
            curr = edge[0]
            if curr == self.init_state_label:
                continue
            i = self.state_list.index(curr)
            nextt = edge[1]
            j = self.state_list.index(nextt)
            self.trans_str_pfuncs[i][j] = edge[2]


    def parse_str2ast(self, ):
        aeval = Interpreter()
        # Parse init vector to AST expressions
        state_count = len(self.state_list)
        self.init_ast_pfuncs = [None] * state_count
        for i, s in enumerate(self.init_str_pfuncs):
            self.init_ast_pfuncs[i] = aeval.parse(s)
        # Parse transition matrix to AST expressions
        self.trans_ast_pfuncs = [[None] * state_count for i in range(0, state_count)]
        for i in range(0, state_count):
            for j in range(0, state_count):
                self.trans_ast_pfuncs[i][j] = aeval.parse(
                    self.trans_str_pfuncs[i][j])


## UNIT TEST ##
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
    assert(state_label == 'a0=3,a1=3,a2=3,b=0')
    sstate = "(a0'=1) & (a1'=1) & (a2'=1)"
    sstate = parser.clean_gcommand_line(sstate)
    state_label, _ = parser.process_state_label(sstate)
    assert(state_label == 'a0=1,a1=1,a2=1,b=0')


def test_expr():
    parser = PrismDtmcParser("")
    expr_str = '3.0*r_0*r_0*(1-r_0)'
    assert(parser.process_expression(expr_str) == '3.0*r[0]*r[0]*(1-r[0])')


def test_extract_state():
    parser = PrismDtmcParser("bee_multiparam_synchronous_3.pm")
    parser.process()
    print('State list\n', parser.state_list)
    print('BSCC list\n', parser.bscc_list)
    for b in parser.bscc_list:
        assert(b in parser.state_list)
    print('Edge list:')
    for e in parser.edge_list:
        print(e)


def test_build_matrix():
    parser = PrismDtmcParser("bee_multiparam_synchronous_3.pm")
    parser.process()
    print('Initial vector:')
    for iv in parser.init_str_pfuncs:
        print(iv)
    print('Transition matrix:')
    for row in parser.trans_str_pfuncs:
        print(row)


def main():
    test_gcmd_cleanup()
    test_state_label()
    test_expr()
    test_extract_state()
    test_build_matrix()


if __name__ == "__main__":
    sys.exit(main())
