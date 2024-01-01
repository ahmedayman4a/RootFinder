#Move to root directory of the project to run (or TODO: Fix import issue)
from parsers.parsing_non_linear import NonlinearEquation
from solver.second_newton_raphson import SecondNewtonRaphson 
if __name__ == "__main__":
    parsed_expr = "x**5-11*x**4+46*x**3-90*x**2+81*x-27"
    expression = NonlinearEquation(parsed_expr)
    if not expression.valid:
        print("Can't Solve")
    x0 = 10
    tol =1e-6
    sf=100
    maxiter=50
    snr = SecondNewtonRaphson(expression.function, expression.derivative_function, expression.second_derivative_function,x0, tol, sf,maxiter)
    root = snr.solve()
    for step in snr.steps:
        print(step)
        