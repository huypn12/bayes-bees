

# Input: a .txt PRISM result file
# Output: a 

bees_model_template = """

class Bees3(DataModel):
    def __init__(self):
        super().__init__()
        self.bscc_pfuncs = [
            lambda p: self.f_bscc_{}(p),
        ]

    def f_bscc_{}(self, p):
        pass

    def f_bscc_1(self, p):
        pass

    def f_bscc_2(self, p):
        pass
    
    def f_bscc_3(self, p):
        pass
    
    def f_bscc_4(self, p):
        pass

    def get_bscc_pfuncs(self, ):
        return self.bscc_pfuncs

    def eval_bscc_pfuncs(self, p):
        return [f(p) for f in self.bscc_pfuncs]

"""

class PrismResultParser(object):
    def __init__(self, file):
        super().__init__()

    def parse(self,):
        pass


