from .data_model import DataModel

import sys
import numpy as np

class Bees2(DataModel):
    def __init__(self):
        super().__init__()
        self.bscc_pfuncs = [
            lambda p: self.f_bscc_0(p),
            lambda p: self.f_bscc_1(p),
            lambda p: self.f_bscc_2(p)
        ]
        self.params_count = 2

    def f_bscc_0(self, p):
        return p[0]**2 - 2*p[0] + 1

    def f_bscc_1(self, p):
        return (2* p[1] * p[0]**2 - 2 * p[0]**2 - 2 * p[1] * p[0] + 2 * p[0])

    def f_bscc_2(self, p):
        return (-2 * p[1] * p[0]**2 + p[0]**2 + 2 * p[1] * p[0])

    def get_params_count(self,):
        return self.params_count

    def get_bscc_pfuncs(self, ):
        return self.bscc_pfuncs

    def eval_bscc_pfuncs(self, p):
        return [f(p) for f in self.bscc_pfuncs]

    def sample(self, params, sample_size: int = 1000):
        """
        Sample by categorical distribution
        Later can be transformed into multinomial sample
        """
        P = self.eval_bscc_pfuncs(params)
        N = len(P)
        categorical = np.random.choice(N, sample_size, p=P)
        multinomial = [0] * N
        for it in categorical:
            multinomial[it] += 1
        norm = sum(multinomial) * 1.0
        frequency = [v / norm for v in multinomial]
        return (categorical, multinomial, frequency)


### UNIT TEST ###
def main():
    dmodel = Bees2()
    (s, m, f) = dmodel.sample(
        params=[0.1, 0.2],
        sample_size=10000
        )
    print("Simplex assert:    {}".format(np.sum(dmodel.eval_bscc_pfuncs([0.1, 0.2]))))
    print("Sample categorical {}".format(s))
    print("Sample multinomial {}".format(m))
    print("Sample frequency   {}".format(f))


if __name__ == "__main__":
    sys.exit(main())