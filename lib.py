from static import *

from point import Point 
from wall import Wall

import numpy as np

def make_random_walls(pg, screen):
    ''' Generate walls at random positions and angles '''

    ''' (an arbitrary offset value was used to prevent walls from being generated at or outside of view range) '''
    offset = 20

    walls = [
        Wall(
            np.random.randint(offset,WIDTH-offset), 
            np.random.randint(offset,HEIGHT-offset), 
            np.random.randint(offset,WIDTH-offset),  
            np.random.randint(offset,HEIGHT-offset),
            pg, screen
        ) 
        for _ in range(nWalls)
    ]

    ''' Boundary walls (an arbitrary offset value was used to shift boundary walls towards outside of view ange)'''
    offset = -10

    walls.append(Wall(-offset,-offset,-offset,HEIGHT+offset, pg, screen))
    walls.append(Wall(-offset,-offset,WIDTH,-offset, pg, screen))
    walls.append(Wall(-offset,HEIGHT+offset,WIDTH,HEIGHT+offset, pg, screen))
    walls.append(Wall(WIDTH,-offset,WIDTH,HEIGHT+offset, pg, screen))
    return walls
        
def make_rect_walls(pg, screen):
    offset = 100
    walls = []
    for i in range(nWalls):
        pivot = Point(np.random.randint(offset, WIDTH-offset), np.random.randint(offset, WIDTH-offset))

        dx = np.random.randint(40, 90)
        dy = np.random.randint(40, 90)

        point_1 = Point(pivot.x, pivot.y)
        point_2 = Point(pivot.x+dx, pivot.y)
        point_3 = Point(pivot.x+dx, pivot.y+dy)
        point_4 = Point(pivot.x, pivot.y+dy)

        walls.append(Wall(point_1.x, point_1.y, point_2.x, point_2.y, pg, screen))
        walls.append(Wall(point_2.x, point_2.y, point_3.x, point_3.y, pg, screen))
        walls.append(Wall(point_3.x, point_3.y, point_4.x, point_4.y, pg, screen))
        walls.append(Wall(point_4.x, point_4.y, point_1.x, point_1.y, pg, screen))

    offset = -10

    walls.append(Wall(-offset,-offset,-offset,HEIGHT+offset, pg, screen))
    walls.append(Wall(-offset,-offset,WIDTH,-offset, pg, screen))
    walls.append(Wall(-offset,HEIGHT+offset,WIDTH,HEIGHT+offset, pg, screen))
    walls.append(Wall(WIDTH,-offset,WIDTH,HEIGHT+offset, pg, screen))
    return walls

def draw(source, walls, pg, screen):
    source.draw()
    for wall in walls:
        wall.draw()

    pg.draw.rect(screen, BLUE, (WIDTH, 0, WIDTH, int(HEIGHT/2)))
    pg.draw.rect(screen, GREEN, (WIDTH, HEIGHT/2, WIDTH, int(HEIGHT/2)))
    return

def map_value(value):
    _max = np.sqrt(WIDTH**2 + HEIGHT**2)
    _min = 0 

    M = 255.
    m = 0.

    scaler = (M-m)/(_max-_min)
    return (value-_min)*(scaler)+m
