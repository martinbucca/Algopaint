import gamelib as gamelib
from utils.constants import *
import logic as logic


def save_ppm_clicked(x, y):
    '''
    Returns True if the save ppm button in the window was clicked.
    False otherwise
    '''
    return SAVE_PPM_BUTTON[0] < x < SAVE_PPM_BUTTON[1] and HEIGHT_FILE_BUTTONS[0] < y < HEIGHT_FILE_BUTTONS[1]


def save_png_clicked(x, y):
    '''
    Returns True if the save png button in the window was clicked.
    False otherwise
    '''
    return SAVE_PNG_BUTTON[0] < x < SAVE_PNG_BUTTON[1] and HEIGHT_FILE_BUTTONS[0] < y < HEIGHT_FILE_BUTTONS[1]


def upload_ppm_clicked(x, y):
    '''
    Returns True if the upload ppm button in the window was clicked.
    False otherwise
    '''
    return LOAD_PPM_BUTTON[0] < x < LOAD_PPM_BUTTON[1] and HEIGHT_FILE_BUTTONS[0] < y < HEIGHT_FILE_BUTTONS[1]


def pixel_clicked(x, y):
    '''
    Returns True if any pixel in the window was clicked.
    False otherwise
    '''
    x2 = PIXEL_ZONE[0] + PIXEL_SIZE * WIDTH_INITIAL_IMAGE
    y2 = PIXEL_ZONE[1] + PIXEL_SIZE * HEIGHT_INITIAL_IMAGE
    return PIXEL_ZONE[0] <= x <= x2 and PIXEL_ZONE[1] <= y <= y2


def tool_bar_clicked(x, y):
    '''
    Returns True if any tool of the tool bar in the window was clicked.
    False otherwise
    '''
    return HEIGHT_TOOL_BAR[0] <= y <= HEIGHT_TOOL_BAR[1] and UNDO[0] <= x <= CUSTOM_COLOR_3[1]


def shortcut_color_clicked(x, y):
    '''
    Returns True if any shortcut color in the window was clicked.
    False otherwise
    '''
    return HEIGHT_COLOR_BAR[0] <= y <= HEIGHT_COLOR_BAR[1] and WIDTH_COLOR_BAR[0] <= x <= WIDTH_COLOR_BAR[1]


def undo_clicked(x):
    '''
    Returns True if the undo button in the window was clicked.
    False otherwise
    '''
    return UNDO[0] < x < UNDO[1]


def redo_clicked(x):
    '''
    Returns True if the redo button in the window was clicked.
    False otherwise
    '''
    return REDO[0] < x < REDO[1]


def bucket_clicked(x):
    '''
    Returns True if the bucket button in the window was clicked.
    False otherwise
    '''
    return BUCKET[0] < x < BUCKET[1]


def eraser_clicked(x):
    '''
    Returns True if the eraser button in the window was clicked.
    False otherwise
    '''
    return ERASER[0] < x < ERASER[1]


def trash_clicked(x):
    '''
    Returns True if the trash button in the window was clicked.
    False otherwise
    '''
    return TRASH[0] < x < TRASH[1]


def pixeled_clicked(x):
    '''
    Returns True if the pixeled/unpixeled button in the window was clicked.
    False otherwise
    '''
    return PIXELED[0] < x < PIXELED[1]


def input_colors_clicked(x):
    '''
    Returns True if the button to selecte a custom color in the window was clicked.
    False otherwise
    '''
    return INPUT_COLORS[0] < x < INPUT_COLORS[1]


def custom_color1_clicked(x):
    '''
    Returns True if the custom color button in the window was clicked.
    False otherwise
    '''
    return CUSTOM_COLOR_1[0] < x < CUSTOM_COLOR_1[1]


def custom_color2_clicked(x):
    '''
    Returns True if the custom color button in the window was clicked.
    False otherwise
    '''
    return CUSTOM_COLOR_2[0] < x < CUSTOM_COLOR_2[1]


def custom_color3_clicked(x):
    '''
    Returns True if the custom color button in the window was clicked.
    False otherwise
    '''
    return CUSTOM_COLOR_3[0] < x < CUSTOM_COLOR_3[1]


def handle_tool_clicked(paint, x):
    '''
    Handles the event of a tool being clicked in the window according to the x coordinate
    if none of the tools was clicked, nothing happens
    '''
    if undo_clicked(x):
        logic.undo_last_action(paint)
    elif redo_clicked(x):
        logic.redo_last_action(paint)
    elif bucket_clicked(x):
        logic.activate_bucket(paint)
        # if bucket is clicked, the redo stack is cleared
        paint['undone actions'].clear()
    elif eraser_clicked(x):
        logic.activate_eraser(paint)
        # if a eraser is clicked, the redo stack is cleared
        paint['undone actions'].clear()
    elif trash_clicked(x):
        logic.clear_paint(paint)
        # if trash is clicked, the redo stack is cleared
        paint['undone actions'].clear()
    elif pixeled_clicked(x):
        paint['pixeled'] = not paint['pixeled']
    elif input_colors_clicked(x):
        logic.select_custom_color(paint)
        # if a color is clicked, the redo stack is cleared
        paint['undone actions'].clear()
    elif custom_color1_clicked(x):
        logic.change_color_to_custom(paint, 0)
        # if a color is clicked, the redo stack is cleared
        paint['undone actions'].clear()
    elif custom_color2_clicked(x):
        logic.change_color_to_custom(paint, 1)
        paint['undone actions'].clear()
    elif custom_color3_clicked(x):
        logic.change_color_to_custom(paint, 2)
        paint['undone actions'].clear()
