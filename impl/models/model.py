class Model(object):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_bscc_pfuncs(self, ):
        pass

    @abstractmethod
    def eval_bscc_pfuncs(self, p):
        pass

    @abstractmethod
    def sample(self, sample_size):
        pass