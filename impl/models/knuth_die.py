import sys

import numpy as np
import scipy as sp

from .data_model import DataModel

class KnuthDie(DataModel):
    def __init__(self,):
        super().__init__()
        self.name = 'Knuth Die, 1 param'
        self.params_count = 1
        self.bscc_pfuncs = [
            lambda p: p[0]**2 / (p[0] + 1),
            lambda p: ((-1) * p[0]**2 + p[0]) / (p[0] + 1),
            lambda p: (p[0]**2) / (p[0] + 1),
            lambda p: ((-1) * p[0]**2 + p[0]) / (p[0] + 1),
            lambda p: (p[0]**2 - 2 * p[0] + 1) / (p[0] + 1),
            lambda p: ((-1) * p[0]**2 + p[0]) / (p[0] + 1),
        ]

    def get_name(self, ):
        return self.name

    def get_params_count(self, ):
        return self.params_count

    def get_bscc_pfuncs(self, ):
        return self.bscc_pfuncs

    def eval_bscc_pfuncs(self, p):
        return [f(p) for f in self.get_bscc_pfuncs()]


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


### UNIT TEST ###
def main():
    dmodel = KnuthDie()
    (s, m, f) = dmodel.sample(
        params=[0.1],
        sample_size=10000
        )
    print("Sample categorical {}".format(s))
    print("Sample multinomial {}".format(m))
    print("Sample frequency   {}".format(f))
    print("Simplex assert:    {}".format(np.sum(dmodel.eval_bscc_pfuncs([0.7]))))

if __name__ == "__main__":
    sys.exit(main())