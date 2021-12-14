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
