from . import predictors

class IterativeMinimizer:
    def __init__(self, predictor=None, discard_regressive_errors=True):
        self.predictor = predictor or predictors.random_step
        self.error_history = []
        self.parameter_history = []
        self.discard_regressive_errors = discard_regressive_errors

    def _objective(self, ga):
        ga.output = ga.expression(ga.parameters)
        return ga.error_metric(ga.input, ga.output)

    def iterate(self, ga):
        if len(self.error_history) != len(self.parameter_history):
            raise ValueError("Mismatch in error and parameter history length")

        # First ever iteration: use input as the starting guess
        if not self.parameter_history:
            if ga.input is None:
                raise ValueError("Initial input is missing from ga")
            ga.parameters = ga.input
            error = self._objective(ga)
            self.parameter_history.append(ga.parameters)
            self.error_history.append(error)
            return ga.output

        # Use predictor to make a new guess
        new_params = self.predictor(self.parameter_history, self.error_history)
        ga.parameters = new_params
        error = self._objective(ga)

        if self.discard_regressive_errors and error > self.error_history[-1]:
            return None

        self.parameter_history.append(new_params)
        self.error_history.append(error)
        return ga.output

