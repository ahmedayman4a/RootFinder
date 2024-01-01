import dearpygui.dearpygui as dpg
from math import sin
import numpy as np

def update_plot_data():
    mouse_x = dpg.get_axis_limits("x_axis")
    x = np.linspace(mouse_x[0], mouse_x[1], 100)
    y = np.sin(x)
    dpg.set_value('series_1', [x, y])

dpg.create_context()

sindatax = []
sindatay = []
sindatax = np.linspace(-10, 10, 100)


# Calculate the new y values
sindatay = np.sin(sindatax)

with dpg.handler_registry():
    dpg.add_mouse_drag_handler(callback=update_plot_data)

def update_bound(bound_id,new_x,new_y):
    if bound_id == 1:
        dpg.set_value("txt_bound1",new_x)
    elif bound_id == 2:
        dpg.set_value("txt_bound2",new_x)
    redraw_bound(bound_id,new_x,new_y)
        
def func(x):
    return np.sin(x)
        
def redraw_bound(bound_id,new_x,new_y):
    if bound_id == 1:
        bound_point = "point_bound1"
    elif bound_id == 2:
        bound_point = "point_bound2"
        
    values = [0,0,0,0]
    values[0] = new_x
    values[1] = new_y
    dpg.set_value(bound_point,values)
    
def bound1_input_changed():
    value = dpg.get_value("txt_bound1")
    update_bound(1,value,func(value))
    
def bound2_input_changed():
    value = dpg.get_value("txt_bound2")
    update_bound(2,value,func(value))

def redraw_bound_1():
    values = dpg.get_value("point_bound1")
    update_bound(1,values[0],func(values[0]))
    
def redraw_bound_2():
    values = dpg.get_value("point_bound2")
    update_bound(2,values[0],func(values[0]))

with dpg.window(label="Tutorial", width=400, height=400):
    with dpg.theme(tag="plot_theme"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (60, 150, 200), category=dpg.mvThemeCat_Plots)
            
    with dpg.group(horizontal=True):
        dpg.add_text("Bound 1: ")
        dpg.add_input_double(tag="txt_bound1",default_value=1,width=100,callback=bound1_input_changed)
        dpg.add_spacer(width=30)
        dpg.add_text("Bound 2: ")
        dpg.add_input_double(tag="txt_bound2",default_value=1,width=100,callback=bound2_input_changed)
        
        
    
    
    # create plot
    dpg.add_text("Right click a series in the legend!")
    
    with dpg.plot(label="Line Series", height=-1, width=-1):
        dpg.add_plot_legend()

        dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="x_axis")
        dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")

        # series 1
        dpg.add_line_series(sindatax, sindatay, label="series 1", parent="y_axis", tag="series_1")
        dpg.add_button(label="Delete Series 1", parent=dpg.last_item(), callback=lambda: dpg.delete_item("series_1"))
        dpg.add_drag_point(label="Bound 1",tag="point_bound1", color=[255, 0, 255, 255], default_value=(0, 0), callback=redraw_bound_1)
        dpg.add_drag_point(label="Bound 2",tag="point_bound2",thickness=0.5, color=[255, 0, 255, 255], default_value=(1, np.sin(1)), callback=redraw_bound_2)
        dpg.bind_item_theme("series_1", "plot_theme")
        min = min(sindatay)
        max = max(sindatay)
        added = (abs(min) + abs(max))/5
        dpg.set_axis_limits("y_axis", ymin=min-added,ymax= max+added)
        

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()