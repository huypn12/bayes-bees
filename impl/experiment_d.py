from models.bees_linear_model import BeesLinearModel
from bayesian_mcmc_linear import BayesianMcmcLinear

import sys, timeit


def run_linear_3bees():
    dtmc_filepath = 'models/prism/bee_multiparam_synchronous_3.pm'
    bscc_filepath = 'models/prism/bee_multiparam_synchronous_3.txt'
    model = BeesLinearModel.from_files(dtmc_filepath, bscc_filepath)
    p_true = [0.2, 0.5]
    (s, m, f) = model.sample(params=p_true, trials_count=10000)
    print("Data multinomial: {}".format(m))
    print("Data histogram: {}".format(f))
    # pass model in to get BSCC parameterized functions
    mcmc = BayesianMcmcLinear(model)
    mcmc.mh_params['chain_length'] = 50000
    start_time = timeit.default_timer()
    mcmc.estimate_p(m)
    stop_time = timeit.default_timer()
    print('Finished in {} seconds, chain length {}'.format(
        stop_time - start_time, mcmc.mh_params['chain_length']))
    print('Estimated parameter: {}'.format(mcmc.estimated_params['P']))
    print('Log likelihood: {}'.format(mcmc.estimated_params['log_llh']))
    print('AIC: {}\n'.format(mcmc.estimated_params['AIC']))

def main():
    run_linear_3bees()

if __name__ == "__main__":
    sys.exit(main())