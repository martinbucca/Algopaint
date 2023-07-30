from png import PNG_IMAGE_SIZE, write
import re
from stack import Stack
import gamelib    
from constants import *
from ui import show_paint




def calculate_pixel_position(i, j):
    '''Calculates the position of a pixel in the interface, centered.'''
    x1 = PIXEL_ZONE[0] + PIXEL_POSITION * i
    y1 = PIXEL_ZONE[1] + PIXEL_POSITION * j
    x2 = x1 + PIXEL_POSITION
    y2 = y1 + PIXEL_POSITION

    #x1 = WIDTH_CENTERED_PIXEL[0] - POSITION_RELATIVE_TO_SIZE * WIDTH_INITIAL_IMAGE + PIXEL_POSITION * i
    #y1 = HEIGHT_CENTERED_PIXEL[0] - POSITION_RELATIVE_TO_SIZE * HEIGHT_INITIAL_IMAGE + PIXEL_POSITION * j
    #x2 = WIDTH_CENTERED_PIXEL[1] - POSITION_RELATIVE_TO_SIZE * WIDTH_INITIAL_IMAGE + PIXEL_POSITION * i
    #y2 = HEIGHT_CENTERED_PIXEL[1] - POSITION_RELATIVE_TO_SIZE * HEIGHT_INITIAL_IMAGE + PIXEL_POSITION * j
    return x1, y1, x2, y2

