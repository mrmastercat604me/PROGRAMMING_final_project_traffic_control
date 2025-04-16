import pygame, sys, random
from functions import *
from classes import *
from variables import *

pygame.init()

def draw_grid(surface, grid)->'pygame.Surface':
	surface.fill((230,200,200))
	for y in range(grid.height):
		for x in range(grid.width):
			tile = grid.grid[y][x]

			create_rect = pygame.Rect(x*TILE_SIZE,y*TILE_SIZE,TILE_SIZE,TILE_SIZE)

			#handle the type drawing logic here

			pygame.draw.rect(surface,tile.colour,create_rect)
			#draw border around tile
			pygame.draw.rect(surface,(0,0,0),create_rect, 1)
	return surface

def select_edge_tile(grid,count:int=1,except_tile:'Tile'=None):
	if count > 4 or count <= 0:
		return None
	
	x_max = grid.width -1
	#0 to x_max are valid indexes
	y_max = grid.height -1
	#0 to y_max are valid indexes
	#-----DECLARE-EDGES-AND-LAMBDA-TO-CREATE-RANDOM-X,Y-VALUES-----#
	edges = {
		#edge name		#(generate random x value, generate random y value) when called
		"top": lambda: (random.randint(0,x_max),random.randint(0,LOCATION_SPAWN_RANGE-1)),
		"left": lambda: (random.randint(0,LOCATION_SPAWN_RANGE-1),random.randint(0,y_max)),
		"bottom": lambda: (random.randint(0,x_max),random.randint(y_max-LOCATION_SPAWN_RANGE-1,y_max)),
		"right": lambda: (random.randint(x_max-LOCATION_SPAWN_RANGE-1,x_max),random.randint(0,y_max))
	}
	#----------#
	#-----GENERATE-LIST-OF-RANDOM-TILES-----#
	random_tiles_list = []
	for edge, coord_func in edges.items():
		while True:
			x, y = coord_func() #call each lambda
			random_tile = grid.get_tile_with_index(x=x,y=y)
			if except_tile is None or (isinstance(except_tile,Tile) and random_tile != except_tile) or (isinstance(except_tile,list) and random_tile not in except_tile):
				random_tiles_list.append(random_tile)
				break #break out of loop to continue to next edge tile
	#----------#
	#-----RETURN-TILE(S)-----#
	if count == 1:
		return random.choice(random_tiles_list)
	else:
		return_list = list(random.sample(population=random_tiles_list,k=count)) #takes count many items from the population without any repeating elements
		return return_list

