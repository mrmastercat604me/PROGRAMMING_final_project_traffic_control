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

			pygame.draw.rect(surface,(255,255,255),create_rect)
			#draw border around tile
			pygame.draw.rect(surface,(0,0,0),create_rect, 1)
	return surface

def update_grid(grid,settings)->'Grid':
	pass

def select_edge_tile(grid,count:int=1):
	if count > 4 or count <= 0:
		return None
	
	x_max = grid.width -1
	#0 to x_max are valid indexes
	y_max = grid.height -1
	#0 to y_max are valid indexes
	#-----TOP-EDGE-----#
	top_y_min = 0
	top_y_max = LOCATION_SPAWN_RANGE -1
	random_tile_y = random.randint(top_y_min,top_y_max)
	top_x_min = 0
	top_x_max = x_max
	random_tile_x = random.randint(top_x_min,top_x_max)
	random_top_tile = grid.get_tile_within_area(x=random_tile_x, y=random_tile_y)
	#----------#
	#-----LEFT-EDGE-----#
	left_x_min = 0
	left_x_max = LOCATION_SPAWN_RANGE -1
	random_tile_x = random.randint(left_x_min,left_x_max)
	left_y_min = 0
	left_y_max = y_max
	random_tile_y = random.randint(left_y_min,left_y_max)
	random_left_tile = grid.get_tile_within_area(x=random_tile_x, y=random_tile_y)
	#----------#
	#-----BOTTOM-EDGE-----#
	bottom_x_min = 0
	bottom_x_max = x_max
	random_tile_x = random.randint(bottom_x_min,bottom_x_max)
	bottom_y_min = y_max - (LOCATION_SPAWN_RANGE-1)
	bottom_y_max = y_max
	random_tile_y = random.randint(bottom_y_min,bottom_y_max)
	random_bottom_tile = grid.get_tile_within_area(x=random_tile_x,y=random_tile_y)
	#----------#
	#-----RIGHT-EDGE-----#
	right_x_min = x_max - (LOCATION_SPAWN_RANGE-1)
	right_x_max = x_max
	random_tile_x = random.randint(right_x_min,right_x_max)
	right_y_min = 0
	right_y_max = y_max
	random_tile_y = random.randint(right_y_min,right_y_max)
	random_right_tile = grid.get_tile_within_area(x=random_tile_x,y=random_tile_y)
	#----------#
	#-----LIST-OF-RANDOM-TILES-----#
	random_tiles_list = []
	random_tiles_list.append(random_top_tile)
	random_tiles_list.append(random_left_tile)
	random_tiles_list.append(random_bottom_tile)
	random_tiles_list.append(random_right_tile)
	#----------#
	#-----RETURN-TILE(S)-----#
	if count == 1:
		return random.choice(random_tiles_list)
	else:
		return_list = list(random.sample(population=random_tiles_list,k=count)) #takes count many items from the population without any repeating elements
	return return_list


