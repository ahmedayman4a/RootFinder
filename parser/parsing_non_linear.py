import sympy as sp

class NonlinearEquation:
    def __init__(self, equation_str):
        self.valid = False
        self.error_message = ""
        self.function = None
        # Define the symbolic variable
        self.x = sp.symbols('x')
        try:
            # Parse the string into a sympy expression
            self.expression = sp.sympify(equation_str)
            # Create a callable function from the expression
            self.function = sp.lambdify(self.x, self.expression, "numpy")
            self.valid = True
        except Exception as e:
            self.error_message = f"Invalid equation: {e}"

    def evaluate(self, x_value):
        # Check if the equation was valid before evaluating
        if not self.valid:
            return f"Error: Cannot evaluate due to invalid equation. {self.error_message}"
        return self.function(x_value)

# # Example usage:
# equation = NonlinearEquation("y + sin(x)")

# # Evaluate the equation for x = 1
# result = equation.evaluate(1)
# if equation.valid:
#     print("The result is:", result)
# else:
#     print("There was an error:", equation.error_message)
