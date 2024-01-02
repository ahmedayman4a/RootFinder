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
        threshold=1e10
        sf = self.sf
        x0 = round_to_sf(self.x0, sf)
        func = self.func
        df = self.df
        self.steps.append(f"Initial guess: {x0}")

        for i in range(self.maxiter):
            # Evaluate function and its derivative
            f_x0 = round_to_sf(func(x0), sf)
            df_x0 = round_to_sf(df(x0), sf)
            if df_x0 == 0:
                self.steps.append(f"Division by zero at iteration {i + 1}, derivative is zero.")
                break

            # Calculate the next approximation for the root
            x_new = round_to_sf(x0 - self.m * (f_x0 / df_x0), sf)
            
            # Calculate the relative error
            epsolon_a = abs(((x_new - x0) / x_new) * 100) if x_new != 0 else float('inf')
            self.steps.append(f"Iteration {i + 1}: x_new = {x_new}, f(x_new) = {f_x0}, f'(x_new) = {df_x0}, Relative Error: {epsolon_a}%")

            # Check for convergence
            if epsolon_a <= self.tol or f_x0 == 0:
                self.steps.append(f"Convergence after {i + 1} iterations.")
                self.steps.append(f"Root: {x_new}")
                return x_new
            if abs(x_new) > threshold:
                self.steps.append("Diverge!!")
                return None
            # Update the current point
            x0 = x_new

        self.steps.append(f"No convergence after {self.maxiter} iterations.")
        return None

# Sample usage (you must define the functions f and df, and provide initial values for x0, tol, etc.):
# nr = NewtonRaphson(f, df, x0, tol, sf, m)
# root = nr.solve()
# for step in nr.steps:
#     print(step)
