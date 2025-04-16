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
COLOURS = {
    "maroon": (123,0,0),
    "firebrick": (167,0,0),
	"red": (255,0,0),
    "darkorange": (255,123,0),
    "orange": (255,167,0),
    "gold": (255,211,0),
    "yellow": (255,255,0),
    "yellowgreen": (167,255,0),
    "chartreuse": (123,255,0),
    "lime": (45,255,0),
	"green": (0,255,0),
    "springgreen": (0,255,123),
    "mediumspringgreen": (0,255,167),
    "aquamarine": (0,255,211),
    "turquoise": (0,255,228),
    "aqua": (0,255,255),
    "darkturquoise": (0,227,255),
    "skyblue": (0,218,255),
    "deepskyblue": (0,211,255),
    "cornflowerblue": (0,167,255),
    "dodgerblue": (0,143,255),
    "royalblue": (0, 116,255),
    "mediumslateblue": (0,93,255),
    "mediumblue": (0,64,255),
    "blue": (0,0,255),
    "darkblue": (0,0,152),
    "navy": (0,0,118),
    "midnightblue": (0,0,75)
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
        "pairs": 1,
		"obstacles": (GRID_HEIGHT*GRID_WIDTH)//20,
		"car_spawn_rate": 4#cars to spawn per MINUTE
	},
	"Normal" : {
        "colours": 5,
        "pairs": 3,
        "obstacles": (GRID_HEIGHT*GRID_WIDTH)//15,
        "car_spawn_rate": 12 #cars to spawn per MINUTE
	},
	"Hard" : {
        "colours":10,
        "pairs":4,
        "obstacles": (GRID_HEIGHT*GRID_WIDTH) // 10,
        "car_spawn_rate": 20
	}
}
difficulties_list = list(difficulties_dict.keys())