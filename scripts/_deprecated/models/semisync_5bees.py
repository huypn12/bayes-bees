from .data_model import DataModel

import numpy as np

#### This code is generated by a script ####
class Semisync5bees(DataModel):
    def __init__(self):
        super().__init__()
        self.name = 'Semisynchronous, 5 bees, 5 params'
        self.params_count = 5
        self.bscc_pfuncs = [
            lambda p: self.f_bscc_0(p),
            lambda p: self.f_bscc_1(p),
            lambda p: self.f_bscc_2(p),
            lambda p: self.f_bscc_3(p),
            lambda p: self.f_bscc_4(p),
            lambda p: self.f_bscc_5(p)
        ]

    def get_name(self, ):
        return self.name

    def get_params_count(self):
        return self.params_count

    def get_bscc_pfuncs(self, ):
        return self.bscc_pfuncs

    def eval_bscc_pfuncs(self, p):
        return [f(p) for f in self.bscc_pfuncs]

    def sample(self, params, trials_count: int = 1000):
        """
        Sample by categorical distribution
        Later can be transformed into multinomial sample
        """
        P = self.eval_bscc_pfuncs(params)
        bins_count = len(P)
        categorical = np.random.choice(bins_count, trials_count, p=P)
        multinomial = [0] * bins_count
        for it in categorical:
            multinomial[it] += 1
        norm = sum(multinomial) * 1.0
        frequency = [v / norm for v in multinomial]
        return (categorical, multinomial, frequency)

    #### Parameterized P(BSCC i) ####
    def f_bscc_0(self, p):
        f = ( ( -1 ) * p[0]**5 + 5 * p[0]**4 - 10 * p[0]**3 + 10 * p[0]**2 - 5 * p[0] + 1  )
        return f

    def f_bscc_1(self, p):
        f = ( 5 * p[1]**4 * p[0]**5 - 20 * p[1]**3 * p[0]**5 - 20 * p[1]**4 * p[0]**4 + 30 * p[1]**2 * p[0]**5 + 80 * p[1]**3 * p[0]**4 + 30 * p[1]**4 * p[0]**3 - 20 * p[1] * p[0]**5 - 120 * p[1]**2 * p[0]**4 - 120 * p[1]**3 * p[0]**3 - 20 * p[1]**4 * p[0]**2 + 5 * p[0]**5 + 80 * p[1] * p[0]**4 + 180 * p[1]**2 * p[0]**3 + 80 * p[1]**3 * p[0]**2 + 5 * p[1]**4 * p[0] - 20 * p[0]**4 - 120 * p[1] * p[0]**3 - 120 * p[1]**2 * p[0]**2 - 20 * p[1]**3 * p[0] + 30 * p[0]**3 + 80 * p[1] * p[0]**2 + 30 * p[1]**2 * p[0] - 20 * p[0]**2 - 20 * p[1] * p[0] + 5 * p[0] )
        return f

    def f_bscc_2(self, p):
        f = ( ( -5 ) * p[1]**4 * p[0]**5 - 5 * p[2] * p[1]**3 * p[0]**5 - 5 * p[2]**2 * p[1]**2 * p[0]**5 - 5 * p[2]**3 * p[1] * p[0]**5 + 20 * p[1]**3 * p[0]**5 + 20 * p[2] * p[1]**2 * p[0]**5 + 20 * p[2]**2 * p[1] * p[0]**5 + 10 * p[2]**3 * p[0]**5 + 20 * p[1]**4 * p[0]**4 + 20 * p[2] * p[1]**3 * p[0]**4 + 20 * p[2]**2 * p[1]**2 * p[0]**4 + 20 * p[2]**3 * p[1] * p[0]**4 - 30 * p[1]**2 * p[0]**5 - 30 * p[2] * p[1] * p[0]**5 - 30 * p[2]**2 * p[0]**5 - 80 * p[1]**3 * p[0]**4 - 80 * p[2] * p[1]**2 * p[0]**4 - 80 * p[2]**2 * p[1] * p[0]**4 - 30 * p[2]**3 * p[0]**4 - 30 * p[1]**4 * p[0]**3 - 30 * p[2] * p[1]**3 * p[0]**3 - 30 * p[2]**2 * p[1]**2 * p[0]**3 - 30 * p[2]**3 * p[1] * p[0]**3 + 20 * p[1] * p[0]**5 + 30 * p[2] * p[0]**5 + 120 * p[1]**2 * p[0]**4 + 120 * p[2] * p[1] * p[0]**4 + 90 * p[2]**2 * p[0]**4 + 120 * p[1]**3 * p[0]**3 + 120 * p[2] * p[1]**2 * p[0]**3 + 120 * p[2]**2 * p[1] * p[0]**3 + 30 * p[2]**3 * p[0]**3 + 20 * p[1]**4 * p[0]**2 + 20 * p[2] * p[1]**3 * p[0]**2 + 20 * p[2]**2 * p[1]**2 * p[0]**2 + 20 * p[2]**3 * p[1] * p[0]**2 - 10 * p[0]**5 - 80 * p[1] * p[0]**4 - 90 * p[2] * p[0]**4 - 180 * p[1]**2 * p[0]**3 - 180 * p[2] * p[1] * p[0]**3 - 90 * p[2]**2 * p[0]**3 - 80 * p[1]**3 * p[0]**2 - 80 * p[2] * p[1]**2 * p[0]**2 - 80 * p[2]**2 * p[1] * p[0]**2 - 10 * p[2]**3 * p[0]**2 - 5 * p[1]**4 * p[0] - 5 * p[2] * p[1]**3 * p[0] - 5 * p[2]**2 * p[1]**2 * p[0] - 5 * p[2]**3 * p[1] * p[0] + 30 * p[0]**4 + 120 * p[1] * p[0]**3 + 90 * p[2] * p[0]**3 + 120 * p[1]**2 * p[0]**2 + 120 * p[2] * p[1] * p[0]**2 + 30 * p[2]**2 * p[0]**2 + 20 * p[1]**3 * p[0] + 20 * p[2] * p[1]**2 * p[0] + 20 * p[2]**2 * p[1] * p[0] - 30 * p[0]**3 - 80 * p[1] * p[0]**2 - 30 * p[2] * p[0]**2 - 30 * p[1]**2 * p[0] - 30 * p[2] * p[1] * p[0] + 10 * p[0]**2 + 20 * p[1] * p[0] )
        return f

    def f_bscc_3(self, p):
        f = ( 5 * p[2] * p[1]**3 * p[0]**5 + 5 * p[2]**2 * p[1]**2 * p[0]**5 + 5 * p[3] * p[2] * p[1]**2 * p[0]**5 + 5 * p[2]**3 * p[1] * p[0]**5 + 5 * p[3] * p[2]**2 * p[1] * p[0]**5 + 5 * p[3]**2 * p[2] * p[1] * p[0]**5 - 20 * p[2] * p[1]**2 * p[0]**5 - 20 * p[2]**2 * p[1] * p[0]**5 - 20 * p[3] * p[2] * p[1] * p[0]**5 - 10 * p[2]**3 * p[0]**5 - 10 * p[3] * p[2]**2 * p[0]**5 - 10 * p[3]**2 * p[2] * p[0]**5 - 20 * p[2] * p[1]**3 * p[0]**4 - 20 * p[2]**2 * p[1]**2 * p[0]**4 - 20 * p[3] * p[2] * p[1]**2 * p[0]**4 - 20 * p[2]**3 * p[1] * p[0]**4 - 20 * p[3] * p[2]**2 * p[1] * p[0]**4 - 20 * p[3]**2 * p[2] * p[1] * p[0]**4 + 30 * p[2] * p[1] * p[0]**5 + 30 * p[2]**2 * p[0]**5 + 30 * p[3] * p[2] * p[0]**5 + 10 * p[3]**2 * p[0]**5 + 80 * p[2] * p[1]**2 * p[0]**4 + 80 * p[2]**2 * p[1] * p[0]**4 + 80 * p[3] * p[2] * p[1] * p[0]**4 + 30 * p[2]**3 * p[0]**4 + 30 * p[3] * p[2]**2 * p[0]**4 + 30 * p[3]**2 * p[2] * p[0]**4 + 30 * p[2] * p[1]**3 * p[0]**3 + 30 * p[2]**2 * p[1]**2 * p[0]**3 + 30 * p[3] * p[2] * p[1]**2 * p[0]**3 + 30 * p[2]**3 * p[1] * p[0]**3 + 30 * p[3] * p[2]**2 * p[1] * p[0]**3 + 30 * p[3]**2 * p[2] * p[1] * p[0]**3 - 30 * p[2] * p[0]**5 - 20 * p[3] * p[0]**5 - 120 * p[2] * p[1] * p[0]**4 - 90 * p[2]**2 * p[0]**4 - 90 * p[3] * p[2] * p[0]**4 - 20 * p[3]**2 * p[0]**4 - 120 * p[2] * p[1]**2 * p[0]**3 - 120 * p[2]**2 * p[1] * p[0]**3 - 120 * p[3] * p[2] * p[1] * p[0]**3 - 30 * p[2]**3 * p[0]**3 - 30 * p[3] * p[2]**2 * p[0]**3 - 30 * p[3]**2 * p[2] * p[0]**3 - 20 * p[2] * p[1]**3 * p[0]**2 - 20 * p[2]**2 * p[1]**2 * p[0]**2 - 20 * p[3] * p[2] * p[1]**2 * p[0]**2 - 20 * p[2]**3 * p[1] * p[0]**2 - 20 * p[3] * p[2]**2 * p[1] * p[0]**2 - 20 * p[3]**2 * p[2] * p[1] * p[0]**2 + 10 * p[0]**5 + 90 * p[2] * p[0]**4 + 40 * p[3] * p[0]**4 + 180 * p[2] * p[1] * p[0]**3 + 90 * p[2]**2 * p[0]**3 + 90 * p[3] * p[2] * p[0]**3 + 10 * p[3]**2 * p[0]**3 + 80 * p[2] * p[1]**2 * p[0]**2 + 80 * p[2]**2 * p[1] * p[0]**2 + 80 * p[3] * p[2] * p[1] * p[0]**2 + 10 * p[2]**3 * p[0]**2 + 10 * p[3] * p[2]**2 * p[0]**2 + 10 * p[3]**2 * p[2] * p[0]**2 + 5 * p[2] * p[1]**3 * p[0] + 5 * p[2]**2 * p[1]**2 * p[0] + 5 * p[3] * p[2] * p[1]**2 * p[0] + 5 * p[2]**3 * p[1] * p[0] + 5 * p[3] * p[2]**2 * p[1] * p[0] + 5 * p[3]**2 * p[2] * p[1] * p[0] - 20 * p[0]**4 - 90 * p[2] * p[0]**3 - 20 * p[3] * p[0]**3 - 120 * p[2] * p[1] * p[0]**2 - 30 * p[2]**2 * p[0]**2 - 30 * p[3] * p[2] * p[0]**2 - 20 * p[2] * p[1]**2 * p[0] - 20 * p[2]**2 * p[1] * p[0] - 20 * p[3] * p[2] * p[1] * p[0] + 10 * p[0]**3 + 30 * p[2] * p[0]**2 + 30 * p[2] * p[1] * p[0] )
        return f

    def f_bscc_4(self, p):
        f = ( ( -5 ) * p[3] * p[2] * p[1]**2 * p[0]**5 - 5 * p[3] * p[2]**2 * p[1] * p[0]**5 - 5 * p[3]**2 * p[2] * p[1] * p[0]**5 - 5 * p[4] * p[3] * p[2] * p[1] * p[0]**5 + 20 * p[3] * p[2] * p[1] * p[0]**5 + 10 * p[3] * p[2]**2 * p[0]**5 + 10 * p[3]**2 * p[2] * p[0]**5 + 10 * p[4] * p[3] * p[2] * p[0]**5 + 20 * p[3] * p[2] * p[1]**2 * p[0]**4 + 20 * p[3] * p[2]**2 * p[1] * p[0]**4 + 20 * p[3]**2 * p[2] * p[1] * p[0]**4 + 20 * p[4] * p[3] * p[2] * p[1] * p[0]**4 - 30 * p[3] * p[2] * p[0]**5 - 10 * p[3]**2 * p[0]**5 - 10 * p[4] * p[3] * p[0]**5 - 80 * p[3] * p[2] * p[1] * p[0]**4 - 30 * p[3] * p[2]**2 * p[0]**4 - 30 * p[3]**2 * p[2] * p[0]**4 - 30 * p[4] * p[3] * p[2] * p[0]**4 - 30 * p[3] * p[2] * p[1]**2 * p[0]**3 - 30 * p[3] * p[2]**2 * p[1] * p[0]**3 - 30 * p[3]**2 * p[2] * p[1] * p[0]**3 - 30 * p[4] * p[3] * p[2] * p[1] * p[0]**3 + 20 * p[3] * p[0]**5 + 5 * p[4] * p[0]**5 + 90 * p[3] * p[2] * p[0]**4 + 20 * p[3]**2 * p[0]**4 + 20 * p[4] * p[3] * p[0]**4 + 120 * p[3] * p[2] * p[1] * p[0]**3 + 30 * p[3] * p[2]**2 * p[0]**3 + 30 * p[3]**2 * p[2] * p[0]**3 + 30 * p[4] * p[3] * p[2] * p[0]**3 + 20 * p[3] * p[2] * p[1]**2 * p[0]**2 + 20 * p[3] * p[2]**2 * p[1] * p[0]**2 + 20 * p[3]**2 * p[2] * p[1] * p[0]**2 + 20 * p[4] * p[3] * p[2] * p[1] * p[0]**2 - 5 * p[0]**5 - 40 * p[3] * p[0]**4 - 5 * p[4] * p[0]**4 - 90 * p[3] * p[2] * p[0]**3 - 10 * p[3]**2 * p[0]**3 - 10 * p[4] * p[3] * p[0]**3 - 80 * p[3] * p[2] * p[1] * p[0]**2 - 10 * p[3] * p[2]**2 * p[0]**2 - 10 * p[3]**2 * p[2] * p[0]**2 - 10 * p[4] * p[3] * p[2] * p[0]**2 - 5 * p[3] * p[2] * p[1]**2 * p[0] - 5 * p[3] * p[2]**2 * p[1] * p[0] - 5 * p[3]**2 * p[2] * p[1] * p[0] - 5 * p[4] * p[3] * p[2] * p[1] * p[0] + 5 * p[0]**4 + 20 * p[3] * p[0]**3 + 30 * p[3] * p[2] * p[0]**2 + 20 * p[3] * p[2] * p[1] * p[0] )
        return f

    def f_bscc_5(self, p):
        f = ( 5 * p[4] * p[3] * p[2] * p[1] * p[0]**5 - 10 * p[4] * p[3] * p[2] * p[0]**5 - 20 * p[4] * p[3] * p[2] * p[1] * p[0]**4 + 10 * p[4] * p[3] * p[0]**5 + 30 * p[4] * p[3] * p[2] * p[0]**4 + 30 * p[4] * p[3] * p[2] * p[1] * p[0]**3 - 5 * p[4] * p[0]**5 - 20 * p[4] * p[3] * p[0]**4 - 30 * p[4] * p[3] * p[2] * p[0]**3 - 20 * p[4] * p[3] * p[2] * p[1] * p[0]**2 + p[0]**5 + 5 * p[4] * p[0]**4 + 10 * p[4] * p[3] * p[0]**3 + 10 * p[4] * p[3] * p[2] * p[0]**2 + 5 * p[4] * p[3] * p[2] * p[1] * p[0] )
        return f


### UNIT TEST ###
import sys

def main():
    dmodel = Semisync5bees()
    (s, m, f) = dmodel.sample(
        params=[0.1, 0.2, 0.4, 0.5, 0.6],
        trials_count=10000
        )
    print("Simplex assert:    {}".format(np.sum(dmodel.eval_bscc_pfuncs([0.1, 0.2]))))
    print("Sample categorical {}".format(s))
    print("Sample multinomial {}".format(m))
    print("Sample frequency   {}".format(f))


if __name__ == "__main__":
    sys.exit(main())