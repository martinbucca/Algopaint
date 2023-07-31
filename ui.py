from utils.constants import *
import gamelib as gamelib

def show_title():
    '''
    Shows the title of the paint
    '''
    gamelib.draw_rectangle(0, 0, WINDOW_WIDTH, HEIGHT_TITLE, fill=TITLE_COLOR)
    gamelib.draw_image('icons/logo.ppm', 185, 4)
    gamelib.draw_text('ALGOPAINT', WIDTH_TEXT_TITLE,
                      HEIGHT_TEXT_TITLE, bold=True, fill='black')

def show_save_load_image_buttons(paint):
    '''
    Shows the buttons to load/save images in their respective positions of the paint
    '''
    gamelib.draw_rectangle(LOAD_PPM_BUTTON[0], HEIGHT_FILE_BUTTONS[0], LOAD_PPM_BUTTON[1],
                           HEIGHT_FILE_BUTTONS[1], fill='white', activeoutline='black', outline='black', activewidth=3)
    gamelib.draw_rectangle(SAVE_PPM_BUTTON[0], HEIGHT_FILE_BUTTONS[0], SAVE_PPM_BUTTON[1],
                           HEIGHT_FILE_BUTTONS[1], fill='white', activeoutline='black', outline='black', activewidth=3)
    gamelib.draw_rectangle(SAVE_PNG_BUTTON[0], HEIGHT_FILE_BUTTONS[0], SAVE_PNG_BUTTON[1],
                           HEIGHT_FILE_BUTTONS[1], fill='white', activeoutline='black', outline='black', activewidth=3)
    image_height = HEIGHT_FILE_TEXT - 12
    x_load_ppm = LOAD_PPM_BUTTON[0] + 2
    x_save_ppm = SAVE_PPM_BUTTON[0] + 3
    x_save_png = SAVE_PNG_BUTTON[0] + 3
    gamelib.draw_image('icons/upload.ppm', x_load_ppm, image_height)
    gamelib.draw_image('icons/save.ppm', x_save_ppm, image_height)
    gamelib.draw_image('icons/save.ppm', x_save_png, image_height)
    gamelib.draw_text('Upload PPM', X_LOAD_PPM_TEXT,
                      HEIGHT_FILE_TEXT, fill='black', bold=True)
    gamelib.draw_text('Save as PPM', X_SAVE_PPM_TEXT,
                      HEIGHT_FILE_TEXT, fill='black', bold=True)
    gamelib.draw_text('Save as PNG', X_SAVE_PNG_TEXT,
                      HEIGHT_FILE_TEXT, fill='black', bold=True)

def show_pixels(paint):
    '''
    Shows the pixels to draw in the interface.
    '''
    outline = 'black' if paint['pixeled'] else paint['selected color']
    for pixel in paint['pixels'].values():
        x1, y1, x2, y2 = pixel['pos']
        color = pixel['color']
        # either black (to see pixels) or the color of the pixel
        outline = 'black' if paint['pixeled'] else color
        gamelib.draw_rectangle(x1, y1, x2, y2, fill=color, outline=outline)

def show_shortcut_colors(paint):
    '''
    Shows the shortcut colors in the interface
    '''
    for i, color in enumerate(MAIN_COLORS):
        distance_to_first_color_x1 = (
            WIDTH_COLOR_BOX + SEPARATION_BETWEEN_COLORS) * i
        x1 = X1_FIRST_COLOR + distance_to_first_color_x1
        x2 = X1_FIRST_COLOR + WIDTH_COLOR_BOX + distance_to_first_color_x1
        if color == paint['selected color']:
            gamelib.draw_rectangle(
                x1, HEIGHT_COLOR_BAR[0], x2, HEIGHT_COLOR_BAR[1], fill=color, outline='black', width=4)
        else:
            gamelib.draw_rectangle(
                x1, HEIGHT_COLOR_BAR[0], x2, HEIGHT_COLOR_BAR[1], fill=color, activeoutline='black', activewidth=2)

def show_tool_bar(paint):
    '''
    Shows the tool bar in the interface
    '''
    show_undo_redo_buttons(paint)
    show_bucket(paint)
    show_eraser(paint)
    show_pixeled_option()
    show_trash()
    show_input_color(paint)

def show_undo_redo_buttons(paint):
    '''
    Shows the 'UNDO' and 'REDO' buttons in their respective positions of the paint
    '''
    gamelib.draw_rectangle(UNDO[0], HEIGHT_TOOL_BAR[0], UNDO[1], HEIGHT_TOOL_BAR[1],
                           outline='black', activeoutline='black', activewidth=3)
    x_undo_image = UNDO[0] + 6
    x_redo_image = REDO[0] + 6
    y_undo_image = y_redo_image = HEIGHT_TOOL_BAR[0] + 7
    gamelib.draw_image('icons/undo1.ppm', x_undo_image, y_undo_image)
    gamelib.draw_rectangle(REDO[0], HEIGHT_TOOL_BAR[0], REDO[1], HEIGHT_TOOL_BAR[1],
                           activeoutline='black', outline='black', activewidth=3)
    gamelib.draw_image('icons/redo1.ppm', x_redo_image, y_redo_image)

