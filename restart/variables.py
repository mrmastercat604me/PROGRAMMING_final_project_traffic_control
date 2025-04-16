import pygame

#GLOBAL VARIABLES
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

pygame.init()
#PYGAME SPECIFIC VARIABLES
font = pygame.font.SysFont(None,75)
mainClock = pygame.time.Clock()
FPS = 60

#COLOURS
EASY_COLOURS = {
    "red": (255,0,0),
    "orange": (255,181,0),
    "yellow": (255,2550,0),
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
#GRID VARIABLES
TILE_SIZE:int = 20
GRID_WIDTH:int = 30
GRID_HEIGHT:int = 30
DIRECTIONS:list = [(0,-1),(0,1),(-1,0),(1,0)] #up, down, left, right

#GAME VARIABLES
LOCATION_SPAWN_RANGE = 3 #how many tiles from the edge (including the edge tile) can be used for a location

#DIFFICULTIES
difficulties_dict = {
	"Easy" : {
		"colours": 3,
        "colour_list": EASY_COLOURS,
		"pairs": 1,
		"obstacles": (GRID_HEIGHT*GRID_WIDTH)//20,
		"car_spawn_rate": 4#cars to spawn per MINUTE
	},
	"Normal" : {
		"colours": 5,
        "colours_list": NORMAL_COLOURS,
		"pairs": 3,
		"obstacles": (GRID_HEIGHT*GRID_WIDTH)//15,
		"car_spawn_rate": 12 #cars to spawn per MINUTE
	},
	"Hard" : {
		"colours":10,
        "colours_list": HARD_COLOURS,
		"pairs":4,
		"obstacles": (GRID_HEIGHT*GRID_WIDTH) // 10,
		"car_spawn_rate": 20
	}
}
difficulties_list = list(difficulties_dict.keys())