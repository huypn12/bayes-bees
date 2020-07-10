from .bees_model import BeesModel


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
        return [linear_r[0] * i + linear_r[1]
                for i in range(0, self.chain_params_count)]

    def set_params(self, chain_params):
        self.params = self.eval_chain_params(chain_params)
