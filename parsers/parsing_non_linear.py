import sympy as sp

class NonlinearEquation:
    def __init__(self, equation_str):
        self.valid = False
        self.error_message = ""
        self.function = None
        self.derivative_function = None
        self.second_derivative_function = None
        # Define the symbolic variable
        self.x = sp.symbols('x')
        try:
            # Parse the string into a sympy expression
            self.expression = sp.sympify(equation_str)
            # Create a callable function from the expression
            self.function = sp.lambdify(self.x, self.expression, "numpy")
            # Compute and create a callable function for the derivative
            self.derivative_expression = sp.diff(self.expression, self.x)
            self.derivative_function = sp.lambdify(self.x, self.derivative_expression, "numpy")
            # Second Derivative
            self.second_derivative_expression = sp.diff(self.derivative_expression, self.x)
            self.second_derivative_function = sp.lambdify(self.x, self.second_derivative_expression, "numpy")
            self.valid = True
        except Exception as e:
            self.error_message = f"Invalid equation: {e}"

    def evaluate(self, x_value):
        # Check if the equation was valid before evaluating
        if not self.valid:
            return f"Error: Cannot evaluate due to invalid equation. {self.error_message}"
        return self.function(x_value)

    def evaluate_derivative(self, x_value):
        # Check if the equation was valid before evaluating the derivative
        if not self.valid:
            return f"Error: Cannot evaluate the derivative due to invalid equation. {self.error_message}"
        return self.derivative_function(x_value)
    def evaluate_second_derivative(self, x_value):
        # Check if the equation was valid before evaluating the second derivative
        if not self.valid:
            return f"Error: Cannot evaluate the second derivative due to invalid equation. {self.error_message}"
        return self.second_derivative_function(x_value)

# Example usage:
# equation = NonlinearEquation("x**2 + sin(x)")

# # Evaluate the equation and its derivative for x = 1
# result = equation.evaluate(1)
# derivative_result = equation.evaluate_derivative(1)
# sderivative_result = equation.evaluate_second_derivative(1)
# if equation.valid:
#     print("The result is:", result)
#     print("The derivative at this point is:", derivative_result)
#     print("The second derivative at this point is:", sderivative_result)

# else:
#     print("There was an error:", equation.error_message)
