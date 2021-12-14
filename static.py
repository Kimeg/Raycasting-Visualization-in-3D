import math

''' Below are parameter configurations; feel free to play with them! '''

''' field of view angle (0 ~ 360) '''
FOV = 60 


''' number of rays being emitted from the source light '''
''' This value has to do with how "smooth" the walls look like '''
N = 100


''' dimensions of the 2D ray-casting window '''
WIDTH = 800
HEIGHT = 800


''' horizontal length of the entire screen, which includes 3D ray-casting window '''
SWIDTH = 2*WIDTH


''' number of walls '''
nWalls = 10


''' wall shape [ rect, random, ...more to be updated ] '''
WALL_TYPE = 'rect'


''' light source rotation speed '''
ROTATION_SPEED = 1


''' parameter to tweak 3D view experience '''
DISTORTION_ANGLE = N*WIDTH/(math.tan(math.pi/3))


''' Various methods for pseudo-3D view perspective '''
VIEW_MODES = [
    'tangent',
    'cosine',
    'fisheye'
]


''' Colors in rectRGB format '''
RED = (255, 0, 0)
ORANGE = (255,127,80)
YELLOW = (253, 253, 150)
GREEN = (0,155,0)
BLUE = (0,128,255)
PURPLE = (102, 51, 153)
PINK = (255,192,203)
WHITE = (255, 255, 255)
BROWN = (210, 125, 45)
GREY = (50, 50, 50)
BLACK = (0, 0, 0)
COLORS = [
	RED,
	ORANGE,
	YELLOW,
	GREEN,
	BLUE,
	PURPLE,
	PINK,
	WHITE,
	BROWN,
	GREY,
]