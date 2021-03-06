from static import *

from point import Point

class Wall:
    def __init__(self, x1, y1, x2, y2, color, pg, screen):
        self.p1 = Point(x1, y1)
        self.p2 = Point(x2, y2)
        self.color = color
        self.pg = pg
        self.screen = screen 
        return
        
    def draw(self):
        self.pg.draw.line(self.screen, self.color, (self.p1.x, self.p1.y), (self.p2.x, self.p2.y), 3)
        return
