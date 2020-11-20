from platform import system
from colors import *
from button import Button, arc, roundrect
from solar_objects import *
from solar_input import *
from solar_model import *
from solar_vis import *

import pygame as pg
import pygame.draw as pgd
import math as m
import os.path

#defining how many hard drives exist
current_system = system()
dr = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
drives = ['%s:'%d for d in dr if os.path.exists('%s:'%d)]

"""
this file contains:
    class Menu(for buttons and interaction)
    functions which work with paths and file(for input and output data)
    
"""

pg.init()
pg.font.init()
font = pg.font.Font(None, 30)

FPS = 60
size = (800, 800)
screen = pg.display.set_mode(size)
pg.display.set_caption('Solar system')


"""
class Menu constants:
    width - if you wanna the menu will be transparent, make it non-zero int
    Rect = ((x, y), (length, height))
    colors = (menu_color, text_color, background)
functions:
    add_buttons - if new buttons appear, it will add them
    app - show on screen n update
"""
class Menu:
    width = 0
    Rect = ((10, 10), (100, 150))
    colors = (YELLOW, RED, BLACK)
    def __init__(self, screen, r=20):
        self.screen = screen
        self.Rect = Menu.Rect
        self.colors = Menu.colors
        self.width = Menu.width
        self.b_r = r
        self.buttons = []
        self.active = False
                
    def add_buttons(self, buttons):
        self.buttons = []
        for button in buttons:
            self.buttons.append(button)
                
    def app(self, m_pos):
        pgd.rect(self.screen, BLACK, self.Rect)
        roundrect(self.screen, (self.colors[0], self.colors[2]), self.Rect, self.width, self.b_r)
        for button in self.buttons:
            button.app(BLACK, m_pos)


"""
functions:
    get_files - gets all the files from a dir and makes buttons with files'
                names
    count_slash - counts slashes in path(type=str). it is used for moving 
                  through dirs
    level_up - when '. . .' button is pushed
    shape - makes a path proccessable
    define_format - is used when we wanna open or save a file
    file_menu_actions - is created for readability
"""
def convert_x(obj, x_list, size):
    max_x = max(x_list)
    x = size[0]//2 + ((size[0]-10)*obj.x)//(2*max_x)
    return int(x)

def convert_y(obj, y_list, size):
    max_y = max(y_list)
    y = size[1]//2 + ((size[1]-10)*obj.y)//(2*max_y)
    return int(y)

def convert_Vy(obj, Vy_list):
    max_Vy = max(Vy_list)
    Vy = 20 + (20*obj.Vy)//(2*max_Vy)
    return int(Vy)
    
def minus(string):
    new_string = ''
    for i in range(len(string)-1):
        new_string += string[i]
    return new_string


def get_files(directory, menu, up, down):
    files = os.listdir(directory)
    buttons = [button_return, button_scrolld, button_scrollu]
    x, y, l, h = menu.Rect[0][0]+10, menu.Rect[0][1]+60, 300, 20
    for i in range(up-1, min(len(files), down)):
        buttons.append(Button(screen, x, y, l, h, (RED, BLACK), files[i], 5))
        y += 30
    return buttons
    
    
def count_slash(directory):
    k = 0
    for elem in directory:
        if elem == '/':
            k += 1
    return k
    
    
def level_up(directory, slash):
    new_dir = ''
    i = 0
    for elem in directory:
        if elem == '/':
            i += 1
        if i != slash:
            new_dir += elem
        else:
            break
    return new_dir

    
def shape(directory):
    list_dir = list(directory)
    new_dir = ''
    for elem in list_dir:
        if elem == '\\':
            new_dir += '/'
        else:
            new_dir += elem
    return new_dir


def define_format(directory):
    formatt = '.'
    k = 0
    for i in range(1, len(directory)+1):
        if directory[-i] != '.':
            k += 1
        else:
            break
    for i in range(k):
        formatt += directory[len(directory)-k+i]
    return formatt


def file_menu_actions(event, menu, mouse_pos, directory, act_file, up, down, hard_menu):
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        for button in hard_menu.buttons:
            if button.check_pos(mouse_pos):
                up, down = 1, 14
                directory = button.button_text+'/'
                menu.buttons = get_files(directory, menu, up, down)
        for button in menu.buttons:
            if button.check_pos(mouse_pos):
                slash = count_slash(directory)
                if button.button_text == '. . .':
                    up, down = 1, 14
                    new_dir = level_up(directory, slash)
                    directory = new_dir
                    if directory[-1] == ':':
                        directory += '/'
                    elif len(directory) == 0:
                        if current_system == 'Linux':
                            directory += '/home'
                        else:
                            directory += '/Users'
                    menu.buttons = get_files(directory, menu, up, down)
                    screen.fill(BLACK)
                else:
                    if os.path.isfile(directory+'/'+button.button_text):
                        pass
                    elif button.button_text == 'SCROLL DOWN':
                        if down < len(os.listdir(directory))-1:
                            up += 1
                            down += 1
                            menu.buttons = get_files(directory, menu, up, down)
                    elif button.button_text == 'SCROLL UP':
                        if up > 1:
                            up -= 1
                            down -= 1
                            menu.buttons = get_files(directory, menu, up, down)
                    else:
                        up, down = 1, 14
                        directory += '/'+button.button_text
                        menu.buttons = get_files(directory, menu, up, down)
                        screen.fill(BLACK)
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
        for button in menu.buttons:
            if button.check_pos(mouse_pos):
                if button.button_text == '. . .':
                    pass
                else:
                    if define_format(button.button_text) == '.txt':
                        act_file = directory+'/'+button.button_text
                        up, down = 1, 14
                    else:
                        pass
    return (directory, act_file, up, down)

