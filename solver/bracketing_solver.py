from solver.round_to_sf import round_to_sf

class BracketingMethodsSolver:
    def __init__(self, equation, sf, max_iterations=100):
        self.equation = equation
        self.steps = []
        self.sf = sf
        self.max_iterations = max_iterations

    def absolute_error(self, x_new, x_old):
        return abs((x_new - x_old) / x_new) * 100

    def bisection_method(self, L, U, error):
        step = 0
        L = round_to_sf(L, self.sf)
        U = round_to_sf(U, self.sf)
        error = round_to_sf(error, self.sf)

        if self.equation(L) * self.equation(U) >= 0:
            raise ValueError("Bisection method fails.")
        else:
            x_old = round_to_sf((L + U) / 2, self.sf)
            self.steps.append(f"[{step}]:\nLower bound: {L}\nUpper bound: {U}\nX: {x_old}\n")
            if self.equation(L) * self.equation(x_old) < 0:
                U = x_old
            else:
                L = x_old
            x_new = round_to_sf((L + U) / 2, self.sf)
            step += 1
            self.steps.append(f"[{step}]:\nLower bound: {L}\nUpper bound: {U}\nX: {x_new}\nAbsolute Error: {self.absolute_error(x_new, x_old)}\n")
            while self.absolute_error(x_new, x_old) > error and step < self.max_iterations:
                x_old = x_new
                if self.equation(L) * self.equation(x_old) < 0:
                    U = x_old
                else:
                    L = x_old
                x_new = round_to_sf((L + U) / 2, self.sf)
                step += 1
                self.steps.append(f"[{step}]:\nLower bound: {L}\nUpper bound: {U}\nX: {x_new}\nAbsolute Error: {self.absolute_error(x_new, x_old)}\n")
            self.steps.append(f"X: {x_new}")
            return x_new

    def false_position_method(self, L, U, error):
        step = 0
        L = round_to_sf(L, self.sf)
        U = round_to_sf(U, self.sf)
        error = round_to_sf(error, self.sf)

        if self.equation(L) * self.equation(U) >= 0:
            raise ValueError("False position method fails.")
        else:
            x_old = round_to_sf((L * self.equation(U) - U * self.equation(L)) / (self.equation(U) - self.equation(L)), self.sf)
            self.steps.append(f"[{step}]:\nLower bound: {L}\nUpper bound: {U}\nX: {x_old}\n")
            if self.equation(L) * self.equation(x_old) < 0:
                U = x_old
            else:
                L = x_old
            x_new = round_to_sf((L * self.equation(U) - U * self.equation(L)) / (self.equation(U) - self.equation(L)), self.sf)
            step += 1
            self.steps.append(f"[{step}]:\nLower bound: {L}\nUpper bound: {U}\nX: {x_new}\nAbsolute Error: {self.absolute_error(x_new, x_old)}\n")
            while self.absolute_error(x_new, x_old) > error and step < self.max_iterations:
                x_old = x_new
                if self.equation(L) * self.equation(x_old) < 0:
                    U = x_old
                else:
                    L = x_old
                x_new = round_to_sf((L * self.equation(U) - U * self.equation(L)) / (self.equation(U) - self.equation(L)), self.sf)
                step += 1
                self.steps.append(f"[{step}]:\nLower bound: {L}\nUpper bound: {U}\nX: {x_new}\nAbsolute Error: {self.absolute_error(x_new, x_old)}\n")
            self.steps.append(f"X: {x_new}")
            return x_new

# Example:
# equation = lambda x: 3 * x**4 + 6.1 * x**3 - 2 * x**2 + 3 * x + 2
# sf = 5  # Specify the desired number of significant figures
# solver = BracketingMethodsSolver(equation, sf)
# bisection_result = solver.bisection_method(-1, 0, 0.001)
# print("Bisection Method Result For a:", bisection_result)
# false_position_result = solver.false_position_method(-1, 0, 0.001)
# print("False Position Method Result For a:", false_position_result)