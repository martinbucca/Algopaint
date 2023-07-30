from constants import *
import gamelib


def show_save_load_image_buttons(paint):
    '''Shows the buttons to load/save images in their respective positions of the paint'''
    gamelib.draw_rectangle(LOAD_PPM_BUTTON[0], HEIGHT_FILE_BUTTONS[0], LOAD_PPM_BUTTON[1], HEIGHT_FILE_BUTTONS[1], fill='white', activeoutline='black', outline='black', activewidth=3)
    gamelib.draw_rectangle(SAVE_PPM_BUTTON[0], HEIGHT_FILE_BUTTONS[0], SAVE_PPM_BUTTON[1], HEIGHT_FILE_BUTTONS[1], fill='white', activeoutline='black', outline='black', activewidth=3)
    gamelib.draw_rectangle(SAVE_PNG_BUTTON[0], HEIGHT_FILE_BUTTONS[0], SAVE_PNG_BUTTON[1], HEIGHT_FILE_BUTTONS[1], fill='white', activeoutline='black', outline='black', activewidth=3)
    image_height = HEIGHT_FILE_TEXT - 12
    x_load_ppm = LOAD_PPM_BUTTON[0] + 2
    x_save_ppm = SAVE_PPM_BUTTON[0] + 3
    x_save_png = SAVE_PNG_BUTTON[0] + 3
    gamelib.draw_image('assets/images/upload.ppm', x_load_ppm, image_height)
    gamelib.draw_image('assets/images/save.ppm', x_save_ppm, image_height)
    gamelib.draw_image('assets/images/save.ppm', x_save_png, image_height)
    gamelib.draw_text('Upload PPM',X_LOAD_PPM_TEXT, HEIGHT_FILE_TEXT, fill='black', bold=True)
    gamelib.draw_text('Save as PPM',X_SAVE_PPM_TEXT, HEIGHT_FILE_TEXT,fill='black', bold=True)
    gamelib.draw_text('Save as PNG',X_SAVE_PNG_TEXT, HEIGHT_FILE_TEXT,fill='black', bold=True)

def show_pixels(paint):
    '''Shows the pixels to draw in the interface, centered.'''
    for pixel in paint['pixels'].values():
        x1, y1, x2, y2 = pixel['pos']
        color = pixel['color']
        gamelib.draw_rectangle(x1, y1, x2, y2, fill=color, outline='black')

def show_shortcut_colors(paint):
    '''Shows the shortcut colors in the interface'''
    for i, color in enumerate(MAIN_COLORS):
        distance_to_first_color_x1 = (WIDTH_COLOR_BOX + SEPARATION_BETWEEN_COLORS) * i
        x1 = X1_FIRST_COLOR + distance_to_first_color_x1
        x2 = X1_FIRST_COLOR + WIDTH_COLOR_BOX + distance_to_first_color_x1
        if color == paint['selected color']:
            gamelib.draw_rectangle(x1, HEIGHT_COLOR_BAR[0], x2, HEIGHT_COLOR_BAR[1] , fill = color, outline='black', width=4 )
        else:
            gamelib.draw_rectangle(x1, HEIGHT_COLOR_BAR[0], x2, HEIGHT_COLOR_BAR[1] , fill = color, activeoutline='black', activewidth=2)




def show_tool_bar(paint):
    '''Shows the tool bar in the interface'''
    show_undo_redo_buttons(paint)
    show_bucket(paint)
    show_eraser(paint)
    show_input_color(paint)


def show_undo_redo_buttons(paint):
    '''Shows the 'UNDO' and 'REDO' buttons in their respective positions of the paint'''
    gamelib.draw_rectangle(UNDO[0], HEIGHT_TOOL_BAR[0], UNDO[1], HEIGHT_TOOL_BAR[1], outline='black', activeoutline='black', activewidth=3)
    x_undo_image = UNDO[0] + 6
    x_redo_image = REDO[0] + 6
    y_undo_image = y_redo_image = HEIGHT_TOOL_BAR[0] + 4
    gamelib.draw_image('assets/images/undo1.ppm', x_undo_image, y_undo_image)
    gamelib.draw_rectangle(REDO[0], HEIGHT_TOOL_BAR[0], REDO[1], HEIGHT_TOOL_BAR[1], activeoutline='black', outline='black', activewidth=3)
    gamelib.draw_image('assets/images/redo1.ppm', x_redo_image, y_redo_image)

def show_bucket(paint):
    '''Shows the bucket in the interface'''
    fill_color = paint['selected color'] if paint['bucket'] else 'white'
    outline_color = 'white' if paint['bucket'] else 'black'
    bucket_width = 4 if paint['bucket'] else 1
    gamelib.draw_rectangle(BUCKET[0], HEIGHT_TOOL_BAR[0], BUCKET[1], HEIGHT_TOOL_BAR[1], fill=fill_color, outline=outline_color, width=bucket_width, activeoutline='black', activewidth=3)
    gamelib.draw_image('assets/images/bucket.ppm', BUCKET[0] + 6, HEIGHT_TOOL_BAR[0] + 4)

def show_eraser(paint):
    '''Shows the erase button in the interface'''
    if paint['eraser']:
        gamelib.draw_rectangle(ERASER[0], HEIGHT_TOOL_BAR[0], ERASER[1], HEIGHT_TOOL_BAR[1], outline='black', width=4)
    else:
        gamelib.draw_rectangle(ERASER[0], HEIGHT_TOOL_BAR[0], ERASER[1], HEIGHT_TOOL_BAR[1], outline='black', activeoutline='black', activewidth=3)
    gamelib.draw_image('assets/images/eraser.ppm', ERASER[0] + 6, HEIGHT_TOOL_BAR[0] + 4)

def show_input_color(paint):
    '''Shows the input color option in the interface'''
    gamelib.draw_image('assets/images/palette.ppm', INPUT_COLORS[0] + 6, HEIGHT_TOOL_BAR[0] + 4)
    if paint['entered color selected'] and paint['entered color'] != 'white':
        gamelib.draw_rectangle(INPUT_COLOR[0], HEIGHT_TOOL_BAR[0], INPUT_COLOR[1], HEIGHT_TOOL_BAR[1],fill=paint['entered color'], outline = 'black', width=4)
    else:       
        gamelib.draw_rectangle(INPUT_COLOR[0], HEIGHT_TOOL_BAR[0], INPUT_COLOR[1], HEIGHT_TOOL_BAR[1],fill=paint['entered color'], outline = 'black')






def show_paint(paint):
    '''Shows all the elements in the UI'''
    gamelib.draw_begin()
    # background and title.
    gamelib.icon('assets/images/icon.ppm')
    gamelib.draw_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, fill= BACKGROUND_COLOR)
    gamelib.draw_rectangle(0, 0, WINDOW_WIDTH, HEIGHT_TITLE, fill= TITLE_COLOR)
    gamelib.draw_text('AlgoPaint', WIDTH_TEXT_TITLE, HEIGHT_TEXT_TITLE, bold=True, fill = 'black')    
    # elements of UI
    show_save_load_image_buttons(paint)
    show_pixels(paint)  
    show_shortcut_colors(paint)
    show_tool_bar(paint)
    gamelib.draw_end()