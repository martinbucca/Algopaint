from utils.png import PNG_IMAGE_SIZE, write
import re
from utils.stack import Stack
import gamelib as gamelib
from utils.constants import *
from ui import show_paint


def calculate_pixel_position(i, j):
    '''
    Calculates the position of a pixel in the interface
    '''
    x1 = PIXEL_ZONE[0] + PIXEL_SIZE * i
    y1 = PIXEL_ZONE[1] + PIXEL_SIZE * j
    x2 = x1 + PIXEL_SIZE
    y2 = y1 + PIXEL_SIZE
    return x1, y1, x2, y2


def new_paint():
    '''
    Creates a new paint. It is an empty image. It returns a dictionary with the paint data
    '''
    empty_image = {
        'header': 'Empty image',
        'width': WIDTH_INITIAL_IMAGE,
        'height': HEIGHT_INITIAL_IMAGE,
        'intensity': 255,
        'selected color': '',
        'entered color': 'white',
        'entered color selected': False,
        'bucket': False,
        'eraser': False,
        'pixeled': True,
        'done actions': Stack(),
        'undone actions': Stack(),
        'pixels': {
            f'{j},{i}': {
                'pos': calculate_pixel_position(i, j),
                'color': DEFAULT_PIXEL_COLOR,
            }
            for j in range(HEIGHT_INITIAL_IMAGE)
            for i in range(WIDTH_INITIAL_IMAGE)
        }
    }
    return empty_image


def save_as_ppm(paint):
    '''
    Saves an image in ppm format
    '''
    name = gamelib.input('Save as:')
    if name == None:  # close button
        return
    paint['header'] = name
    with open(name, 'w') as ppm:
        ppm.write(paint['header'] + '\n')
        ppm.write(str(paint['width']) + ' ' + str(paint['height']) + '\n')
        ppm.write(str(paint['intensity']) + '\n')
        for pixel in paint['pixels']:
            r, g, b = int(paint['pixels'][pixel]['color'][1:3], 16), int(
                paint['pixels'][pixel]['color'][3:5], 16), int(paint['pixels'][pixel]['color'][5:7], 16)
            ppm.write(str(r) + ' ')
            ppm.write(str(g) + ' ')
            ppm.write(str(b) + '   ')
            if int(pixel.split(',')[1]) + 1 == paint['width']:  # last of row
                ppm.write('\n')  # to save it in the correct format


