import pygame as pg
import numpy as np
import random
import math

class Source:
    def __init__(self, x, y):
        self.pos = Point(x, y)
        self.angle = np.random.randint(0, 360)
        self.view_mode = 0 

        ''' list to store all light ray objects emerging from light source '''
        self.rays = []
        return
        
    def generate_rays(self):
        for i in range(0, N):
            angle = i*FOV/N * np.pi/180
            self.rays.append(Ray(self.pos.x, self.pos.y, angle))
        return
    
    def move(self, x, y):
        self.pos.move(x, y)
        
        for ray in self.rays:
            ray.move(x, y)
        return
    
    def dist(self, ip):
        return np.sqrt(np.sum([(self.pos.x-ip[0])**2, (self.pos.y-ip[1])**2]))

    def draw(self):
        pg.draw.rect(screen, BLACK, (0, 0, SWIDTH, HEIGHT))
        
        if (self.pos.x < WIDTH):
            pg.draw.circle(screen, GREEN, (self.pos.x, self.pos.y), 10)
        return

    ''' 3D Rendering of ray-casting process '''
    ''' There are dozens of other ways to map 2D info to 3D, '''
    ''' which affects how the rendering process looks like to our eyes. '''
    ''' parameters i and distance refers to the index of a ray and its distance to the nearest wall '''
    ''' '''
    def draw3D(self, i, distance):
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
        color = 255-map_value(distance)

        try:
            pg.draw.rect(screen, (color, color, color), (WIDTH + (i*dx), int((HEIGHT-dy)/2), dx, dy))
        except:
            pass
        return
    
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        return
        
    def __add__(self, pos):
        return (self.x + pos[0], self.y + pos[1]) 

    def move(self, x, y):
        self.x = x
        self.y = y
        return
        
class Ray:
    def __init__(self, x, y, angle=0):
        self.angle = angle
        self.p1 = Point(x, y)
        self.p2 = Point(self.p1.x + (999 * np.cos(self.angle)), self.p1.y + (999* np.sin(self.angle)))
        
        self.hit = False
        return
           
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
    
    def __str__(self):
        return '{0}_{1}__{2}_{3}'.format(str(self.p1.x),str(self.p1.y),str(self.p2.x),str(self.p2.y))
    
    def draw(self, ip):
        if (self.p1.x < WIDTH):
            pg.draw.line(screen, WHITE, (self.p1.x, self.p1.y), ip, 1)
        pg.draw.circle(screen, YELLOW, ip, 3)
        return
        
class Wall:
    def __init__(self, x1, y1, x2, y2):
        self.p1 = Point(x1, y1)
        self.p2 = Point(x2, y2)
        return
        
    def draw(self):
        pg.draw.line(screen, PURPLE, (self.p1.x, self.p1.y), (self.p2.x, self.p2.y), 3)
        return

def make_random_walls():
    ''' Generate walls at random positions and angles '''

    ''' (an arbitrary offset value was used to prevent walls from being generated at or outside of view range) '''
    offset = 20

    walls = [
        Wall(
            np.random.randint(offset,WIDTH-offset), 
            np.random.randint(offset,HEIGHT-offset), 
            np.random.randint(offset,WIDTH-offset),  
            np.random.randint(offset,HEIGHT-offset)  
        ) 
        for _ in range(nWalls)
    ]

    ''' Boundary walls (an arbitrary offset value was used to shift boundary walls towards outside of view ange)'''
    offset = -10

    walls.append(Wall(-offset,-offset,-offset,HEIGHT+offset))
    walls.append(Wall(-offset,-offset,WIDTH,-offset))
    walls.append(Wall(-offset,HEIGHT+offset,WIDTH,HEIGHT+offset))
    walls.append(Wall(WIDTH,-offset,WIDTH,HEIGHT+offset))
    return walls
        
def make_rect_walls():
    offset = 50
    walls = []
    for i in range(nWalls):
        pivot = Point(np.random.randint(offset, WIDTH-offset), np.random.randint(offset, WIDTH-offset))

        dx = np.random.randint(20, 40)
        dy = np.random.randint(20, 40)

        point_1 = Point(pivot.x, pivot.y)
        point_2 = Point(pivot.x+dx, pivot.y)
        point_3 = Point(pivot.x+dx, pivot.y+dy)
        point_4 = Point(pivot.x, pivot.y+dy)

        walls.append(Wall(point_1.x, point_1.y, point_2.x, point_2.y))
        walls.append(Wall(point_2.x, point_2.y, point_3.x, point_3.y))
        walls.append(Wall(point_3.x, point_3.y, point_4.x, point_4.y))
        walls.append(Wall(point_4.x, point_4.y, point_1.x, point_1.y))

    offset = -10

    walls.append(Wall(-offset,-offset,-offset,HEIGHT+offset))
    walls.append(Wall(-offset,-offset,WIDTH,-offset))
    walls.append(Wall(-offset,HEIGHT+offset,WIDTH,HEIGHT+offset))
    walls.append(Wall(WIDTH,-offset,WIDTH,HEIGHT+offset))
    return walls

def draw(source, walls):
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

def main():
    ''' The light source casting rays within specified field of view range ''' 
    source = Source(int(WIDTH/2), int(HEIGHT/2))
    source.generate_rays()


    ''' Generate walls which "blocks" the light rays thus providing what we perceive as shade effects '''
    ''' You can pick the wall type of your choice '''
    wall_type = 'rect'

    wall_generator = {
        'rect': make_rect_walls,
        'random': make_random_walls,
    }
    walls = wall_generator[wall_type]()


    ''' ######### Rendering Pipeline ########## '''
    clicked = False
    while True:
        draw(source, walls)
        
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
            source = Source(int(WIDTH/2), int(HEIGHT/2))
            source.generate_rays()
            walls = wall_generator[wall_type]()
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
    ''' Below are parameter configurations; feel free to play with them! '''

    ''' field of view angle (0 ~ 360) '''
    FOV = 30 


    ''' number of rays being emitted from the source light '''
    ''' This value has to do with how "smooth" the walls look like '''
    N = 30


    ''' dimensions of the 2D ray-casting window '''
    WIDTH = 400
    HEIGHT = 400


    ''' horizontal length of the entire screen, which includes 3D ray-casting window '''
    SWIDTH = 2*WIDTH


    ''' number of walls '''
    nWalls = 10


    ''' light source rotation speed '''
    ROTATION_SPEED = 1


    ''' parameter to tweak 3D view experience '''
    DISTORTION_ANGLE = N*WIDTH/(math.tan(math.pi/6))


    ''' Various methods for pseudo-3D view perspective '''
    VIEW_MODES = [
        'cosine',
        'tangent',
        'fisheye'
    ]


    ''' Colors in rectRGB format '''
    RED = (255, 0, 0)
    YELLOW = (253, 253, 150)
    GREEN = (0,155,0)
    BLUE = (0,128,255)
    PURPLE = (102, 51, 153)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)


    ''' Initialize pygame session and configure settings '''
    pg.init()

    screen = pg.display.set_mode((SWIDTH, HEIGHT))

    pg.display.set_caption('3D Ray Casting')

    main()