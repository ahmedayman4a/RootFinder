from round_to_sf import round_to_sf

class FixedPoint:
    def __init__(self, f, g, x0, tol, sf, maxiter=50):
        self.f = f
        self.g = g
        self.x0 = x0
        self.tol = tol
        self.sf = sf
        self.maxiter = maxiter
        self.steps = []

    def solve(self):
        x0 = round_to_sf(self.x0, self.sf)
        self.steps.append(f"Initial guess: {x0}")

        for i in range(self.maxiter):
            # Calculate the next approximation
            try:
                x_new = round_to_sf(self.g(x0), self.sf)
            except Exception as e:
                print("Error in function evaluation:", e)
                return None

            # Calculate the relative error
            epsilon_a = abs((x_new - x0) / x_new) * 100 if x_new != 0 else float('inf')
            self.steps.append(f"Iteration {i + 1}:")
            self.steps.append(f"x_new = {x_new}, Relative Error: {epsilon_a}%")

            # Check for convergence
            if epsilon_a <= self.tol:
                self.steps.append(f"Convergence after {i + 1} iterations.")
                self.steps.append(f"Root: {x_new}")
                return x_new

            # Update the current point
            x0 = x_new

        self.steps.append(f"No convergence after {self.maxiter} iterations.")
        return None

# # Define your f(x) and g(x) functions
# def f(x):
#     return x**2 - 2*x -3   # Replace this with your desired f(x) function

# def g(x):
#     return (x**2-3)/2  # Replace this with your desired g(x) function

# # Define initial values
# initial_guess = 4  # Initial guess for the root
# tolerance = 0.0001  # Tolerance for convergence
# significant_figures = 5  # Number of significant figures
# max_iterations = 50  # Maximum number of iterations

# # Create an instance of FixedPoint with predefined f(x) and g(x)
# fixed_pt = FixedPoint(f, g, initial_guess, tolerance, significant_figures, max_iterations)

# # Solve the equation using Fixed-Point iteration
# root = fixed_pt.solve()

# # Display the result and iteration steps
# print("Iteration steps:")
# for step in fixed_pt.steps:
#     print(step)
# if root is not None:
#     print("Root found:", root)
    
# else:
#     print("Diverge!!")