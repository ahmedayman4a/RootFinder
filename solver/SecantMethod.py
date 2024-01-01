import numpy as np
from solver.round_to_sf import round_to_sf

class SecantMethod:
    def __init__(self, func, x0, x1, tol, max_iter, sf):
        self.func = func
        self.x0 = x0
        self.x1 = x1
        self.tol = tol
        self.max_iter = max_iter
        self.sf = sf
        self.steps = []

    def solve(self):
        x0 = self.x0
        x1 = self.x1
        tol = self.tol
        max_iter = self.max_iter
        func = self.func
        sf = self.sf

        for i in range(max_iter):
            f6_1_x1 = func(x1)
            f6_1_x0 = func(x0)
            x1_minus_x0 = x1 - x0
            if np.isinf(f6_1_x1) or np.isnan(f6_1_x1) or np.isinf(f6_1_x0) or np.isnan(f6_1_x0) or np.isinf(x1_minus_x0) or np.isnan(x1_minus_x0):
                print("Error: intermediate calculation resulted in inf or nan")
                return None
            x_new = round_to_sf(x1 - round_to_sf(round_to_sf(f6_1_x1 * round_to_sf(x1_minus_x0, sf), sf), sf) / round_to_sf(f6_1_x1 - f6_1_x0, sf), sf)

            epsolon_a = abs((x_new - x1) / x_new) * 100
            x0 = x1
            x1 = x_new
            self.steps.append(("Iteration {}: {} Relative Error: {}".format(i + 1, x_new, epsolon_a)))

            if func(x_new) == 0 or epsolon_a <= tol:
                self.steps.append(("It converges after {} iterations".format(i + 1)))
                self.steps.append(("Root: {}".format(x_new)))
                return x_new

        self.steps.append(("It doesn't converge after {} iterations".format(max_iter)))
