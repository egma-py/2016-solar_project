from colors import *
from random import randint
from solar_model import *

import pygame as pg
import pygame.draw as pgd
import math as m

class Star:
    def __init__(self):
        self.type = 'star'
        self.m = 0
        self.x = 0
        self.y = 0
        self.Vx = 0
        self.Vy = 0
        self.Fx = 0
        self.Fy = 0
        self.R = 5
        self.color = RED
        self.image = None
        
    def app(self, screen, x, y, space_objects, dt):
        pgd.circle(screen, self.color, (x, y), self.R)
        recalculate_space_objects_positions(space_objects, dt)
        
    def convert_color(self):
        if self.color == "orange":
            self.color = ORANGE
        elif self.color == "red":
            self.color = RED
        elif self.color == "blue":
            self.color = BLUE
        elif self.color == "green":
            self.color = GREEN
        elif self.color == "yellow":
            self.color = YELLOW
        elif self.color == "white":
            self.color = WHITE
        elif self.color == "gray":
            self.color = GRAY
        elif self.color == "cyan":
            self.color = CYAN
            
    def unconvert_color(self):
        if self.color == ORANGE:
            self.color = 'orange'
        elif self.color == RED:
            self.color = 'red'
        elif self.color == BLUE:
            self.color = 'blue'
        elif self.color == GREEN:
            self.color = 'green'
        elif self.color == YELLOW:
            self.color = 'yellow'
        elif self.color == WHITE:
            self.color = 'white'
        elif self.color == GRAY:
            self.color = 'gray'
        elif self.color == CYAN:
            self.color = 'cyan'


class Planet:
    def __init__(self):
        self.type = 'planet'
        self.m = 0
        self.x = 0
        self.y = 0
        self.Vx = 0
        self.Vy = 0
        self.Fx = 0
        self.Fy = 0
        self.R = 5
        self.color = GREEN
        self.image = None
        
    def app(self, screen, x, y, space_objects, dt):
        pgd.circle(screen, self.color, (x, y), self.R)
        recalculate_space_objects_positions(space_objects, dt)
        
    def convert_color(self):
        if self.color == "orange":
            self.color = ORANGE
        elif self.color == "red":
            self.color = RED
        elif self.color == "blue":
            self.color = BLUE
        elif self.color == "green":
            self.color = GREEN
        elif self.color == "yellow":
            self.color = YELLOW
        elif self.color == "white":
            self.color = WHITE
        elif self.color == "gray":
            self.color = GRAY
        elif self.color == "cyan":
            self.color = CYAN
            
    def unconvert_color(self):
        if self.color == ORANGE:
            self.color = 'orange'
        elif self.color == RED:
            self.color = 'red'
        elif self.color == BLUE:
            self.color = 'blue'
        elif self.color == GREEN:
            self.color = 'green'
        elif self.color == YELLOW:
            self.color = 'yellow'
        elif self.color == WHITE:
            self.color = 'white'
        elif self.color == GRAY:
            self.color = 'gray'
        elif self.color == CYAN:
            self.color = 'cyan'



class Sky:
    star_amount = 60
    star_r = 1
    def __init__(self, screen, size):
        self.screen = screen
        self.Rect = ((0, 0), size)
        self.stars = []
        for i in range(Sky.star_amount):
            self.stars.append((randint(0, size[0]), randint(0, size[1])))
        
    def app(self):
        pgd.rect(self.screen, BLACK, self.Rect)
        for star in self.stars:
            pgd.circle(self.screen, WHITE, star, Sky.star_r)