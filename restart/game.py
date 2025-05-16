import pygame, sys
from functions import *
from classes import *
from variables import *
from popups import *
from grid import *

pygame.init()


def game(screen, surface:pygame.Surface)->None:
	'''
	Function to create a new "window" by blanking the surface and drawing everything to the surface.
	The surface is then blit to the screen.

	"screen" is a pygame.display.set_mode().
	
	"surface" is a pygame.Surface.

	Uses surface to draw all the new features. The settings is used for certain difficulty information.
	The screen paramtre is used to blit the surface to the screen properly.

	Return None
	'''
	#Calculate grid placement
	GRID_X = percent_of(50,(SCREEN_WIDTH-(GRID_WIDTH)))
	GRID_Y = percent_of(50,(SCREEN_HEIGHT-(GRID_HEIGHT)))
	#create any and all objects
	grid_surface = pygame.Surface((GRID_WIDTH,GRID_HEIGHT))
	grid = Grid(GRID_COLS,GRID_ROWS)

	#create the random maze
	create_maze(grid)
	#create the starting positions and store the grid to be saved (if the level is solved)
	
	LeftClick = False
	RightClick = False

	running = True
	#while loop to run while the game is not exited.
	while running:
		#--------------UPDATE-BACKGROUND---------#
		surface.fill((0,0,0,0))
		#---------------------------------------#
		#----------DRAW-EVERYTHING--------------#
		grid_surface = draw_grid(grid_surface,grid)
		surface.blit(grid_surface,(GRID_X,GRID_Y))
		#---------------------------------------#
		#-------------INPUT-LOGIC----------------#
		LeftClick = False
		RightClick = False
		#-----------------------------------------#
		#-----------------------------------#
		#------------PYGAME-EVENT-HANDLING----------#
		#iterate through all of pygame's events.
		for event in pygame.event.get():
			#if the user hits the x in the corner close the entire window.
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()
				sys.exit()
			#if the user hits the escape key, confirm their exit
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				#if they confirm their exit, return out of the function (to go back to the main function / main menu)
				if confirm_game_exit_popup(screen,surface):
					return
			#TEMPORARY
			if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
				print('c key pressed')
				while True:
					routes = create_valid_locations(grid,3)
					if routes:
						print("Routes created")
						break
					else:
						print("NO ROUTES MADE")
						break
				temp_colours = []
				for route in routes:
					while True:
						colour = random.choice(list(EASY_COLOURS.values()))
						if colour not in temp_colours:
							temp_colours.append(colour)
							break
					first_tile = route[0]
					last_tile = route[-1]
					first_tile.colour = colour
					last_tile.colour = colour
					for tile in route:
						print(tile.type)

			#if the user uses the mouse buttons
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1: #if left click
					LeftClick = True
				if event.button == 3: #if right click
					RightClick = True
			
			#if the user is not using the mouse buttons
			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1: #if not left clicking
					LeftClick = False
				if event.button == 3: #if not right clicking
					RightClick = False

		#--------------------------------------------------#
		#----------DRAW-THE-SURFACE-TO-THE-SCREEN-----------#
		screen.fill((0,0,0))
		screen.blit(surface, (0,0))
		pygame.display.flip()
		mainClock.tick(FPS)
		#---------------------------#

#if the user tries to run THIS file.
if __name__ == "__main__":
	print()
	print("Cannot run this file :(")
	print()