import pygame, sys
from functions import *
from classes import *
from variables import *
from popups import *
from grid import *

pygame.init()


def game(screen, surface:pygame.Surface, settings:list)->list:
	'''
	Function to create a new "window" by blanking the surface and drawing everything to the surface. The surface is then blit to the screen.

	screen = pygame.display.set_mode(), surface = pygame.Surface, settings = list (custom or preset)

	Uses surface to draw all the new features. The settings is used for certain difficulty information.
	The screen paramtre is used to blit the surface to the screen properly.

	return settings list to be able to be modified and kept while the window stays active.
	'''
	#Calculate grid placement
	GRID_X = percent_of(50,(SCREEN_WIDTH-(GRID_WIDTH*TILE_SIZE)))
	GRID_Y = percent_of(50,(SCREEN_HEIGHT-(GRID_WIDTH*TILE_SIZE)))
	#create any and all objects
	grid_surface = pygame.Surface((TILE_SIZE*GRID_WIDTH,TILE_SIZE*GRID_HEIGHT))
	grid = Grid(GRID_WIDTH,GRID_HEIGHT)
	
	#GENERATE PAIRS
	colour_count = settings.get("colours")
	colour_list = settings.get("colour_list")
	colours = random.sample(list(colour_list.keys()),colour_count)
	pairs = settings.get("pairs")
	tiles_in_pairs = []
	for colour in colours:
		for pair in range(pairs):
			location1 = select_edge_tile(grid,1,tiles_in_pairs)
			tiles_in_pairs.append(location1)
			location2 = select_edge_tile(grid,1,tiles_in_pairs)
			tiles_in_pairs.append(location2)
			pair1 = DestinationPair(grid,location1,location2,colour)

	LeftClick = False
	RightClick = False
	set_key = False
	score = []

	frames = 0
	seconds = 0

	running = True
	while running:
		#--------------UPDATE-BACKGROUND---------#
		surface.fill((0,0,0,0))
		#---------------------------------------#
		#----------DRAW-EVERYTHING--------------#
		grid_surface = draw_grid(grid_surface,grid)
		surface.blit(grid_surface,(GRID_X,GRID_Y))
		#---------------------------------------#
		#-------------INPUT-LOGIC----------------#
		if set_key:
			location1 = select_edge_tile(grid,1)
			location2 = select_edge_tile(grid,1,location1)
			pair1 = DestinationPair(grid,location1,location2,(255,0,0))
		LeftClick = False
		RightClick = False
		set_key = False
		#-----------------------------------------#
		#------------TIMED-LOGIC---------------#
		if frames == FPS:
			seconds += 1
			frames = 0
		#-----------------------------------#
		#------------PYGAME-EVENT-HANDLING----------#
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				if confirm_game_exit_popup(screen,surface):
					return score
			
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1: #if left click
					LeftClick = True
				if event.button == 3: #if right click
					RightClick = True
			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					LeftClick = False
				if event.button == 3:
					RightClick = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_s:
					set_key = True
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_s:
					set_key = False
		#--------------------------------------------------#
		#----------DRAW-THE-SURFACE-TO-THE-SCREEN-----------#
		screen.fill((0,0,0))
		screen.blit(surface, (0,0))
		pygame.display.flip()
		mainClock.tick(FPS)
		frames += 1
		#---------------------------#

if __name__ == "__main__":
	print()
	print("Cannot run this file :(")
	print()