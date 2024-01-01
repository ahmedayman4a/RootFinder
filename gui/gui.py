
import dearpygui.dearpygui as dpg
from gui import CustomLogger
from parser.parser_noletter import Parser
from parser.parser_letter import Parser_Letter
from mpmath import mp, matrix
# from solvers.solver import Solver
# from solvers.solver_factory import SolverFactory
import time

class SolverGUI:
    def __init__(self) -> None:
        self.set_theme()
        self.__create_menubar()
    
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
                
    def on_scaling_changed(self, sender, app_data):
        if dpg.get_value("scaling"):
            dpg.set_value("letter_coefficients", False)

    def on_letter_coefficients_changed(self, sender, app_data):
        if dpg.get_value("letter_coefficients"):
            dpg.set_value("scaling", False)
                
    def validate_initial_guess(self,initial_guess):
        # Split the input string by commas
        initial_guess = initial_guess.split(',')

        # Convert the string elements to float
        try:
            initial_guess_mat = [float(num) for num in initial_guess]
        except ValueError:
            raise ValueError("Initial guess must be comma separated decimal numbers")

        # Convert the list to a mpmath matrix
        initial_guess_mp = matrix(initial_guess_mat)

        return initial_guess_mp
    
    def create_windows(self):
        with dpg.window(tag="equations_window", label="System of Equations",pos=(0,30),autosize=True):
            dpg.add_input_text(tag="equations",default_value="2*x+4*y=5\nx-8*y=15.5",multiline=True,no_spaces=True,width=580,height=176)

            with dpg.group(horizontal=True):
                dpg.add_spacer(width=423)
                dpg.add_button(label="SOLVE",width=150)
                
        with dpg.window(tag="solution_window", label="Solution",pos=(0,285),width=390,height=350):
                dpg.add_text(tag="solution_text")
        
        with dpg.window(tag="steps_window",label="Steps",pos=(395,285),width=750,height=350,):
            self.steps = CustomLogger(title="Steps",pos=(595,300),width=550,height=350,parent="steps_window")
            mat = [[1,0],[5,1]]
        
        with dpg.window(tag="properties_window",label="Properties",pos=(595,30),autosize=True):
            dpg.add_spacer(width=545)
            dpg.add_checkbox(label="Scaling", tag="scaling", callback=self.on_scaling_changed)
            dpg.add_checkbox(label="Letter Coefficients", tag="letter_coefficients", callback=self.on_letter_coefficients_changed)
    
            dpg.add_slider_int(tag="precision",label="Precision",default_value=16,min_value=1,max_value=50)
            dpg.add_combo(label = "Method",
                        tag="method",
                        items=["Gauss Elimination", "Gauss-Jordan", "LU Decomposition", "Gauss-Seidel", "Jacobi-Iteration"],
                        default_value="Gauss Elimination",
                        callback=self.on_method_changed)
            
            with dpg.group(label="LU Decomposition Settings",tag="lu_settings",show=False):
                dpg.add_combo(label = "LU Format",
                        tag="lu_format",
                        items=["Doolittle", "Crout", "Cholesky"],
                        default_value="Doolittle")
                
            with dpg.group(label="Iterative Methods Settings",tag="iter_settings",show=False):
                dpg.add_input_text(label = "Initial Guess",
                        tag="initial_guess",
                        default_value="1,1")
                
                with dpg.tooltip("initial_guess"):
                    dpg.add_text("Comma sperated decimal numbers.\nNumber of elements should match the number of equations.")
                    
                dpg.add_combo(label = "Stopping Condition",
                        tag="stop_condition",
                        items=["Number of Iterations", "Absolute Relative Error"],
                        default_value="Number of Iterations")
                
                #based on the stopping condition combo, show either a number_of_iterations input or absolute_relative_error input
                dpg.add_input_int(label="Number of Iterations", tag="number_of_iterations",default_value=50,max_value=500,min_value=1,min_clamped=True,max_clamped=True)
                dpg.add_input_float(label="Absolute Relative Error", tag="absolute_relative_error",default_value=0.001,step=0.001,format="%.6f",min_value=0.000001,min_clamped=True)


    def reset_gui(self,sender, app_data):
        # Destroy all existing windows
        dpg.delete_item("equations_window")
        dpg.delete_item("properties_window")
        dpg.delete_item("solution_window")
        dpg.delete_item("steps_window")
        # Recreate the windows
        self.create_windows()
    
    
        

    def on_method_changed(self, sender, app_data):
        selected_method = dpg.get_value(sender)
        if selected_method == "Gauss Elimination":
            dpg.configure_item("scaling", show=True)
            dpg.configure_item("letter_coefficients", show=True)
        else:
            dpg.configure_item("scaling", show=False)
            dpg.configure_item("letter_coefficients", show=False)
            
        if selected_method == "LU Decomposition":
            dpg.configure_item("lu_settings", show=True)
            dpg.configure_item("iter_settings", show=False)
        elif selected_method in ["Gauss-Seidel", "Jacobi-Iteration"]:
            dpg.configure_item("lu_settings", show=False)
            dpg.configure_item("iter_settings", show=True)
        else:
            dpg.configure_item("lu_settings", show=False)
            dpg.configure_item("iter_settings", show=False)