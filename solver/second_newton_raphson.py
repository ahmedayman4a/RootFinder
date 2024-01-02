import numpy as np
import sympy as sp
from solver.round_to_sf import round_to_sf

class SecondNewtonRaphson:
    def __init__(self, f, df, sdf,x0, tol, sf, maxiter=50):
        self.func = f
        self.df = df
        self.sdf=sdf    # second derivative function
        self.x0 = x0
        self.tol = tol
        self.sf = sf
        self.maxiter = maxiter
        self.steps = []

    def solve(self):
        threshold = 1e10
        sf = self.sf
        x0 = round_to_sf(self.x0, sf)
        func = self.func
        df = self.df
        sdf = self.sdf  # Second derivative function
        self.steps.append(f"Initial guess: {x0}")

        for i in range(self.maxiter):
            # Evaluate function, its first derivative, and second derivative
            f_x0 = round_to_sf(func(x0), sf)
            df_x0 = round_to_sf(df(x0), sf)
            sdf_x0 = round_to_sf(sdf(x0), sf)
            if (f_x0 == 0):
                self.steps.append(f"Convergence after {i} iterations.")
                self.steps.append(f"Root: {x_new}")
                return x0

            if (df_x0)*(df_x0)==f_x0*sdf_x0:
                self.steps.append(f"Division by zero at iteration {i + 1}, derivative is zero.")
                return None
            numerator = round_to_sf(f_x0 * df_x0,sf)
            denominator = round_to_sf(df_x0**2 - f_x0 * sdf_x0,sf)
            # Calculate the next approximation for the root using second derivative
            x_new = round_to_sf(x0-(numerator)/(denominator),sf)
            self.steps.append(f"Iteration {i + 1}: x_new =  {x0} - {numerator} / {denominator}")

            # Calculate the relative error
            epsilon_a = abs(((x_new - x0) / x_new) * 100) if x_new != 0 else float('inf')
            self.steps.append(
                f"therefore, x_new = {x_new}, f(x_new) = {f_x0}, f'(x_new) = {df_x0}, f''(x_new) = {sdf_x0}, Relative Error: {epsilon_a}%\n"
            )
            self.steps.append("_____________________________________________________")
            # Check for convergence
            if abs(x_new) > threshold:
                self.steps.append("Diverge!!")
                return None
            if epsilon_a <= self.tol or self.func(x_new) == 0:
                self.steps.append(f"Convergence after {i + 1} iterations.")
                self.steps.append(f"Root: {x_new}")
                return x_new

            # Update the current point
            x0 = x_new

        self.steps.append(f"No convergence after {self.maxiter} iterations.")
        return None


# Example Usage
# if __name__ == "__main__":
#     parsed_expr = "x**5-11*x**4+46*x**3-90*x**2+81*x-27"
#     expression = NonlinearEquation(parsed_expr)
#     if not expression.valid:
#         print("Can't Solve")
#     x0 = 10
#     tol =1e-6
#     sf=100
#     maxiter=50
#     snr = SecondNewtonRaphson(expression.function, expression.derivative_function, expression.second_derivative_function,x0, tol, sf,maxiter)
#     root = snr.solve()
#     for step in snr.steps:
#         print(step)
        