def show_bucket(paint):
    '''
    Shows the bucket in the interface
    '''
    bucket_width = 4 if paint['bucket'] else 1
    gamelib.draw_rectangle(BUCKET[0], HEIGHT_TOOL_BAR[0], BUCKET[1], HEIGHT_TOOL_BAR[1],
                           outline='black', width=bucket_width, activeoutline='black', activewidth=3)
    gamelib.draw_image('icons/bucket.ppm',
                       BUCKET[0] + 6, HEIGHT_TOOL_BAR[0] + 7)

def show_eraser(paint):
    '''
    Shows the erase button in the interface
    '''
    if paint['eraser']:
        gamelib.draw_rectangle(
            ERASER[0], HEIGHT_TOOL_BAR[0], ERASER[1], HEIGHT_TOOL_BAR[1], outline='black', width=4)
    else:
        gamelib.draw_rectangle(ERASER[0], HEIGHT_TOOL_BAR[0], ERASER[1],
                               HEIGHT_TOOL_BAR[1], outline='black', activeoutline='black', activewidth=3)
    gamelib.draw_image('icons/eraser.ppm',
                       ERASER[0] + 6, HEIGHT_TOOL_BAR[0] + 7)

def show_pixeled_option():
    '''
    Shows the pixeled/unpixeled button in the interface
    '''
    gamelib.draw_rectangle(PIXELED[0], HEIGHT_TOOL_BAR[0], PIXELED[1],
                           HEIGHT_TOOL_BAR[1], outline='black', activeoutline='black', activewidth=3)
    gamelib.draw_image('icons/border.ppm',
                       PIXELED[0] + 6, HEIGHT_TOOL_BAR[0] + 7)

def show_trash():
    '''
    Shows the trash button in the interface
    '''
    gamelib.draw_rectangle(TRASH[0], HEIGHT_TOOL_BAR[0], TRASH[1], HEIGHT_TOOL_BAR[1],
                           outline='black', activeoutline='black', activewidth=3)
    gamelib.draw_image('icons/trash.ppm',
                       TRASH[0] + 6, HEIGHT_TOOL_BAR[0] + 7)

def show_input_color(paint):
    '''
    Shows the input color option in the interface
    '''
    gamelib.draw_rectangle(INPUT_COLORS[0], HEIGHT_TOOL_BAR[0], INPUT_COLORS[1],
                           HEIGHT_TOOL_BAR[1], outline='black', activeoutline='black', activewidth=3)
    gamelib.draw_image('icons/palette.ppm',
                       INPUT_COLORS[0] + 6, HEIGHT_TOOL_BAR[0] + 7)
    
def show_custom_colors(paint):
    '''
    Shows the custom colors in the interface
    '''
    show_custom_color1(paint)
    show_custom_color2(paint)
    show_custom_color3(paint)
    
def show_custom_color1(paint):
    '''
    Shows the custom color 1 in the interface
    '''
    custom_color_selected = paint['custom colors selected'][0]
    custom_color = paint['custom colors'][0]
    if custom_color_selected and custom_color != 'white':
        gamelib.draw_rectangle(CUSTOM_COLOR_1[0], HEIGHT_TOOL_BAR[0], CUSTOM_COLOR_1[1],
                               HEIGHT_TOOL_BAR[1], fill=custom_color, outline='black', width=4)
    else:
        gamelib.draw_rectangle(CUSTOM_COLOR_1[0], HEIGHT_TOOL_BAR[0], CUSTOM_COLOR_1[1],
                               HEIGHT_TOOL_BAR[1], fill=custom_color, outline='black')
        
def show_custom_color2(paint):
    '''
    Shows the custom color 2 in the interface
    '''
    custom_color_selected = paint['custom colors selected'][1]
    custom_color = paint['custom colors'][1]
    if custom_color_selected and custom_color != 'white':
        gamelib.draw_rectangle(CUSTOM_COLOR_2[0], HEIGHT_TOOL_BAR[0], CUSTOM_COLOR_2[1],
                               HEIGHT_TOOL_BAR[1], fill=custom_color, outline='black', width=4)
    else:
        gamelib.draw_rectangle(CUSTOM_COLOR_2[0], HEIGHT_TOOL_BAR[0], CUSTOM_COLOR_2[1],
                               HEIGHT_TOOL_BAR[1], fill=custom_color, outline='black')
        
def show_custom_color3(paint):
    '''
    Shows the custom color 3 in the interface
    '''
    custom_color_selected = paint['custom colors selected'][2]
    custom_color = paint['custom colors'][2]
    if custom_color_selected and custom_color != 'white':
        gamelib.draw_rectangle(CUSTOM_COLOR_3[0], HEIGHT_TOOL_BAR[0], CUSTOM_COLOR_3[1],
                               HEIGHT_TOOL_BAR[1], fill=custom_color, outline='black', width=4)
    else:
        gamelib.draw_rectangle(CUSTOM_COLOR_3[0], HEIGHT_TOOL_BAR[0], CUSTOM_COLOR_3[1],
                               HEIGHT_TOOL_BAR[1], fill=custom_color, outline='black')





def show_paint(paint):
    '''Shows all the elements in the UI'''
    gamelib.draw_begin()
    # background
    gamelib.icon('icons/icon.ppm')
    gamelib.draw_rectangle(
        0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, fill=BACKGROUND_COLOR)
    show_title()
    # elements of UI
    show_save_load_image_buttons(paint)
    show_pixels(paint)
    show_shortcut_colors(paint)
    show_tool_bar(paint)
    show_custom_colors(paint)
    gamelib.draw_end()
