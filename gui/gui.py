import dearpygui.dearpygui as dpg
from gui.logger import CustomLogger
from mpmath import mp, matrix
import time
import numpy as np

# enum for keeping track of CurrentState = Plotter,Solver
class CurrentState:
    PLOTTER = 0
    SOLVER = 1

class SolverGUI:
    def __init__(self) -> None:
        self.set_theme()
        self.__create_menubar()
        self.func = None
        self.current_state = CurrentState.PLOTTER
    
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
                

    
    def create_windows(self):
        with dpg.window(tag="function_window", label="Function",pos=(0,30),height=140,width=1150):
            with dpg.group(horizontal=True):
                dpg.add_input_text(tag="txt_function",default_value="x**3+4",no_spaces=True,width=1105)
                dpg.add_text("= 0")
            dpg.add_slider_int(tag="precision",label="Precision",default_value=16,min_value=1,max_value=50,width=1055)
            with dpg.group(horizontal=True):
                # dpg.add_spacer(width=983)
                dpg.add_button(label="PLOT",tag="btn_plot",width=-1,callback=self.plot_cb)
                
        with dpg.window(tag="plot_window", label="Plot",pos=(0,180),width=1150,height=650, show=False):
            with dpg.theme(tag="plot_theme"):
                with dpg.theme_component(dpg.mvLineSeries):
                    dpg.add_theme_color(dpg.mvPlotCol_Line, (60, 150, 200), category=dpg.mvThemeCat_Plots)
            
            with dpg.group(horizontal=True):
                dpg.add_text("Bound 1: ")
                dpg.add_input_double(tag="txt_bound1",default_value=1,width=150,callback=self.bound1_input_changed)
                dpg.add_spacer(width=30)
                dpg.add_text("Bound 2: ")
                dpg.add_input_double(tag="txt_bound2",default_value=1,width=150,callback=self.bound2_input_changed)
                
            dpg.add_text("Right click to open plot settings")
            with dpg.plot(label="Function",tag="function_plot", height=500, width=-1,anti_aliased=True):
                dpg.add_plot_legend()

                dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="x_axis")
                dpg.add_plot_axis(dpg.mvYAxis, label="f(x)", tag="y_axis")
                
            dpg.add_button(label="SOLVE",tag="btn_solve",width=-1)

    def reset_gui(self,sender, app_data):
        # Destroy all existing windows
        dpg.delete_item("equations_window")
        dpg.delete_item("properties_window")
        dpg.delete_item("solution_window")
        dpg.delete_item("steps_window")
        self.current_state = CurrentState.PLOTTER
        # Recreate the windows
        self.create_windows()
    
    def remove_plot(self):
        dpg.delete_item("point_bound1")
        dpg.delete_item("point_bound2")
        dpg.delete_item("function_line_plot")
    
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
        if func_str.isspace():
            return
        
        dpg.configure_item("plot_window", show=True)
        
        self.func = eval("lambda x: " + func_str)

        x = np.linspace(-10, 10, 1000)
        y = self.func(x)

        # Draw the function on the plot
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
