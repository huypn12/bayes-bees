## UNIT TEST ##


def test_3bees():
    max_trials = 1000
    print('Metropolis-Hasting, sampling with chain run, {} trials'.format(max_trials))
    dtmc_filepath = 'models/prism/bee_multiparam_synchronous_3.pm'
    bscc_filepath = 'models/prism/bee_multiparam_synchronous_3.txt'
    bees_model = BeesModel.from_files(dtmc_filepath, bscc_filepath)
    r = [0.1, 0.2, 0.3]
    print('True parameters: {}'.format(r))
    (s, m, f) = bees_model.sample(params=r, trials_count=1000)
    print('Synthetic data {}'.format(m))
    mcmc = BayesianMcmcSim(bees_model)
    start_time = timeit.default_timer()
    mcmc.estimate_p(m)
    stop_time = timeit.default_timer()
    print('Finished in {} seconds, chain length {}'.format(
        stop_time - start_time, mcmc.mh_params['chain_length']))
    print('Estimated parameter: {}'.format(mcmc.estimated_params['P']))
    print('Highest posterior density interval: {}'.format(mcmc.estimated_params['HPD']))
    print('Log likelihood: {}'.format(mcmc.estimated_params['log_llh']))
    print('AIC: {}\n'.format(mcmc.estimated_params['AIC']))


def main():
    test_3bees()


if __name__ == "__main__":
    sys.exit(main())