#buliding file_menu
up = 1
down = 14
directory = os.path.abspath(os.curdir)
file_menu = Menu(screen)
file_menu.Rect = ((130, 50), (320, 500))
brx, bry, brl, brh = file_menu.Rect[0][0]+10, file_menu.Rect[0][1]+5, 300, 20
bsxd, bsyd = file_menu.Rect[0][0]+10, file_menu.Rect[1][1]+file_menu.Rect[0][1]-25 
bsld, bshd = 300, 20
bsxu, bsyu = file_menu.Rect[0][0]+10, file_menu.Rect[0][1]+30
bslu, bshu = 300, 20
button_return = Button(screen, brx, bry, brl, brh, (BLACK, WHITE), '. . .', 5)
button_scrolld = Button(screen, bsxd, bsyd, bsld, bshd, (GREEN, BLACK), 'SCROLL DOWN', 5)
button_scrollu = Button(screen, bsxu, bsyu, bslu, bshu, (GREEN, BLACK), 'SCROLL UP', 5)
buttons = get_files(directory, file_menu, up, down)
file_menu.add_buttons(buttons)
directory = shape(directory)
open_file = ''
save_file = ''
save_menu = False
open_menu = False

#building hard_drive_menu
hard_drive_menu = Menu(screen)
ml = 80
mh = 100
mx = file_menu.Rect[0][0]-ml-10
my = file_menu.Rect[0][1]+file_menu.Rect[1][1]//2
hard_drive_menu.Rect = ((mx, my), (ml, mh))
x, y, =  hard_drive_menu.Rect[0][0]+10, hard_drive_menu.Rect[0][1]+5
if len(drives) != 0:
    l, h = ml-20, (mh-(len(drives)+1)*5)//len(drives)
else:
    hard_drive_menu.Rect = ((0, 0), (0, 0))
hard_drives = []
for elem in drives:
    hard_drives.append(Button(screen, x, y, l, h, (RED, BLACK), elem, 5))
    y += h+5
hard_drive_menu.add_buttons(hard_drives)

#building create file menu
cx = file_menu.Rect[0][0]+5
cy = file_menu.Rect[0][1]+file_menu.Rect[1][1]+5
cl, ch = 100, 20
create_button = Button(screen, cx, cy, cl, ch, (RED, BLACK), 'Create file', 5)
cmRect = ((file_menu.Rect[0][0]+file_menu.Rect[1][0]+5, file_menu.Rect[0][1]), 
          (270, 70))
cfont = pg.font.Font(None, 20)
rule = cfont.render('Choose a directory and ENTER the name', True, BLACK)
rule1 = cfont.render('ESC to exit create mode', True, BLACK)
name = cfont.render(save_file, True, BLACK)
create_menu = False

#buliding main menu
menu = Menu(screen)
menu.active = True
time = cfont.render('Control time step with SPACE and BACKSPACE', True, WHITE)
s = 8 #distance between menu's left border and button's one
button_height = Menu.Rect[1][1]//6
button_colors = [menu.colors[1], menu.colors[2]]
start_button = Button(screen, 
                     Menu.Rect[0][0]+s, 
                     Menu.Rect[0][1]+Menu.Rect[1][1]-4*(s+button_height),
                     Menu.Rect[1][0]-2*s,
                     button_height,
                     button_colors,
                     'Start',
                     100)
quit_button = Button(screen, 
                     Menu.Rect[0][0]+s, 
                     Menu.Rect[0][1]+Menu.Rect[1][1]-(s+button_height),
                     Menu.Rect[1][0]-2*s,
                     button_height,
                     button_colors,
                     'Quit',
                     100)
open_button = Button(screen, 
                     Menu.Rect[0][0]+s, 
                     Menu.Rect[0][1]+Menu.Rect[1][1]-3*(s+button_height),
                     Menu.Rect[1][0]-2*s,
                     button_height,
                     button_colors,
                     'Open file',
                     100)
save_button = Button(screen, 
                     Menu.Rect[0][0]+s, 
                     Menu.Rect[0][1]+Menu.Rect[1][1]-2*(s+button_height),
                     Menu.Rect[1][0]-2*s,
                     button_height,
                     button_colors,
                     'Save file',
                     100)
buttons = [quit_button, start_button, open_button, save_button]
menu.add_buttons(buttons)

