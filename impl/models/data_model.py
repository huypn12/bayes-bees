from abc import ABC, abstractmethod

class DataModel(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_params_count(self, ):
        pass

    @abstractmethod
    def get_bscc_pfuncs(self, ):
        pass

    @abstractmethod
    def eval_bscc_pfuncs(self, p):
        pass

    @abstractmethod
    def sample(self, p, trials_count):
        pass