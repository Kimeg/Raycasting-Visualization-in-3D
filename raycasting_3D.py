from static import *
from lib import *

from source import Source
from point import Point 
from wall import Wall 
from ray import Ray 

import pygame as pg
import numpy as np
import random
import math

def main():
    ''' The light source casting rays within specified field of view range ''' 
    source = Source(int(WIDTH/2), int(HEIGHT/2), pg, screen)
    source.generate_rays()

    ''' Generate walls which "blocks" the light rays thus providing what we perceive as light & shade effects '''
    ''' You can pick the wall type of your choice '''

    wall_generator = {
        'rect': make_rect_walls,
        'random': make_random_walls,
    }
    walls = wall_generator[WALL_TYPE](pg, screen)


    ''' ######### Rendering Pipeline ########## '''
    clicked = False
    while True:
        draw(source, walls, pg, screen)
        
        source_angle = 0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            ''' Click left mouse button to change pseudo-3D view mode '''
            if event.type == pg.MOUSEBUTTONDOWN:
                if not clicked:
                    source.view_mode = (source.view_mode+1)%len(VIEW_MODES)
                    clicked = True

            if event.type == pg.MOUSEBUTTONUP:
                    clicked = False 

            mx, my = pg.mouse.get_pos()

        ''' Press A or D to rotate the light source '''
        ''' Press R to reset the environment '''
        ''' Press X to quit '''
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            source_angle = -ROTATION_SPEED
        elif keys[pg.K_d]:
            source_angle = ROTATION_SPEED
        elif keys[pg.K_r]:
            source = Source(int(WIDTH/2), int(HEIGHT/2), pg, screen)
            source.generate_rays()
            walls = wall_generator[WALL_TYPE](pg, screen)
        elif keys[pg.K_x]:
            break

        ''' Update all ray and wall objects '''
        source.angle += source_angle
        for i, ray in enumerate(source.rays):
            ray.rotate(source_angle)
            closest = None
            record = 99999

            ''' Calculate the distance between the given ray and walls, store the closest one '''
            for wall in walls:

                ''' calculate intersection point between ray and wall '''
                ip = ray.intersection(wall)
                
                if not ip == None:
                    d = source.dist(ip) 
                    if d < record:
                        record = d
                        closest = ip

            ''' If there exists a wall, that is closest to the given ray, '''
            ''' draw the ray from the light source to the intersection point on the wall '''
            ''' Render this information on a pseudo-3D space '''
            if not closest == None:
                ray.draw(closest)
                source.draw3D(i, record)
               
        ''' Update the position of the light source ''' 
        source.move(mx, my)


        ''' Render all pygame objects in current frame '''
        pg.display.flip()

    pg.quit()                   
    return

if __name__=="__main__":
    ''' Initialize pygame session and configure settings '''
    pg.init()

    screen = pg.display.set_mode((SWIDTH, HEIGHT))

    pg.display.set_caption('3D Ray Casting Renderer')

    main()