from static import *

from point import Point

import numpy as np
import random

class Ray:
    def __init__(self, x, y, ray_color, point_color, pg, screen, angle=0):
        self.angle = angle
        self.p1 = Point(x, y)
        self.p2 = Point(self.p1.x + (999 * np.cos(self.angle)), self.p1.y + (999* np.sin(self.angle)))
        self.ray_color = ray_color 
        self.point_color = point_color 
       	self.pg = pg 
       	self.screen = screen 
        self.hit = False
        return

    def __str__(self):
        return '{0}_{1}__{2}_{3}'.format(str(self.p1.x),str(self.p1.y),str(self.p2.x),str(self.p2.y))   

    def move(self, x, y):
        self.p1.move(x, y)
        return
          
    def rotate(self, angle):
        self.angle += angle * np.pi/180
        self.p2 = Point(self.p1.x + (999 * np.cos(self.angle)), self.p1.y + (999* np.sin(self.angle)))
        return
       
    ''' An application of line-line intersection search algorithm ''' 
    ''' The intersection points of each light ray and walls are calculated, '''
    ''' and the nearest wall from each light ray is determined for shade effects and 3D rendering process. '''
    def intersection(self, wall):
        d = (wall.p1.x-wall.p2.x)*(self.p1.y-self.p2.y)-(wall.p1.y-wall.p2.y)*(self.p1.x-self.p2.x)
        
        if d==0:
            return None
        
        t = ((wall.p1.x-self.p1.x)*(self.p1.y-self.p2.y) - (wall.p1.y-self.p1.y)*(self.p1.x-self.p2.x)) / d
        u = -(((wall.p1.x-wall.p2.x)*(wall.p1.y-self.p1.y) - (wall.p1.y-wall.p2.y)*(wall.p1.x-self.p1.x)) / d)
        
        if t > 0 and t < 1 and u > 0:
            hit_x = int(wall.p1.x + t*(wall.p2.x-wall.p1.x))
            hit_y = int(wall.p1.y + t*(wall.p2.y-wall.p1.y))
            return (hit_x, hit_y)
        else:
            return None
        return
    
    def change_color(self, ray_color, point_color):
        self.ray_color = ray_color
        self.point_color = point_color
        return
    
    def draw(self, ip):
        if (self.p1.x < WIDTH):
            self.pg.draw.line(self.screen, self.ray_color, (self.p1.x, self.p1.y), ip, 1)
        self.pg.draw.circle(self.screen, self.point_color, ip, 3)
        return
