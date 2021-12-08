import pygame as pg
import numpy as np
import math

class Source:
    def __init__(self, x, y, distortion_angle):
        self.pos = Point(x, y)
        self.distortion_angle = distortion_angle

        ''' list to store all light ray objects emerging from light source '''
        self.rays = []
        return
        
    def generate_rays(self):
        for i in range(0, FOV, int(FOV/N)):
            angle = i * np.pi/180
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

        ''' width of rectangle being rendered in 3D '''
        dx = int(WIDTH/N)

        ''' height of rectangle being rendered in 3D '''
        try:
            dy = int(self.distortion_angle/distance)
        except:
            return 
            
        ''' color value provides an effect in which wall's color being altered '''
        ''' depending on its distance to the light source '''
        color = 255-map_value(distance)

        pg.draw.rect(screen, (50, color, 50), (WIDTH + (i*dx), int((HEIGHT-dy)/2), dx, dy))
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
        pg.draw.circle(screen, RED, ip, 3)
        return
        
class Wall:
    def __init__(self, x1, y1, x2, y2):
        self.p1 = Point(x1, y1)
        self.p2 = Point(x2, y2)
        return
        
    def draw(self):
        pg.draw.line(screen, BLUE, (self.p1.x, self.p1.y), (self.p2.x, self.p2.y), 1)
        return

def make_walls():
    walls = []

    ''' Generate walls at random positions and angles '''
    for i in range(nWalls):
        walls.append(Wall(np.random.randint(10,WIDTH-10),np.random.randint(10,WIDTH-10), np.random.randint(10,WIDTH-10),np.random.randint(10,WIDTH-10)))

    ''' Boundary walls '''
    walls.append(Wall(-20,-20,-20,HEIGHT+20))
    walls.append(Wall(-20,-20,WIDTH,-20))
    walls.append(Wall(-20,HEIGHT+20,WIDTH,HEIGHT+20))
    walls.append(Wall(WIDTH,-20,WIDTH,HEIGHT+20))
    return walls
        
def draw(o, walls):
    o.draw()
    for wall in walls:
        wall.draw()
    return

def map_value(value):
    _max = np.sqrt((WIDTH/2.)**2 + HEIGHT**2)
    _min = 0 

    M = 255.
    m = 0.

    scaler = (M-m)/(_max-_min)
    return (value-_min)*(scaler)+m

def main():
    ''' The light source casting rays within specified field of view range ''' 
    source = Source(int(WIDTH/2), int(HEIGHT/2), distortion_angle)
    source.generate_rays()


    ''' Generate walls which "blocks" the light rays thus providing what we perceive as shade effects '''
    walls = make_walls()
    
    while True:
        draw(source, walls)
        
        source_angle = 0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                    
            mx, my = pg.mouse.get_pos()
            
        ''' Press A or D to rotate the light source '''
        ''' Press R to reset the environment '''
        ''' Press X to quit '''
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            source_angle = -5
        elif keys[pg.K_d]:
            source_angle = 5
        elif keys[pg.K_r]:
            source = Source(int(WIDTH/2), int(HEIGHT/2))
            source.generate_rays()
            walls = make_walls()
        elif keys[pg.K_x]:
            break

        ''' Update all ray and wall objects '''
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

    ''' number of rays being emitted from the source light (this value must be less than FOV) '''
    ''' This value has to do with how "smooth" the walls look like '''
    N = 45 


    ''' dimensions of the 2D ray-casting window '''
    WIDTH = 400
    HEIGHT = 400


    ''' horizontal length of the entire screen, which includes 3D ray-casting window '''
    SWIDTH = 2*WIDTH


    ''' number of walls '''
    nWalls = 10 


    ''' field of view angle (0 ~ 360) '''
    FOV = 45 


    ''' parameter to tweak 3D view experience '''
    distortion_angle = N*WIDTH/(math.tan(math.pi/4))


    ''' Colors in RGB format '''
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0,255,0)
    BLUE = (0,128,255)
    RED = (255, 0, 0)


    ''' Initialize pygame session and configure settings '''
    pg.init()

    screen = pg.display.set_mode((SWIDTH, HEIGHT))

    pg.display.set_caption('3D Ray Casting')

    main()