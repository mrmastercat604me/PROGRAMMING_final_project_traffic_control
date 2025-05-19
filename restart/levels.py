import pygame, sys
from variables import *
from classes import *
from functions import *
from grid import draw_grid, iterate_grid
from game import game

pygame.init()

def levels_screen(screen,surface)->None:
	'''
	Create a new 'window' to select previous levels

	Takes the current screen and surface

	Runs the game window using a selected grid.
	'''
	print("levels")
	print(len(LEVELS))
	print()

	tiles_to_make = len(LEVELS)
	print(tiles_to_make)
	#need to calculate max grid_width
	tiles_can_make = percent_of(75,TILE_SIZE_WIDTH*tiles_to_make)
	print(SCREEN_WIDTH)
	print(TILE_SIZE_WIDTH)
	print(tiles_can_make)
	if tiles_to_make*TILE_SIZE_WIDTH > percent_of(75,SCREEN_WIDTH):
		if tiles_to_make % 5 == 0:
			grid_height = tiles_to_make//5
		else:
			grid_height = tiles_to_make//5 +1
	else:
		grid_height = 1
	LeftClick = False
	running = True
	while running:
		break



#if the user tries to run THIS file
if __name__ == "__main__":
	print()
	print("Cannot run this file :(")
	print()