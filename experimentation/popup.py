import dearpygui.dearpygui as dpg

dpg.create_context()

with dpg.window(label="Invalid Expression", modal=True, show=False, tag="modal_id"):
    dpg.add_text("The function you supplied is invalid\nPlease make sure that the expression is a valid non-linear equation in the expected format.")
    dpg.add_spacer(height=5)
    dpg.add_button(label="OK", width=-1, callback=lambda: dpg.configure_item("modal_id", show=False))

with dpg.window(label="Tutorial"):
    dpg.add_button(label="Open Dialog", callback=lambda: dpg.configure_item("modal_id", show=True))

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()