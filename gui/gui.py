import dearpygui.dearpygui as dpg
from gui.logger import CustomLogger
from mpmath import mp, matrix
import time
import numpy as np

from parsers import NonlinearEquation
from solver import BracketingMethodsSolver,FixedPoint,NewtonRaphson,SecondNewtonRaphson,SecantMethod


class SolverGUI:
    def __init__(self) -> None:
        self.set_theme()
        self.__create_menubar()
        self.func = None
        self.steps = None
        self.parsed_equation = None
    
    def set_theme(self, theme=None):
        if theme is None:
            with dpg.theme() as theme:

                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
                    dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0, category=dpg.mvThemeCat_Core)
                    dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 5, 5, category=dpg.mvThemeCat_Core)
                    dpg.add_theme_style(dpg.mvStyleVar_ItemInnerSpacing, 5, 5, category=dpg.mvThemeCat_Core)
                    dpg.add_theme_style(dpg.mvStyleVar_IndentSpacing, 20, category=dpg.mvThemeCat_Core)
                    dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 20, category=dpg.mvThemeCat_Core)
                    dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 5, category=dpg.mvThemeCat_Core)
                    dpg.add_theme_style(dpg.mvStyleVar_GrabMinSize, 5, category=dpg.mvThemeCat_Core)
                    dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 5, category=dpg.mvThemeCat_Core)
                    dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0, category=dpg.mvThemeCat_Core)
                    dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 5, category=dpg.mvThemeCat_Core)
                    dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 5, category=dpg.mvThemeCat_Core)
                    dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 5, category=dpg.mvThemeCat_Core)
                    dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0, category=dpg.mvThemeCat_Core)
                    dpg.add_theme_style(dpg.mvStyleVar_PopupBorderSize, 0, category=dpg.mvThemeCat_Core)
                    dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 5, 5, category=dpg.mvThemeCat_Core)
                    dpg.add_theme_style(dpg.mvStyleVar_WindowMinSize, 100, 100, category=dpg.mvThemeCat_Core)
                    dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 5, 5, category=dpg.mvThemeCat_Core)
                    dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.5, 0.5, category=dpg.mvThemeCat_Core)
                    dpg.add_theme_style(dpg.mvStyleVar_SelectableTextAlign, 0.5, 0.5, category=dpg.mvThemeCat_Core)
        
        dpg.bind_theme(theme)
        
    def __create_menubar(self):
        with dpg.viewport_menu_bar(tag="menu_window"):
        
            with dpg.menu(label="Settings"):
                dpg.add_menu_item(label="Reset GUI", callback=self.reset_gui)
                dpg.add_menu_item(label="Fullscreen",check=True, callback=lambda:dpg.toggle_viewport_fullscreen())
            with dpg.menu(label="About"):
                dpg.add_text("Root Finder - v1.0")
                dpg.add_text("CSE213 Numerical Analysis Project")
                dpg.add_text("By CSED 2026 Students :\nAhmed Ayman\nAhmed Youssef\nEbrahim Alaa\nAli Hassan\nAhmed Mustafa\nMostafa Esam")
                
    def on_method_changed(self, sender, app_data):
        method = dpg.get_value(sender)

        # Hide all inputs initially
        dpg.configure_item("m", show=False)
        dpg.configure_item("x0", show=False)
        dpg.configure_item("x1", show=False)
        dpg.configure_item("g_x", show=False)

        # Show inputs based on the selected method
        if method == "Fixed point":
            dpg.configure_item("g_x", show=True)
            dpg.configure_item("x0", show=True)
        elif method == "First Modified Newton-Raphson":
            dpg.configure_item("m", show=True)
            dpg.configure_item("x0", show=True)
        elif method == "Second Modified Newton-Raphson":
            dpg.configure_item("x0", show=True)
        elif method == "Secant Method":
            dpg.configure_item("x0", show=True)
            dpg.configure_item("x1", show=True)
    
    def create_windows(self):
        with dpg.window(tag="function_window", label="Function",pos=(0,30),height=320,width=500):
            with dpg.group(horizontal=True):
                dpg.add_input_text(tag="txt_function",default_value="x**3+4",no_spaces=True)
                dpg.add_text("= 0")
            dpg.add_slider_int(tag="precision",label="Precision",default_value=16,min_value=1,max_value=50)
            
            dpg.add_combo(label = "Method", tag="method", items=["Bisection", "False-Position", "Fixed point", "First Modified Newton-Raphson", "Second Modified Newton-Raphson", "Secant Method"], default_value="Bisection", callback=self.on_method_changed)
            dpg.add_input_int(tag="max_iter", label="Max Iterations", default_value=100,min_value=1, min_clamped=True)
            dpg.add_input_float(tag="abs_error", label="Absolute Error", default_value=0.001,step=0.001,format="%.6f",min_value=0.000001,min_clamped=True)
            dpg.add_input_float(tag="m", label="m", default_value=1,show=False)
            dpg.add_input_float(tag="x0", label="x0", default_value=0,show=False)
            dpg.add_input_float(tag="x1", label="x1", default_value=-1,show=False)
            dpg.add_input_text(tag="g_x", label="g(x)", default_value="x",show=False)
            dpg.add_button(label="PLOT",tag="btn_plot",width=-1,callback=self.plot_cb)
            
        with dpg.window(tag="solution_window", label="Solution",pos=(502,30),width=950,height=320):
                dpg.add_text(tag="solution_text")    
                
        with dpg.window(label="Invalid Expression", modal=True, show=False, tag="modal_invalid_exp", pos=(400,400)):
            dpg.add_text("The function you supplied is invalid\nPlease make sure that the expression is a valid non-linear equation in the expected format.")
            dpg.add_spacer(height=5)
            dpg.add_button(label="OK", width=-1, callback=lambda: dpg.configure_item("modal_invalid_exp", show=False))
            
        with dpg.window(tag="steps_window",label="Steps",pos=(702, 352),width=750,height=545):
                self.steps = CustomLogger(title="Steps",pos=(595,300),width=550,height=350,parent="steps_window")
                
        with dpg.window(tag="plot_window", label="Plot",pos=(0,352),width=700,height=545, show=False):
            with dpg.theme(tag="plot_theme"):
                with dpg.theme_component(dpg.mvLineSeries):
                    dpg.add_theme_color(dpg.mvPlotCol_Line, (60, 150, 200), category=dpg.mvThemeCat_Plots)
            
            with dpg.group(horizontal=True):
                dpg.add_text("Bound 1: ")
                dpg.add_input_double(tag="txt_bound1",default_value=1,width=150,callback=self.bound1_input_changed)
                dpg.add_spacer(width=30)
                dpg.add_text("Bound 2: ")
                dpg.add_input_double(tag="txt_bound2",default_value=1,width=150,callback=self.bound2_input_changed)
                with dpg.tooltip("txt_bound1"):
                    dpg.add_text("Bounds are only used in Bisection and False-Position methods")
                with dpg.tooltip("txt_bound2"):
                    dpg.add_text("Bounds are only used in Bisection and False-Position methods")
                
            dpg.add_text("Right click to open plot settings")
            with dpg.plot(label="Function",tag="function_plot", height=400, width=-1,anti_aliased=True):
                dpg.add_plot_legend()

                dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="x_axis")
                dpg.add_plot_axis(dpg.mvYAxis, label="f(x)", tag="y_axis")
                
                
            dpg.add_button(label="SOLVE",tag="btn_solve",width=-1, callback=self.solve_cb)

    def reset_gui(self,sender, app_data):
        # Destroy all existing windows
        dpg.delete_item("equations_window")
        dpg.delete_item("properties_window")
        dpg.delete_item("solution_window")
        dpg.delete_item("steps_window")
        # Recreate the windows
        self.create_windows()
    
    def remove_plot(self):
        dpg.delete_item("point_bound1")
        dpg.delete_item("point_bound2")
        dpg.delete_item("function_line_plot")
        dpg.delete_item("root_anot")
    
    def update_bound(self,bound_id,new_x,new_y):
        if bound_id == 1:
            dpg.set_value("txt_bound1",new_x)
        elif bound_id == 2:
            dpg.set_value("txt_bound2",new_x)
        self.redraw_bound(bound_id,new_x,new_y)
    
    def redraw_bound(self,bound_id,new_x,new_y):
        if bound_id == 1:
            bound_point = "point_bound1"
        elif bound_id == 2:
            bound_point = "point_bound2"
            
        values = [0,0,0,0]
        values[0] = new_x
        values[1] = new_y
        dpg.set_value(bound_point,values)
        
    def bound1_input_changed(self):
        value = dpg.get_value("txt_bound1")
        self.update_bound(1,value,self.func(value))
        
    def bound2_input_changed(self):
        value = dpg.get_value("txt_bound2")
        self.update_bound(2,value,self.func(value))

    def redraw_bound_1(self):
        values = dpg.get_value("point_bound1")
        self.update_bound(1,values[0],self.func(values[0]))
        
    def redraw_bound_2(self):
        values = dpg.get_value("point_bound2")
        self.update_bound(2,values[0],self.func(values[0]))
        
    def update_plot_data(self):
        if self.func is None:
            return
        mouse_x = dpg.get_axis_limits("x_axis")
        dpg.set_axis_limits_auto("y_axis")
        x = np.linspace(mouse_x[0], mouse_x[1], 1000)
        y = self.func(x)
        dpg.set_value('function_line_plot', [x, y])
    
    def plot_cb(self):
        # Get the function string from txt_function
        func_str = dpg.get_value("txt_function")
        if func_str.isspace() or "x" not in func_str:
            dpg.configure_item("modal_invalid_exp", show=True)
            return
        
        self.parsed_equation = NonlinearEquation(func_str)
        if not self.parsed_equation.valid:
            dpg.configure_item("modal_invalid_exp", show=True)
            return
        
        self.func = self.parsed_equation.function
                

        x = np.linspace(-10, 10, 1000)
        y = self.func(x)

        # Draw the function on the plot
        dpg.configure_item("plot_window", show=True)
        self.remove_plot()
        dpg.add_line_series(x, y, label=func_str, parent="y_axis", tag="function_line_plot")
        dpg.add_drag_point(label="Bound 1",tag="point_bound1", color=[255, 0, 255, 255], default_value=(0, self.func(0)), callback=self.redraw_bound_1,parent="function_plot")
        dpg.add_drag_point(label="Bound 2",tag="point_bound2",thickness=0.5, color=[255, 0, 255, 255], default_value=(1, self.func(1)), callback=self.redraw_bound_2,parent="function_plot")
        dpg.set_value("txt_bound1",0)
        dpg.set_value("txt_bound2",1)
        dpg.bind_item_theme("function_line_plot", "plot_theme")
        min_val = min(y)
        max_val = max(y)
        added = (abs(min_val) + abs(max_val))/5
        dpg.set_axis_limits("y_axis", ymin=min_val-added,ymax= max_val+added)
        
    def solve_cb(self):
        try:
            dpg.delete_item("root_anot")
            method = dpg.get_value("method")
            
            # ["Bisection", "False-Position", "Fixed point", "First Modified Newton-Raphson", "Second Modified Newton-Raphson", "Secant Method"]
            precision = dpg.get_value("precision")
            max_iter = dpg.get_value("max_iter")
            abs_error = dpg.get_value("abs_error")
            sol = None
            steps = None
            fixed_point = False
            if method in ["Bisection", "False-Position"]:
                
                bracketing_solver = BracketingMethodsSolver(self.func,precision,max_iter)
                bound1 = dpg.get_value("txt_bound1")
                bound2 = dpg.get_value("txt_bound2")
                lower_bound, upper_bound = (bound1,bound2) if bound1 < bound2 else (bound2, bound1)
                tic = time.perf_counter()
                if method == "Bisection":
                    sol = bracketing_solver.bisection_method(lower_bound,upper_bound,abs_error)
                else:
                    sol =bracketing_solver.false_position_method(lower_bound,upper_bound,abs_error)
                    
                steps = bracketing_solver.steps
            elif method == "Fixed point":
                fixed_point = True
                g_x_str = dpg.get_value("g_x")
                if g_x_str.isspace() or "x" not in g_x_str:
                    dpg.configure_item("modal_invalid_exp", show=True)
                    return
                
                # Fix g(x) validation
                g_x_expression = NonlinearEquation(g_x_str)
                if not g_x_expression.valid:
                    dpg.configure_item("modal_invalid_exp", show=True)
                    return
                g_x_func = g_x_expression.function

                x0 = dpg.get_value("x0")
                fixed_point_solver = FixedPoint(self.func,g_x_func,x0,abs_error,precision,max_iter)
                tic = time.perf_counter()
                sol = fixed_point_solver.solve()
                steps = fixed_point_solver.steps
            elif method == "First Modified Newton-Raphson":
                x0 = dpg.get_value("x0")
                m = dpg.get_value("m")
                newton1_solver = NewtonRaphson(self.func,self.parsed_equation.derivative_function,x0,abs_error,precision,m,max_iter)
                tic = time.perf_counter()
                sol = newton1_solver.solve()
                steps = newton1_solver.steps
            elif method == "Second Modified Newton-Raphson":
                x0 = dpg.get_value("x0")
                m = dpg.get_value("m")
                newton2_solver = SecondNewtonRaphson(self.func,self.parsed_equation.derivative_function,self.parsed_equation.second_derivative_function,x0,abs_error,precision,max_iter)
                tic = time.perf_counter()
                sol = newton2_solver.solve()
                steps = newton2_solver.steps
            elif method == "Secant Method":
                x0 = dpg.get_value("x0")
                x1 = dpg.get_value("x1")
                secant_solver = SecantMethod(self.func,x0,x1,abs_error,max_iter,precision)
                tic = time.perf_counter()
                sol = secant_solver.solve()
                steps = secant_solver.steps
            else:
                return
            toc = time.perf_counter()
            if sol is None:
                if fixed_point:
                    dpg.set_value("solution_text","No solution found -- Divergent")
                else:
                    dpg.set_value("solution_text","No solution found")
            else:
                x= float(sol)
                y = self.func(x)
                dpg.add_plot_annotation(tag = "root_anot",label=f"Root = {x:.2f}", default_value=(x, y),parent="function_plot", offset=(-15, 15), color=[255, 255, 0, 255])
                dpg.set_value("solution_text",f"Root Found\n x = {str(sol)}\nRuntime : {(toc-tic):.6f}seconds")
                
            self.steps.clear_log()
            for step in steps:
                self.steps.log(str(step))
        except Exception as e:
            print(e)
            dpg.set_value("solution_text","No solution found -- Can't Solve")
        
        # Hide all inputs initially
        # dpg.configure_item("m", show=False)
        # dpg.configure_item("x0", show=False)
        # dpg.configure_item("x1", show=False)
        # dpg.configure_item("g_x", show=False)

        # Show inputs based on the selected method
        # if method == "Fixed point":
        #     dpg.configure_item("g_x", show=True)
        #     dpg.configure_item("x0", show=True)
        # elif method == "First Modified Newton-Raphson":
        #     dpg.configure_item("m", show=True)
        #     dpg.configure_item("x0", show=True)
        # elif method == "Second Modified Newton-Raphson":
        #     dpg.configure_item("x0", show=True)
        # elif method == "Secant Method":
        #     dpg.configure_item("x0", show=True)
        #     dpg.configure_item("x1", show=True)
