from static import *

from lib import map_value
from point import Point
from ray import Ray 

import numpy as np
import random
import math

class Source:
    def __init__(self, x, y, pg, screen):
        self.pos = Point(x, y)
        self.angle = np.random.randint(0, 360)
        self.view_mode = 0 
        self.pg = pg
        self.screen = screen 

        ''' list to store all light ray objects emerging from light source '''
        self.rays = []
        return
        
    def generate_rays(self):
        self.ray_color = BLUE 
        self.point_color = GREEN 
        for i in range(0, N):
            angle = i*FOV/N * np.pi/180
            self.rays.append(Ray(self.pos.x, self.pos.y, self.ray_color, self.point_color, self.pg, self.screen, angle))
        return
    
    def change_ray_colors(self):
        self.ray_color = random.choice(COLORS)
        self.point_color = random.choice(COLORS)
        for ray in self.rays:
            ray.change_color(self.ray_color, self.point_color)
        return

    def move(self, x, y):
        self.pos.move(x, y)
        
        for ray in self.rays:
            ray.move(x, y)
        return
    
    def dist(self, ip):
        return np.sqrt(np.sum([(self.pos.x-ip[0])**2, (self.pos.y-ip[1])**2]))

    def draw(self):
        self.pg.draw.rect(self.screen, BLACK, (0, 0, SWIDTH, HEIGHT))
        
        if (self.pos.x < WIDTH):
            self.pg.draw.circle(self.screen, GREEN, (self.pos.x, self.pos.y), 10)
        return

    ''' 3D Rendering of ray-casting process '''
    ''' There are dozens of other ways to map 2D info to 3D, '''
    ''' which affects how the rendering process looks like to our eyes. '''
    ''' parameters i and distance refers to the index of a ray and its distance to the nearest wall '''
    ''' '''
    def draw3D(self, i, distance, color):
        if distance==0:
            return

        ''' width of rectangle being rendered in 3D '''
        dx = int(WIDTH/N)

        ''' height of rectangle being rendered in 3D '''
        if VIEW_MODES[self.view_mode] == 'tangent':
            dy = int(DISTORTION_ANGLE/distance)
        elif VIEW_MODES[self.view_mode] == 'cosine':
            dy = int((N*HEIGHT/distance)*math.cos(abs(i*(FOV/N)-FOV)*math.pi/180))
        elif VIEW_MODES[self.view_mode] == 'fisheye':
            dy = int(HEIGHT-distance)

        ''' color value provides an effect in which wall's color being altered '''
        ''' depending on its distance to the light source '''
        #color = 255-map_value(distance)
        color = tuple([v-map_value(distance, v) for v in color])

        try:
            self.pg.draw.rect(self.screen, color, (WIDTH + (i*dx), int((HEIGHT-dy)/2), dx, dy))
        except:
            pass
        return
