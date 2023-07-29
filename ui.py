from constants import *
import gamelib

def show_bucket(paint):
    '''Shows the bucket in the interface'''
    gamelib.draw_oval(BUCKET_HANDLE[0], BUCKET_HANDLE[1], BUCKET_HANDLE[2], BUCKET_HANDLE[3], fill=BACKGROUND_COLOR, width=3)
    fill_color = paint['selected color'] if paint['bucket'] else None
    outline_color = 'white' if paint['bucket'] else None
    bucket_width = 4 if paint['bucket'] else 1
    gamelib.draw_rectangle(BUCKET[0], BUCKET[1], BUCKET[2], BUCKET[3], fill=fill_color, outline=outline_color, width=bucket_width)

def show_undo_redo_buttons(paint):
    '''Shows the 'UNDO' and 'REDO' buttons in their respective positions of the paint'''
    gamelib.draw_rectangle(UNDO[0], UNDO[1], UNDO[2], UNDO[3], activeoutline='green')
    gamelib.draw_rectangle(REDO[0], REDO[1], REDO[2], REDO[3], activeoutline='green')
    gamelib.draw_text('UNDO', UNDO_TEXT[0], UNDO_TEXT[1], fill='black', bold=True, activefill='green')
    gamelib.draw_text('REDO',REDO_TEXT[0], REDO_TEXT[1], fill='black', bold=True, activefill='green')

def show_pixels(paint):
    '''Shows the pixels to draw in the interface, centered.'''
    for pixel in paint['pixels'].values():
        x1, y1, x2, y2 = pixel['pos']
        color = pixel['color']
        gamelib.draw_rectangle(x1, y1, x2, y2, fill=color)

def show_save_load_image_buttons(paint):
    '''Shows the buttons to load/save images in their respective positions of the paint'''
    gamelib.draw_rectangle(LOAD_PPM_BUTTON[0], LOAD_PPM_BUTTON[1], LOAD_PPM_BUTTON[2], LOAD_PPM_BUTTON[3], fill='white', activeoutline='green')
    gamelib.draw_rectangle(SAVE_PPM_BUTTON[0], SAVE_PPM_BUTTON[1], SAVE_PPM_BUTTON[2], SAVE_PPM_BUTTON[3], fill='white', activeoutline='green')
    gamelib.draw_rectangle(SAVE_PNG_BUTTON[0], SAVE_PNG_BUTTON[1], SAVE_PNG_BUTTON[2], SAVE_PNG_BUTTON[3], fill='white', activeoutline='green')
    gamelib.draw_text('Upload PPM',LOAD_PPM_TEXT[0], LOAD_PPM_TEXT[1], fill='black', activefill='green',bold=True)
    gamelib.draw_text('Save as PPM',SAVE_PPM_TEXT[0], SAVE_PPM_TEXT[1],fill='black', activefill='green',bold=True)
    gamelib.draw_text('Save as PNG',SAVE_PNG_TEXT[0], SAVE_PNG_TEXT[1],fill='black', activefill='green',bold=True)


def show_shortcut_colors(paint):
    '''Shows the shortcut colors in the interface'''
    for color in MAIN_COLORS:
        index_color = MAIN_COLORS.index(color)
        x1, x2 = COLOR_POSITION * index_color + WIDTH_COLOR[0], COLOR_POSITION * index_color + WIDTH_COLOR[1]
        outline = 'white' if color == paint['selected color'] else 'active'
        width = 4 if color == paint['selected color'] else 1
        gamelib.draw_rectangle(x1, HEIGHT_COLOR_BAR[0], x2, HEIGHT_COLOR_BAR[1], fill=color, outline=outline, width=width)


def show_input_color(paint):
    '''Shows the input color option in the interface'''
    gamelib.draw_rectangle(INPUT_COLORS[0], INPUT_COLORS[1], INPUT_COLORS[2], INPUT_COLORS[3], fill= '#ffffef', activeoutline='green')
    gamelib.draw_text('Pick another color', INPUT_COLORS_TEXT[0], INPUT_COLORS_TEXT[1], fill='black', bold=True, activefill='green', size = CHANGE_COLOR_FONT)
    if paint['entered color'] == paint['selected color']:       
        gamelib.draw_oval(COLOR_CIRCLE[0], COLOR_CIRCLE[1], COLOR_CIRCLE[2], COLOR_CIRCLE[3],fill= paint['selected color'], outline = 'white', width=4)


def show_paint(paint):
    '''Shows all the elements in the UI'''
    gamelib.draw_begin()
    # background and title.
    gamelib.draw_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, fill= BACKGROUND_COLOR)
    gamelib.draw_rectangle(0, 0, WINDOW_WIDTH, HEIGHT_TITLE, fill= TITLE_COLOR)
    gamelib.draw_text('AlgoPaint', WIDTH_TEXT_TITLE, HEIGHT_TEXT_TITLE, bold=True, fill = 'black')    
    # elements of UI
    show_shortcut_colors(paint)
    show_input_color(paint)
    show_pixels(paint)   
    show_save_load_image_buttons(paint)
    show_bucket(paint)
    show_undo_redo_buttons(paint)
    gamelib.draw_end()