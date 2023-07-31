import gamelib as gamelib
from constants import *
from ui import show_paint
import logic as logic
import event_handler as event


def main():
    '''
    main function of the program
    shows the paint and handles the events
    '''
    gamelib.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
    paint = logic.new_paint()
    while gamelib.is_alive():
        show_paint(paint)
        ev = gamelib.wait()
        if not ev:
            break
        if ev.type == gamelib.EventType.ButtonPress and ev.mouse_button == 1:
            x, y = ev.x, ev.y
            if event.shortcut_color_clicked(x, y):
                logic.change_color_selected(paint, x)
            elif event.pixel_clicked(x, y) and paint['selected color'] != '':
                logic.change_pixel_color(paint, x, y)
            elif event.tool_bar_clicked(x, y):
                event.handle_tool_clicked(paint, x)
            elif event.upload_ppm_clicked(x, y):
                logic.load_as_ppm(paint)
            elif event.save_ppm_clicked(x, y):
                logic.save_as_ppm(paint)
            elif event.save_png_clicked(x, y):
                logic.save_as_png(paint)
            ev = gamelib.wait()
            if not ev:
                break
            while event.drag_painting(paint, x, y, ev):
                x, y = ev.x, ev.y
                logic.change_pixel_color(paint, x, y)
                show_paint(paint)
                ev = gamelib.wait()
                if not ev:
                    break

        


gamelib.init(main)
