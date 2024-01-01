import dearpygui.dearpygui as dpg
from gui import SolverGUI

if __name__ == "__main__":
    dpg.create_context()

    # add a font registry
    with dpg.font_registry():
        # first argument ids the path to the .ttf or .otf file
        default_font = dpg.add_font("./assets/fonts/Retron2000.ttf", 20)
        
    dpg.bind_font(default_font)

    solver_gui = SolverGUI()
    solver_gui.create_windows()


    dpg.create_viewport(title='Root Finder', width=1150, height=638,x_pos=300,y_pos=300, 
                        small_icon=r'./assets/icons/algebra.png', 
                        large_icon=r'./assets/icons/algebra.ico')
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
