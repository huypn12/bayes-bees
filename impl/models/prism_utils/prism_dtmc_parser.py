# Input: prism dtmc GC model
# Output: transition matrix


class PrismDtmcParser(object):
    def __init__(self, prism_model_file):
        super().__init__()
        self.prism_model_file = prism_model_file

    def process(self,):
        adj_list = self.extract_adj_list()

    def process_state_label(self, sstate):
        tokens = sstate.split('&')
        is_bscc = False
        if 'b=0' in tokens:
            tokens.remove('b=0')
        elif 'b=1' in tokens:
            tokens.remove('b=1')
            is_bscc = True
        state_label = ','.join(tokens)
        return state_label, is_bscc


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
                        gcmd_str = gcmd_str[: i + j] + "$" + gcmd_str[i + j + 1 :] 
                        i += j
                        break
                    j += 1
            i += 1
        return gcmd_str

    def process_gcommand(self, gcmd_str):
        """
        [] a -> x : a' + y : a"
        """
        gcmd_str = self.clean_gcommand_line(gcmd_str)
        # get successor state name
        state_label, is_bscc = self.process_state_label(sstate)


    def clean_gcommand_line(self, gcmd_line):
        gcmd_line = self.replace_select_op(gcmd_line)
        gcmd_line = gcmd_line.replace('[]', '')
        gcmd_line = gcmd_line.replace('\'', '')
        gcmd_line = gcmd_line.replace(' ', '')
        return gcmd_line


    def extract_adj_list(self, ):
        lines = []
        with open(self.prism_model_file) as model_file:
            lines = model_file.readlines()
        adj_list = {}
        for line in lines:
            line = line.rstrip().lstrip()
            if line[0:1] == '[]':
                self.process_gcommand(line)

            pass

        return {}

    def to_trans_matrix(self, adj_list):
        return []


## UNIT TEST ##
import sys 


def test_process_gcmd():
    gcmd_str = """a0 = 3 & a1 = 3  & a2 = 3  & b = 0 -> 1.0*r_0*r_0*r_0: (a0'=1) & (a1'=1) & (a2'=1) + 3.0*r_0*r_0*(1-r_0): (a0'=1) & (a1'=1) & (a2'=0) + 3.0*r_0*(1-r_0)*(1-r_0): (a0'=1) & (a1'=0) & (a2'=0) + 1.0*(1-r_0)*(1-r_0)*(1-r_0): (a0'=0) & (a1'=0) & (a2'=0);"""
    parser = PrismDtmcParser("")
    gcmd_str = gcmd_str.rstrip().lstrip()
    gcmd_str = parser.replace_selection_token(gcmd_str)
    expected = """a0=3&a1 = 3&a2=3&b=0->1.0*r_0*r_0*r_0:a0=1&a1=1&a2=1$3.0*r_0*r_0*(1-r_0):a0=1&a1=1&a2=0$3.0*r_0*(1-r_0)*(1-r_0): (a0'=1) & (a1'=0) & (a2'=0) + 1.0*(1-r_0)*(1-r_0)*(1-r_0): (a0'=0) & (a1'=0) & (a2'=0);"""
    assert(gcmd_str == expected)

def main():
    test_process_gcmd()

if __name__ == "__main__":
    sys.exit(main())