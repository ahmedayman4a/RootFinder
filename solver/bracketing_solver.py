from mpmath import mp

mp.dps = 5  

class BracketingMethodsSolver:
    def __init__(self, equation):
        self.equation = equation
        self.steps = []

    def absolute_error(self, x_new, x_old):
        return mp.fabs((x_new - x_old) / x_new) * 100

    def bisection_method(self, L, U, error):
        step = 0
        L = mp.mpf(L)
        U = mp.mpf(U)
        error = mp.mpf(error)

        if self.equation(L) * self.equation(U) >= 0:
            raise ValueError("Bisection method fails.")
        else:
            x_old = (L + U) / 2
            if self.equation(L) * self.equation(x_old) < 0:
                U = x_old
            else:
                L = x_old
            x_new = (L + U) / 2
            self.steps.append("Step: " + str(step) + " Lower bound: " + str(L) + " Upper bound: " + str(U) + " X: " + str(x_old) + "\n")
            step+=1
            while self.absolute_error(x_new, x_old) > error:
                x_old = x_new
                if self.equation(L) * self.equation(x_old) < 0:
                    U = x_old
                else:
                    L = x_old
                x_new = (L + U) / 2
                self.steps.append("Step: " + str(step) + " Lower bound: " + str(L) + " Upper bound: " + str(U) + " X: " + str(x_old) + " Absolute Error: " + str(self.absolute_error(x_new, x_old)) + "\n")
                step+=1
            self.steps.append("X: " + str(x_new))
            return x_new

    def false_position_method(self, L, U, error):
        step = 0
        L = mp.mpf(L)
        U = mp.mpf(U)
        error = mp.mpf(error)

        if self.equation(L) * self.equation(U) >= 0:
            raise ValueError("False position method fails.")
        else:
            x_old = (L * self.equation(U) - U * self.equation(L)) / (self.equation(U) - self.equation(L))
            if self.equation(L) * self.equation(x_old) < 0:
                U = x_old
            else:
                L = x_old
            x_new = (L * self.equation(U) - U * self.equation(L)) / (self.equation(U) - self.equation(L))
            self.steps.append("Lower bound: " + str(L) + " Upper bound: " + str(U) + " X: " + str(x_old + "\n"))
            step+=1
            while self.absolute_error(x_new, x_old) > error:
                x_old = x_new
                if self.equation(L) * self.equation(x_old) < 0:
                    U = x_old
                else:
                    L = x_old
                x_new = (L * self.equation(U) - U * self.equation(L)) / (self.equation(U) - self.equation(L))
                self.steps.append("Step: " + str(step) + " Lower bound: " + str(L) + " Upper bound: " + str(U) + " X: " + str(x_old) + " Absolute Error: " + str(self.absolute_error(x_new, x_old)) + "\n")
                step+=1

            self.steps.append("X: " + str(x_new))
            return x_new

# Example:
equation = lambda x: 3 * x**4 + 6.1 * x**3 - 2 * x**2 + 3 * x + 2
solver = BracketingMethodsSolver(equation)
bisection_result = solver.bisection_method(-1, 0, 0.001)
print("Bisection Method Result For a:", bisection_result)
false_position_result = solver.false_position_method(-1, 0, 0.001)
print("False Position Method Result For a:", false_position_result)