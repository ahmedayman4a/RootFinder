import numpy as np
from solver.round_to_sf import round_to_sf

class NewtonRaphson:
    def __init__(self, f, df, x0, tol, sf, m, maxiter=50):
        self.func = f
        self.df = df
        self.x0 = x0
        self.tol = tol
        self.sf = sf
        self.m = m
        self.maxiter = maxiter
        self.steps = []

    def solve(self):
        sf = self.sf
        x0 = round_to_sf(self.x0, sf)
        func = self.func
        df = self.df

        for i in range(self.maxiter):
            # Corrected x_new calculation
            x_new = round_to_sf(x0 - round_to_sf(self.m * (round_to_sf(func(x0), sf) / round_to_sf(df(x0), sf)), sf), sf)

            epsolon_a = abs(((x_new - x0) / x_new) * 100)
            x0 = x_new
            self.steps.append("Iteration {}: {} Relative Error: {}".format(i + 1, x_new, epsolon_a))

            # Corrected convergence criteria
            if func(x_new) == 0 or epsolon_a <= self.tol:
                self.steps.append("It converges after {} iterations".format(i + 1))
                self.steps.append("Root: {}".format(x_new))
                return x_new

        self.steps.append("It doesn't converge after {} iterations".format(self.maxiter))
        return x_new

