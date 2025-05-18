import pygame, sys
from functions import *
from classes import *
from variables import *
from popups import *
from grid import *
from astar import find_path_astar

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
	GRID_X = (SCREEN_WIDTH//2) - (GRID_WIDTH//2)
	GRID_Y = (SCREEN_HEIGHT//2) - (GRID_HEIGHT//2)
	#create any and all objects
	grid_surface = pygame.Surface((GRID_WIDTH,GRID_HEIGHT))
	grid = Grid(GRID_COLS,GRID_ROWS,x=GRID_X,y=GRID_Y)

	#create the random maze
	create_maze(grid)
	#create the starting positions and store the grid to be saved (if the level is solved)
	
	LeftClick = False
	RightClick = False

	reservation = []
	finalise_reservation = True
	final_reservation_colour = None

	running = True
	#while loop to run while the game is not exited.
	while running:
		#--------------UPDATE-BACKGROUND---------#
		surface.fill((0,0,0,0))
		#---------------------------------------#
		#----------DRAW-EVERYTHING--------------#
		grid_surface = draw_grid(grid_surface,grid)
		surface.blit(grid_surface,(grid.x,grid.y))
		#---------------------------------------#
		#------------PYGAME-EVENT-HANDLING----------#
		#iterate through all of pygame's events.
		for event in pygame.event.get():
			mouse_pos = pygame.mouse.get_pos()
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
				routes = create_valid_locations(grid,3,50,50,3,5)
				if routes:
					print("Routes created")
				else:
					print("NO ROUTES MADE")
					
				colour_edges_of_routes(grid,routes)
			#--------------------------------------------#

			#if the user uses the mouse buttons
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1: #if left click
					LeftClick = True
					tile = grid.get_tile_with_pos(mouse_pos[0],mouse_pos[1])
					print(tile)
					if tile:
						if '_end' in tile.type and tile not in highlighted_path:
							highlighted_type = f'{tile.colour}_route'
							highlighted_path.append(tile)
							highlighted_colour = tile.colour
				if event.button == 3: #if right click
					RightClick = True
			#if left click and mouse moves
			if event.type == pygame.MOUSEMOTION:
				if LeftClick:
					tile = grid.get_tile_with_pos(mouse_pos[0],mouse_pos[1])
					if tile and tile not in highlighted_path:
						if len(highlighted_path) > 0:
							if tile in grid.get_neighbours(highlighted_path[-1],'path'):
								highlighted_path.append(tile)
								tile.colour = highlighted_colour

			#if the user is not using the mouse buttons
			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1: #if not left clicking
					LeftClick = False
					highlighted_path = []
					highlighted_type = None
					highlighted_colour = None
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