px = Menu.Rect[0][0]+s
py = Menu.Rect[0][1]+Menu.Rect[1][1]+5
pause = Button(screen, px, py, Menu.Rect[1][0]-2*s, 
               button_height, button_colors,
               'Pause', 100)

#setting defaults
sky = Sky(screen, size)
pg.display.update()
clock = pg.time.Clock()
space_objects = []
vx_list = []
y_list = []
time_step = 100
finished = False
not_started = True
k = 0

while not finished:
    clock.tick(FPS)
    mouse_pos = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type==pg.KEYDOWN and event.key==pg.K_SPACE:
            if not_started==False:
                time_step += 200
                print(time_step)
        if event.type==pg.KEYDOWN and event.key==pg.K_BACKSPACE:
            if not_started==False:
                time_step -= 200
                print(time_step)
        if event.type==pg.MOUSEBUTTONDOWN and event.button==1:
            if not_started == False:
                if pause.check_pos(mouse_pos):
                    not_started = True
        if create_menu:
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                if define_format(save_file)=='.txt':
                    create_menu = False
                    save_file = directory + '/' + save_file
                else:
                    save_file = ''
                    name = cfont.render(save_file, True, BLACK)
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                create_menu = False
                save_file = ''
                name = cfont.render(save_file, True, BLACK)
            elif event.type == pg.KEYDOWN and event.key != pg.K_RETURN:
                if event.key == pg.K_BACKSPACE:
                    if len(save_file) != 0:
                        save_file = minus(save_file)
                        name = cfont.render(save_file, True, BLACK)
                else:
                    code = str(event.unicode)
                    save_file += code
                    name = cfont.render(save_file, True, BLACK)
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if save_menu:
                if create_button.check_pos(mouse_pos):
                    create_menu = True
        if file_menu.active:
            if open_menu==True and save_menu==False:
                return_tuple = file_menu_actions(event, 
                                                 file_menu, 
                                                 mouse_pos, 
                                                 directory, 
                                                 open_file,
                                                 up, down,
                                                 hard_drive_menu)
                directory = return_tuple[0]
                open_file = return_tuple[1]
                up, down = return_tuple[2], return_tuple[3]
                if len(open_file) != 0:
                    file_menu.active = False
                    open_menu = False
                    space_objects = read_space_objects_data_from_file(open_file)
                    x_list = []
                    for obj in space_objects:
                        x_list.append(obj.x)
                        obj.convert_color()
                        obj.R = int(obj.R)
                    max_x = 1.005*max(x_list)
            if open_menu==False and save_menu==True and create_menu==False:
                return_tuple = file_menu_actions(event, 
                                                 file_menu, 
                                                 mouse_pos, 
                                                 directory, 
                                                 save_file,
                                                 up, down,
                                                 hard_drive_menu)
                directory = return_tuple[0]
                save_file = return_tuple[1]
                up, down = return_tuple[2], return_tuple[3]
                if len(save_file) != 0:
                    file_menu.active = False
                    save_menu = False
                    create_menu = False
                    for obj in space_objects:
                        obj.unconvert_color()
                    write_space_objects_data_to_file(save_file, space_objects)
                    save_file = ''
        if event.type == pg.QUIT:
            finished = True
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if quit_button.check_pos(mouse_pos):
                finished = True
            if start_button.check_pos(mouse_pos) and not_started and open_file != '':
                open_file = ''
                not_started = False
                file_menu.active = False
                open_menu = False
                save_menu = False
                create_menu = False
            if open_button.check_pos(mouse_pos):
                file_menu.active = True
                open_menu = True
                save_menu = False
            if save_button.check_pos(mouse_pos):
                file_menu.active = True
                open_menu = False
                save_menu = True
    sky.app()
    if file_menu.active and not_started:
        if save_menu:
            create_button.app(BLACK, mouse_pos)
            if create_menu:
                roundrect(screen, (YELLOW, BLACK), cmRect, 0, 5)
                screen.blit(rule, (cmRect[0][0]+5, cmRect[0][1]+5))
                screen.blit(rule1, (cmRect[0][0]+5, cmRect[0][1]+25))
                pgd.rect(screen, RED, ((cmRect[0][0]+2, cmRect[0][1]+43), (260, 18)))
                screen.blit(name, (cmRect[0][0]+5, cmRect[0][1]+45))
        file_menu.app(mouse_pos)
        if current_system == 'Windows':
            hard_drive_menu.app(mouse_pos)
    elif not_started == False:
        pause.app(BLACK, mouse_pos)
        screen.blit(time, (300, 20))
        x_list = []
        y_list = []
        for obj in space_objects:
            x_list.append(obj.x)
            y_list.append(obj.y)
        for obj in space_objects:
            scale_factor = calculate_scale_factor(max(max(x_list), max_x))
            x = scale_coord(obj.x, scale_factor)
            y = scale_coord(obj.y, scale_factor)
            obj.convert_color()
            obj.R = int(obj.R)
            if abs(obj.x) > max_x or abs(obj.y) > max_x:
                space_objects.remove(obj)
            obj.app(screen, x, y, space_objects, time_step)
    menu.app(mouse_pos)
    pg.display.update()
    

pg.quit()