def load_as_ppm(paint):
    '''
    Opens a ppm image in the interface
    '''
    name = gamelib.input('Open PPM:')
    if name == None:  # close button
        return
    try:
        image_ppm = open(name)
        file = image_ppm.read().split()
        paint['header'] = file[0]
        paint['width'] = int(file[1])
        paint['height'] = int(file[2])
        paint['intensity'] = int(file[3])
        paint['pixels'] = {}
        # update the dictionary with the new pixels
        for j in range(paint['height']):
            for i in range(paint['width']):
                paint['pixels'][f'{j},{i}'] = {}
        colors = file[4::]  # rgb list of the file colors
        offset = 0
        for j in range(paint['height']):
            for i in range(0, len(colors)//paint['height'], 3):
                x1 = PIXEL_ZONE[0] + PIXEL_SIZE * i//3
                y1 = PIXEL_ZONE[1] + PIXEL_SIZE * j
                x2 = x1 + PIXEL_SIZE
                y2 = y1 + PIXEL_SIZE
                pixel = f'{j},{i//3}'
                r, g, b = map(int, colors[offset:offset + 3])
                paint['pixels'][pixel]['pos'] = (x1, y1, x2, y2)
                paint['pixels'][pixel]['color'] = f'#{r:02x}{g:02x}{b:02x}'
                offset += 3
        image_ppm.close()
    except FileNotFoundError:
        gamelib.say(f'Error. The file "{name}" does not exist.')
    except (IOError, PermissionError, UnicodeDecodeError):
        gamelib.say(f'Error. The file "{name}" could not be opened or read.')
    except ValueError:
        gamelib.say('Sorry. Something went wrong.')


def save_as_png(paint):
    '''
    Save an image in png format
    '''
    name = gamelib.input('Save as:')
    if name == None:  # close button
        return
    palette = []
    image = []
    for pixel in paint['pixels']:
        r, g, b = int(paint['pixels'][pixel]['color'][1:3], 16), int(
            paint['pixels'][pixel]['color'][3:5], 16), int(paint['pixels'][pixel]['color'][5:7], 16)
        color = (r, g, b)
        if color not in palette:
            palette.append(color)
    for j in range(paint['height']):
        image.append([])
        for i in range(paint['width']):
            r, g, b = int(paint['pixels'][f'{j},{i}']['color'][1:3], 16), int(
                paint['pixels'][f'{j},{i}']['color'][3:5], 16), int(paint['pixels'][f'{j},{i}']['color'][5:7], 16)
            for color in palette:
                if (r, g, b) == color:
                    image[j] += [palette.index(color)] * PNG_IMAGE_SIZE
    final_image = []
    for i in range(len(image)):
        final_image += [image[i]] * PNG_IMAGE_SIZE
    write(name, palette, final_image)


def validate_color(color):
    '''
    Given a string, validates that it is a hexadecimal color
    '''
    return bool(re.match(r'^#[0-9a-fA-F]{6}$', color))


def paint_around(pixel, paint, curr_color):
    '''
    Given a pixel and a color, paints the pixels around that have the same color as the pixel 
    to the current selected color in the paint
    '''
    # me guardo los pixeles pintados, el color anterior y el color al que fue pintado
    painted_pixels = {'prev color': curr_color,
                      'post color': paint['selected color'], 'pixels changed': []}
    paint_around_pixel(pixel, paint, curr_color, painted_pixels)
    return painted_pixels


def paint_around_pixel(pixel, paint, color, painted_pixels):  # pixel = j,i
    '''Paints a pixel if it is the same color as the previous color of the pixel that was pressed.'''
    if int(pixel.split(',')[0]) < 0 or int(pixel.split(',')[0]) == paint['height'] or int(pixel.split(',')[1]) < 0 or int(pixel.split(',')[1]) == paint['width']:
        return
    if paint['pixels'][pixel]['color'] != color:
        return

    else:
        if paint['pixels'][pixel]['color'] == color:
            paint['pixels'][pixel]['color'] = paint['selected color']
            painted_pixels['pixels changed'].append(pixel)  # painted pixel

        paint_around_pixel(
            f'{int(pixel.split(",")[0]) + 1},{int(pixel.split(",")[1])}', paint, color, painted_pixels)  # down
        paint_around_pixel(
            f'{int(pixel.split(",")[0]) - 1},{int(pixel.split(",")[1])}', paint, color, painted_pixels)  # up
        paint_around_pixel(
            f'{int(pixel.split(",")[0])},{int(pixel.split(",")[1]) + 1}', paint, color, painted_pixels)  # rigth
        paint_around_pixel(
            f'{int(pixel.split(",")[0])},{int(pixel.split(",")[1]) - 1}', paint, color, painted_pixels)  # left


def shortcut_color_clicked(x, y):
    '''
    Returns True if a shortcut color was clicked
    '''
    return HEIGHT_COLOR_BAR[0] <= y <= HEIGHT_COLOR_BAR[1] and WIDTH_COLOR_BAR[0] <= x <= WIDTH_COLOR_BAR[1]


def clicked_color(x_click):
    '''Returns the color that was clicked. If no color was clicked, returns None.'''
    for i, color in enumerate(MAIN_COLORS):
        distance_to_first_color_x1 = (
            WIDTH_COLOR_BOX + SEPARATION_BETWEEN_COLORS) * i
        x1 = X1_FIRST_COLOR + distance_to_first_color_x1
        x2 = X1_FIRST_COLOR + WIDTH_COLOR_BOX + distance_to_first_color_x1
        if x1 <= x_click <= x2:
            return color
    return None


def pixel_clicked(x, y):
    '''Returns True if a pixel was clicked.'''
    x2 = PIXEL_ZONE[0] + PIXEL_SIZE * WIDTH_INITIAL_IMAGE
    y2 = PIXEL_ZONE[1] + PIXEL_SIZE * HEIGHT_INITIAL_IMAGE
    return PIXEL_ZONE[0] <= x <= x2 and PIXEL_ZONE[1] <= y <= y2


def tool_bar_clicked(x, y):
    '''Returns True if the tool bar was clicked.'''
    return HEIGHT_TOOL_BAR[0] <= y <= HEIGHT_TOOL_BAR[1] and UNDO[0] <= x <= INPUT_COLOR[1]


def undo_last_action(paint):
    if not paint['done actions'].empty():  # if there is an action to undo
        last_action = paint['done actions'].get_top()
        for pixel in last_action['pixels changed']:
            prev_color = last_action['prev color']
            paint['pixels'][pixel]['color'] = prev_color
        paint['undone actions'].push(paint['done actions'].pop())


def redo_last_action(paint):
    if not paint['undone actions'].empty():  # if there is an action to redo
        last_action = paint['undone actions'].get_top()
        for pixel in last_action['pixels changed']:
            post_color = last_action['post color']
            paint['pixels'][pixel]['color'] = post_color
        paint['done actions'].push(paint['undone actions'].pop())


def main():

    gamelib.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
    paint = new_paint()
    while gamelib.is_alive():
        show_paint(paint)
        ev = gamelib.wait()
        if not ev:
            break
        if ev.type == gamelib.EventType.ButtonPress and ev.mouse_button == 1:
            x, y = ev.x, ev.y
            if shortcut_color_clicked(x, y):
                color = clicked_color(x)
                if color:
                    paint['selected color'] = color
                    # if bucket or eraser is active and a color is clicked, it is deactivated
                    paint['bucket'] = paint['eraser'] = paint['entered color selected'] = False
                    paint['undone actions'].clear()  # if a color is clicked, the redo stack is cleared
            elif pixel_clicked(x, y) and paint['selected color'] != '':
                for pixel, pixel_data in paint['pixels'].items():
                    x1, y1, x2, y2 = pixel_data['pos']
                    if x1 < x < x2 and y1 < y < y2:
                        if paint['bucket']:
                            current_color = pixel_data['color']
                            paint['done actions'].push(paint_around(
                                pixel, paint, current_color))
                        else:
                            prev_color = pixel_data['color']
                            pixel_data['color'] = paint['selected color']
                            post_color = pixel_data['color']
                            paint['done actions'].push(
                                {'prev color': prev_color, 'post color': post_color, 'pixels changed': [pixel]})
            elif tool_bar_clicked(x, y):
                if UNDO[0] < x < UNDO[1]:
                    undo_last_action(paint)
                elif REDO[0] < x < REDO[1]:
                    redo_last_action(paint)
                elif BUCKET[0] < x < BUCKET[1]:
                    if paint['selected color'] != '':
                        # to activate the bucket you must first have a selected color
                        paint['bucket'] = True
                    paint['undone actions'].clear()  # if bucket is clicked, the redo stack is cleared
                elif ERASER[0] < x < ERASER[1]:
                    paint['eraser'] = True
                    paint['selected color'] = DEFAULT_PIXEL_COLOR
                    paint['bucket'] = paint['entered color selected'] = False
                    paint['undone actions'].clear()  # if a eraser is clicked, the redo stack is cleared
                elif PIXELED[0] < x < PIXELED[1]:
                    paint['pixeled'] = not paint['pixeled']
                elif INPUT_COLORS[0] < x < INPUT_COLORS[1]:
                    color = gamelib.input(
                        'Enter a color in hexadecimal code (#RRGGBB)')
                    if color == None:
                        continue
                    if not validate_color(color):
                        gamelib.say(
                            'Invalid color, you should enter something like this: #00ff23')
                    else:
                        paint['entered color'] = paint['selected color'] = color
                        paint['entered color selected'] = True
                        paint['bucket'] = paint['eraser'] = False
                    paint['undone actions'].clear()  # if a color is clicked, the redo stack is cleared
                elif INPUT_COLOR[0] < x < INPUT_COLOR[1]:
                    paint['entered color selected'] = True
                    paint['selected color'] = paint['entered color']
                    paint['bucket'] = paint['eraser'] = False
                    paint['undone actions'].clear()  # if a color is clicked, the redo stack is cleared

            elif LOAD_PPM_BUTTON[0] < x < LOAD_PPM_BUTTON[1] and HEIGHT_FILE_BUTTONS[0] < y < HEIGHT_FILE_BUTTONS[1]:
                load_as_ppm(paint)
                paint['undone actions'].clear()
            elif SAVE_PPM_BUTTON[0] < x < SAVE_PPM_BUTTON[1] and HEIGHT_FILE_BUTTONS[0] < y < HEIGHT_FILE_BUTTONS[1]:
                save_as_ppm(paint)
                paint['undone actions'].clear()
            elif SAVE_PNG_BUTTON[0] < x < SAVE_PNG_BUTTON[1] and HEIGHT_FILE_BUTTONS[0] < y < HEIGHT_FILE_BUTTONS[1]:
                save_as_png(paint)
                paint['undone actions'].clear()


gamelib.init(main)
