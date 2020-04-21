import sys

import numpy as np
import scipy as sp

import matplotlib.pyplot as plt
import matplotlib as mpl


class KnuthDie(object):
    def __init__(self, p=None):
        super().__init__()
        self.p = p if p is not None else 0.5

    def get_pfuncs(self, ):
        funcs = [
            lambda p: p**2 / (p + 1),
            lambda p: ((-1) * p**2 + p) / (p + 1),
            lambda p: (p**2) / (p + 1),
            lambda p: ((-1) * p**2 + p) / (p + 1),
            lambda p: (p**2 - 2 * p + 1) / (p + 1),
            lambda p: ((-1) * p**2 + p) / (p + 1),
        ]
        return funcs

    def evaluate_pdist(self, pdist, p):
        return [f(p) for f in pdist]


    def sample(self, sample_size: int = 1000):
        """
        Sample by categorical distribution
        Later can be transformed into multinomial sample
        """
        P = self.evaluate_pdist(self.get_pfuncs(), self.p)
        N = len(P)
        categorical = np.random.choice(N, sample_size, p=P)
        multinomial = [0] * N
        for it in categorical:
            multinomial[it] += 1
        norm = sum(multinomial) * 1.0
        frequency = [v / norm for v in multinomial]
        return (categorical, multinomial, frequency)


def test_experiment():
    experiment = KnuthDie(p=0.1)
    (s, m, f) = experiment.sample(10000)
    print("Sample categorical {}".format(s))
    print("Sample multinomial {}".format(m))
    print("Sample frequency   {}".format(f))

def main():
    test_experiment()


if __name__ == "__main__":
    sys.exit(main())