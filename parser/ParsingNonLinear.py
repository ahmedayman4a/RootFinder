import sympy as sp

class NonlinearEquation:
    def __init__(self, equation_str):
        # Define the symbolic variable
        self.x = sp.symbols('x')
        # Parse the string into a sympy expression
        self.expression = sp.sympify(equation_str)
        # Create a callable function from the expression
        self.function = sp.lambdify(self.x, self.expression, "numpy")

    def evaluate(self, x_value):
        # Evaluate the function for a given value of x
        return self.function(x_value)

# # Example usage:
# # Create an instance of the class with the equation as a string
# equation = NonlinearEquation("x**2 + sin(x)+x^3")

# # Evaluate the equation for x = 1
# result = equation.evaluate(2)
# print(result)