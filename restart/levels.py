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
	print()

	tiles_to_make = len(LEVELS)
	tiles_can_make = round(percent_of(80,SCREEN_WIDTH)) // TILE_SIZE_WIDTH

	print(tiles_to_make)
	print(tiles_can_make)

	if tiles_to_make >= tiles_can_make:
		grid_width = tiles_can_make
		if tiles_to_make % tiles_can_make == 0:
			grid_height = tiles_to_make//tiles_can_make
		else:
			grid_height = (tiles_to_make//tiles_can_make) +1
	else:
		grid_height = 1
		grid_width = tiles_to_make



		
	LeftClick = False
	running = True
	while running:
		break



#if the user tries to run THIS file
if __name__ == "__main__":
	print()
	print("Cannot run this file :(")
	print()