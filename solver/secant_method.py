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
        threshold = 1e10
        x0 = self.x0
        x1 = self.x1
        tol = self.tol
        max_iter = self.max_iter
        func = self.func
        sf = self.sf

        self.steps.append(f"Initial guesses: x0 = {x0}, x1 = {x1}")

        for i in range(max_iter):
            f_x0 = func(x0)
            f_x1 = func(x1)
            x1_minus_x0 = x1 - x0

            # Check if any intermediate calculation is not valid
            if any(np.isinf(val) or np.isnan(val) for val in [f_x1, f_x0, x1_minus_x0]):
                self.steps.append("Error: intermediate calculation resulted in inf or nan at iteration {}".format(i + 1))
                return None

            if f_x1 - f_x0 == 0:
                self.steps.append(f"Division by zero at iteration {i + 1}, cannot continue.")
                return None

            x_new = round_to_sf(x1 - f_x1 * (x1_minus_x0) / (f_x1 - f_x0), sf)
            epsolon_a = abs((x_new - x1) / x_new) * 100 if x_new != 0 else float('inf')

            self.steps.append(f"Iteration {i + 1}: x_new = {x_new}, f(x_new) = {f_x1}, Relative Error: {epsolon_a}%")

            if epsolon_a <= tol:
                self.steps.append(f"Convergence after {i + 1} iterations.")
                self.steps.append(f"Root: {x_new}")
                return x_new
            if abs(x_new) > threshold:
                self.steps.append("Diverge!!")
                return None
            x0 = x1
            x1 = x_new

        self.steps.append(f"No convergence after {max_iter} iterations.")
        return None

# Example usage:
# sm = SecantMethod(func, x0, x1, tol, max_iter, sf)
# root = sm.solve()
# for step in sm.steps:
#     print(step)
