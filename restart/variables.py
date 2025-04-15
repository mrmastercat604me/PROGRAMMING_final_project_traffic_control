import pygame

#GLOBAL VARIABLES
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

pygame.init()
#PYGAME SPECIFIC VARIABLES
font = pygame.font.SysFont(None,75)
mainClock = pygame.time.Clock()
FPS = 60

#DIFFICULTIES
difficulties_dict = {
	"Easy" : {},
	"Normal" : {},
	"Hard" : {}
}
difficulties_list = list(difficulties_dict.keys())

#GRID VARIABLES
TILE_SIZE:int = 20
GRID_WIDTH:int = 30
GRID_HEIGHT:int = 30
DIRECTIONS:list = [(0,-1),(0,1),(-1,0),(1,0)] #up, down, left, right

#GAME VARIABLES
LOCATION_SPAWN_RANGE = 3 #how many tiles from the edge (including the edge tile) can be used for a location