def new_paint():
    '''Creates a new paint with the given width and height'''
    empty_image = {
        'header': 'Empty image',
        'width': WIDTH_INITIAL_IMAGE,
        'height': HEIGHT_INITIAL_IMAGE,
        'intensity': 255,
        'selected color': '',
        'entered color': '#ffffef',
        'bucket': False,
        'eraser': False,
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
    '''Saves an image in ppm format.'''
    name = gamelib.input('Save as:')
    if name == None: # close button
        return
    paint['header'] = name
    with open(name, 'w') as ppm:
        ppm.write(paint['header'] + '\n')
        ppm.write(str(paint['width']) + ' ' + str(paint['height']) + '\n')
        ppm.write(str(paint['intensity']) + '\n')
        for pixel in paint['pixels']:
            r, g, b = int(paint['pixels'][pixel]['color'][1:3], 16), int(paint['pixels'][pixel]['color'][3:5], 16), int(paint['pixels'][pixel]['color'][5:7], 16)             
            ppm.write(str(r) + ' ')
            ppm.write(str(g) + ' ')
            ppm.write(str(b) + '   ')
            if int(pixel.split(',')[1]) + 1 == paint['width']: # last of row
                ppm.write('\n') # to save it in the correct format
    
def load_as_ppm(paint):
    '''Opens an image in ppm format in the interface'''
    name = gamelib.input('Open PPM:')
    if name == None: # close button
        return
    try:
        ppm = open(name)
        file = []
        for line in ppm:
            file += line.rstrip().split() 
        paint['header'] = file[0]
        paint['width'], paint['height'] = int(file[1]), int(file[2])
        paint['intensity'] = int(file[3])
        paint['pixels'] = {}
        for j in range(paint['height']):
            for i in range(paint['width']):
                paint['pixels'][f'{j},{i}'] = {} # update the dictionary
        colors = file[4::] # rgb list of the file colors
        c = 0 
        for j in range(paint['height']):
            for i in range(0, len(colors)//paint['height'], 3):
                x1 = WIDTH_CENTERED_PIXEL[0] - POSITION_RELATIVE_TO_SIZE * paint['width']  + PIXEL_POSITION * i//3
                y1 = HEIGHT_CENTERED_PIXEL[0] - POSITION_RELATIVE_TO_SIZE * paint['height'] + PIXEL_POSITION * j
                x2 = WIDTH_CENTERED_PIXEL[1] - POSITION_RELATIVE_TO_SIZE * paint['width'] + PIXEL_POSITION * i//3
                y2 = HEIGHT_CENTERED_PIXEL[1] - POSITION_RELATIVE_TO_SIZE * paint['height'] + PIXEL_POSITION * j
                paint['pixels'][f'{j},{i//3}']['pos'] = (x1, y1, x2, y2)
                r, g, b = int(colors[c]), int(colors[c + 1]), int(colors[c + 2])
                paint['pixels'][f'{j},{i//3}']['color'] = '#' + f'{r:02x}' + f'{g:02x}' + f'{b:02x}'
                c += 3
        ppm.close()
    except (FileNotFoundError, IOError, EOFError,PermissionError, UnicodeDecodeError):
        gamelib.say(f'Error. The file {name} does not exist or can not be opened.')
    except ValueError:
        gamelib.say('Sorry. Something went wrong')

def save_as_png(paint):
    '''Save an image in png format.'''
    name = gamelib.input('Save as:')
    if name == None: # close button
        return
    palette = []
    image = []
    for pixel in paint['pixels']:
        r, g, b = int(paint['pixels'][pixel]['color'][1:3], 16), int(paint['pixels'][pixel]['color'][3:5], 16), int(paint['pixels'][pixel]['color'][5:7], 16)
        color =  (r, g, b)
        if color not in palette:
            palette.append(color)
    for j in range(paint['height']):
        image.append([])
        for i in range(paint['width']):
            r, g, b = int(paint['pixels'][f'{j},{i}']['color'][1:3], 16), int(paint['pixels'][f'{j},{i}']['color'][3:5], 16), int(paint['pixels'][f'{j},{i}']['color'][5:7], 16)
            for color in palette:
                if (r, g, b) == color:
                    image[j] += [palette.index(color)] * PNG_IMAGE_SIZE 
    final_image = []
    for i in range(len(image)):
        final_image += [image[i]] * PNG_IMAGE_SIZE  
    write(name, palette, final_image) 



def validate_color(color):
    '''Given a string, validates that it is a hexadecimal color.'''
    return bool(re.match(r'^#[0-9a-fA-F]{6}$', color))

def paint_around(pixel, paint, color):
    painted_pixels = ['BUCKET', []] # me guardo los pixeles pintados, el color anterior y el color al que fue pintado
    _paint_around(pixel, paint, color, painted_pixels)
    return painted_pixels

def _paint_around(pixel, paint, color, painted_pixels): #pixel = j,i
    '''Pinta un pixel si es del mismo color del color anterior al pixel que fue presionado.
    Se llama a si misma recursivamente.
    '''
    if int(pixel.split(',')[0]) < 0 or int(pixel.split(',')[0]) == paint['height'] or int(pixel.split(',')[1]) < 0 or int(pixel.split(',')[1]) == paint['width']:
        return
    if paint['pixels'][pixel]['color'] != color:
        return
    
    else:
        if paint['pixels'][pixel]['color'] == color:
            paint['pixels'][pixel]['color'] = paint['selected color']
            painted_pixels[1].append((pixel, color, paint['selected color'])) # (pixel pintado, color anterior, color pintado)        

        _paint_around(f'{int(pixel.split(",")[0]) + 1},{int(pixel.split(",")[1])}', paint, color, painted_pixels) #el de abajo
        _paint_around(f'{int(pixel.split(",")[0]) - 1},{int(pixel.split(",")[1])}', paint, color, painted_pixels) #el de arriba 
        _paint_around(f'{int(pixel.split(",")[0])},{int(pixel.split(",")[1]) + 1}', paint, color, painted_pixels) #el de la derecha
        _paint_around(f'{int(pixel.split(",")[0])},{int(pixel.split(",")[1]) - 1}', paint, color, painted_pixels) #el de la izquierda
        
def shortcut_color_clicked(x, y):
    '''Returns True if the shortcut color was clicked.'''
    return HEIGHT_COLOR_BAR[0] <= y <= HEIGHT_COLOR_BAR[1] and WIDTH_COLOR_BAR[0] <= x <= WIDTH_COLOR_BAR[1]

def clicked_color(x_click):
    '''Returns the color that was clicked. If no color was clicked, returns None.'''
    for i, color in enumerate(MAIN_COLORS):
        distance_to_first_color_x1 = (WIDTH_COLOR_BOX + SEPARATION_BETWEEN_COLORS) * i
        x1 = X1_FIRST_COLOR + distance_to_first_color_x1
        x2 = X1_FIRST_COLOR + WIDTH_COLOR_BOX + distance_to_first_color_x1
        if x1 <= x_click <= x2:
            return color
    return None     


def pixel_clicked(x, y):
    '''Returns True if a pixel was clicked.'''
    return PIXEL_ZONE[0] <= x <= PIXEL_ZONE[2] and PIXEL_ZONE[1] <= y <= PIXEL_ZONE[3]


def main():
    
    gamelib.title("AlgoPaint")
    gamelib.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
    paint = new_paint()
    done_actions = Stack()
    undone_actions = Stack()
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
                    undone_actions.clear() # if a color is clicked, the redo stack is cleared
                    paint['selected color'] = color
                    paint['bucket'] = paint['eraser'] = False # if bucket or eraser is active and a color is clicked, it is deactivated


            '''
            elif pixel_clicked(x, y):
            for pixel in paint['pixels']:
                
                x1, y1, x2, y2 = paint['pixels'][pixel]['pos'][0], paint['pixels'][pixel]['pos'][1], paint['pixels'][pixel]['pos'][2], paint['pixels'][pixel]['pos'][3]
                if x1 < x < x2 and y1 < y < y2 and paint['selected color'] != '':
                    if paint['bucket']:
                        color = paint['pixels'][pixel]['color']
                        done_actions.push(paint_around(pixel, paint, color))
                    
                    else:       
                        pos_pixel = paint['pixels'][pixel]['pos']
                        prev_color = paint['pixels'][pixel]['color']
                        paint['pixels'][pixel]['color'] = paint['selected color'] #se pinta el pixel del color seleccionado si es que se selecciono alguno.
                        post_color = paint['pixels'][pixel]['color']
                        done_actions.push((pos_pixel, prev_color, post_color)) #apilo la posicion del pixel el color antes de ser pintado y despues
            
            if INPUT_COLORS[0] <= x <= INPUT_COLORS[2] and INPUT_COLORS[1] <= y <= INPUT_COLORS[3]:
                while not undone_actions.empty():
                    undone_actions.pop()
                color = gamelib.input('Enter a color in hexadecimal code (#RRGGBB)')
                if color == None:
                    continue
                if not validate_color(color):
                    gamelib.say('Invalid color, you should enter something like this: #00ff23')
                else:
                    paint['entered color'] = color
                    paint['selected color'] = color
                    paint['bucket'] = False
                    

            if SAVE_PPM_BUTTON[0] < x <  SAVE_PPM_BUTTON[2] and SAVE_PPM_BUTTON[1] < y < SAVE_PPM_BUTTON[3]:
                while not undone_actions.empty():
                    undone_actions.pop()
                save_as_ppm(paint)

            if LOAD_PPM_BUTTON[0] < x <  LOAD_PPM_BUTTON[2] and LOAD_PPM_BUTTON[1] < y < LOAD_PPM_BUTTON[3]:
                while not undone_actions.empty():
                    undone_actions.pop()
                load_as_ppm(paint)

            if SAVE_PNG_BUTTON[0] < x <  SAVE_PNG_BUTTON[2] and SAVE_PNG_BUTTON[1] < y < SAVE_PNG_BUTTON[3]:
                while not undone_actions.empty(): 
                    undone_actions.pop()
                save_as_png(paint)

            if UNDO[0] < x < UNDO[2] and UNDO[1] < y < UNDO[3]:
                if not done_actions.empty(): #si esta vacia no hay acciones que deshacer
                    if done_actions.top()[0] != 'bucket': #si el primer elemento es BUCKET, se deben cambiar los colores de varios pixeles
                        for pixel in paint['pixels']:
                            if paint['pixels'][pixel]['pos'] == done_actions.top()[0]: 
                                paint['pixels'][pixel]['color'] = done_actions.top()[1] #le cambio el color al ultimo estado de ese color que es el tope
                                undone_actions.push(done_actions.pop())
                                break
                    else:
                        for pixel in done_actions.top()[1]:
                            paint['pixels'][pixel[0]]['color'] = pixel[1]
                        undone_actions.push(done_actions.pop())
                    

            if REDO[0] < x < REDO[2] and REDO[1] < y < REDO[3]:
                if not undone_actions.empty(): #si esta vacia no hay acciones que rehacer
                    if undone_actions.top()[0] != 'bucket':
                        for pixel in paint['pixels']:
                            if paint['pixels'][pixel]['pos'] == undone_actions.top()[0]: 
                                paint['pixels'][pixel]['color'] = undone_actions.top()[2] #le cambio el color al ultimo estado de ese color que es el tope
                                done_actions.push(undone_actions.pop())
                                break
                    else:
                        for pixel in undone_actions.top()[1]:
                            paint['pixels'][pixel[0]]['color'] = pixel[2]
                        done_actions.push(undone_actions.pop())
                    
            if BUCKET[0] < x < BUCKET[2] and BUCKET[1] < y < BUCKET[3]:
                while not undone_actions.empty():
                    undone_actions.pop()
                if paint['selected color'] != '':
                    paint['bucket'] = True #PARA ACTIVAR EL BUCKET PRIMERO TENES QUE TENER UN COLOR SELECCIONADO
         '''
        


gamelib.init(main)






