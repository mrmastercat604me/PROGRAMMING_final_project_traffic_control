import pygame

#GLOBAL VARIABLES
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

pygame.init()
#PYGAME SPECIFIC VARIABLES
font = pygame.font.SysFont(None,75)
mainClock = pygame.time.Clock()
FPS = 60

#GRID VARIABLES
GRID_WIDTH:int = 600 #pixels
GRID_HEIGHT:int = 600 #pixels
GRID_COLS:int = 15
GRID_ROWS:int = 15
TILE_SIZE_WIDTH:int = GRID_WIDTH // GRID_COLS
TILE_SIZE_HEIGHT:int = GRID_HEIGHT // GRID_ROWS

EDGES:list = ["top","left" ,"bottom","right"]
DIRECTIONS:list = [(0,-1),(0,1),(-1,0),(1,0)] #up, down, left, right

#COLOURS
EASY_COLOURS = {
	"red": (255,0,0),
	"orange": (255,181,0),
	"yellow": (255,255,0),
	"green": (0,255,0),
	"aqua": (0,255,252),
	"blue":(0,0,255),
	"blueviolet": (147,0,255),
	"fuchsia": (228,0,255)
}
NORMAL_COLOURS = {
	"red":(255,0,0),
	"orangered": (201,0,0),
	"orange": (255,181,0),
	"darkorange": (255,130,0),
	"yellow": (255,255,0),
	"greenyellow": (185,255,0),
	"green": (0,255,0),
	"lime": (45,255,0),
	"blue": (0,0,255),
	"skyblue": (0,218,255),
	"darkviolet": (175,0,255),
	"fuchsia": (228,0,255)
}
HARD_COLOURS = {
	"aqua": (0,255,252),
	"aquamarine": (0,255,210),
	"blue": (0,0,255),
	"blueviolet": (147,0,255),
	"chartreuse": (122,255,0),
	"cornflowerblue": (0,167,255),
	"crimson": (255,0,79),
	"darkblue": (0,0,152),
	"darkorange": (255,130,0),
	"darkred": (150,0,0),
	"darkturquoise": (0,227,255),
	"darkviolet": (175,0,255),
	"deeppink": (255,0,153),
	"deepskyblue": (0,211,255),
	"dodgerblue": (0,143,255),
	"firebrick": (183,0,0),
	"fuchsia": (228,0,255),
	"gold": (255,212,0),
	"green": (0,255,0),
	"greenyellow": (185,255,0),
	"lime": (45,255,0),
	"maroon": (98,0,0),
	"mediumblue": (0,64,255),
	"mediumslateblue": (0,93,255),
	"mediumspringgreen": (0,255,169),
	"midnightblue": (0,0,75),
	"navy": (0,0,118),
	"orange": (255,181,0),
	"orangered": (201,0,0),
	"red": (255,0,0),
	"royalblue": (0, 116,255),
	"skyblue": (0,218,255),
	"springgreen": (0,255,114),
	"turquoise": (0,255,226),
	"yellow": (255,255,0)
}

#DIFFICULTIES
difficulties_dict = {
	"Easy" : {
		"colour_count": 3,
		"colour_list": EASY_COLOURS,
		"pairs": 1,
	},
	"Normal" : {
		"colour_count": 5,
		"colour_list": NORMAL_COLOURS,
		"pairs": 2,
	},
	"Hard" : {
		"colour_count":10,
		"colour_list": HARD_COLOURS,
		"pairs":4,
	}
}
difficulties_list = list(difficulties_dict.keys())