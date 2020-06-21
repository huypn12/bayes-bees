from .bees_model import BeesModel

import numpy as np
from asteval import Interpreter

class BeesLinearModel(BeesModel):
    def __init__(self):
        super().__init__()
        self.chain_params_count = 0

    @staticmethod
    def from_files(prism_model_filepath, prism_result_filepath):
        model = BeesModel.from_files(prism_model_filepath, prism_result_filepath)
        linear_model = BeesLinearModel()
        for name, value in vars(model).items():
            setattr(linear_model, name, value)
        linear_model.chain_params_count = model.params_count
        linear_model.params_count = 2
        return linear_model

    def eval_chain_params(self, linear_r):
        return [linear_r[0] * i + linear_r[1] for i in range(0, self.chain_params_count)]

    def eval_pmc_pfuncs(self, linear_r):
        chain_r = self.eval_chain_params(linear_r)
        return super().eval_pmc_pfuncs(chain_r)

    def eval_bscc_pfuncs(self, linear_r):
        chain_r = self.eval_chain_params(linear_r)
        return super().eval_bscc_pfuncs(chain_r)

## UNIT TEST ##
import sys, timeit

def test_bscc_sample():
    dtmc_filepath = 'models/prism/bee_multiparam_synchronous_3.pm'
    bscc_filepath = 'models/prism/bee_multiparam_synchronous_3.txt'
    bees_model = BeesLinearModel.from_files(dtmc_filepath, bscc_filepath)
    (s, m, f) = bees_model.sample(
        params=[0.1, 0.1],
        trials_count=10000
    )
    print('Sampling with BSCC rational function.')
    start_time = timeit.default_timer()
    bscc_eval = bees_model.eval_bscc_pfuncs([0.1, 0.1])
    stop_time = timeit.default_timer()
    print('Finished evaluation in {} seconds'.format(
        stop_time - start_time))
    print("\tSimplex assert:    {}".format(
        np.sum(bscc_eval)))
    print("\tSample categorical {}".format(s))
    print("\tSample multinomial {}".format(m))
    print("\tSample frequency   {}".format(f))

def test_chain_run():
    print('Sampling with chain run')
    dtmc_filepath = 'models/prism/bee_multiparam_synchronous_3.pm'
    bscc_filepath = 'models/prism/bee_multiparam_synchronous_3.txt'
    bees_model = BeesLinearModel.from_files(dtmc_filepath, bscc_filepath)
    r = [0.1, 0.1]
    start_time = timeit.default_timer()
    h = bees_model.sample_run_chain(r, max_trials=1000)
    stop_time = timeit.default_timer()
    print('Finished in {} seconds, chain length {}'.format(
        stop_time - start_time, 1000))
    assert(sum(h) - 1.0 < 1e-5)
    print('\tSample frequency:', h)

def main():
    test_bscc_sample()
    test_chain_run()

if __name__ == "__main__":
    sys.exit(main())