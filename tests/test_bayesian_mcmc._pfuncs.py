"""
Some notes on complexity of this estimation scheme:
1. There are nIter iterations
2. On each iteration:
    a.
"""

"""
Experiment setup:
1. Parameters of DTMC p = (p1...pk)
2. Parameterized BSCC distribution : f = (f_1...f_n)
3. Posterior on p. Likelihood function is multinomial on f
4. Method. metropolis hastings with Beta distribution as proposal distribution
5. Setup: synthesize data from p_true. Then run the scheme to get p_hat
"""

## UNIT TEST ##
import timeit

# Deprecated models; now switch to general BeesModel
from models.bees_model import BeesModel

def test_3bees():
    dtmc_filepath = 'models/prism/bee_multiparam_synchronous_3.pm'
    bscc_filepath = 'models/prism/bee_multiparam_synchronous_3.txt'
    model = BeesModel.from_files(dtmc_filepath, bscc_filepath)
    p_true = [0.2, 0.5, 0.7]
    (s, m, f) = model.sample(params=p_true, trials_count=10000)
    print("Data multinomial: {}".format(m))
    print("Data histogram: {}".format(f))
    # pass model in to get BSCC parameterized functions
    mcmc = BayesianMcmc(model)
    start_time = timeit.default_timer()
    mcmc.estimate_p(m)
    stop_time = timeit.default_timer()
    print('Finished in {} seconds, chain length {}'.format(
        stop_time - start_time, mcmc.mh_params['chain_length']))
    print('Estimated parameter: {}'.format(mcmc.estimated_params['P']))
    print('Log likelihood: {}'.format(mcmc.estimated_params['log_llh']))
    print('AIC: {}\n'.format(mcmc.estimated_params['AIC']))

def main():
    test_3bees()

if __name__ == "__main__":
    sys.exit(main())