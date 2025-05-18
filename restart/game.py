import pygame, sys
from functions import *
from classes import *
from variables import *
from popups import *
from grid import *
from astar import find_path_astar

pygame.init()


def game(screen, surface:pygame.Surface,grid_arg=None)->None:
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
	if grid_arg is None:
		grid = Grid(GRID_COLS,GRID_ROWS,x=GRID_X,y=GRID_Y)
	else:
		grid = grid_arg.copy()

	#create the random maze
	while True:
		create_maze(grid)
		#create the starting positions and store the grid to be saved (if the level is solved)
		routes = create_valid_locations(grid,PAIRS,50,50,3,5)
		if routes:
			colour_edges_of_routes(grid,routes)
			break
		else:
			print("NO ROUTES MADE")
	#for saving a level to the levels screen (when the level is complete)
	level_save_grid = grid.copy()
		
	LeftClick = False
	RightClick = False

	reservations = []
	reservation = []
	finalise_reservation = True
	final_reservation_colour = None
	remove_reservation = None

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
			
			if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
				reservations = []
				for tile in iterate_grid(grid):
					tile.is_reserved = False
					if "_route" in tile.type:
						tile.type = 'path'
						tile.colour = (255,255,255)
			#--------------------------------------------#

			#if the user uses the mouse buttons
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1: #if left click
					LeftClick = True
					tile = grid.get_tile_with_pos(mouse_pos[0],mouse_pos[1])
					print(tile)
					if tile:
						if '_end' in tile.type and len(reservation) == 0:
							if not tile.is_reserved:
								finalise_reservation = False
								if tile not in reservation:
									reservation.append(tile)
								final_reservation_colour = tile.colour
							else:
								#remove the reservation
								for reserve in reservations:
									if tile in reserve:
										reservations.remove(reserve)
										remove_reservation = reserve
								if remove_reservation is not None:
									for tile_ in remove_reservation:
										tile_.is_reserved = False
										if "_end" not in tile_.type:
											tile_.type = 'path'
											tile_.colour = (255,255,255)
								remove_reservation = None
				if event.button == 3: #if right click
					RightClick = True
			#if left click and mouse moves
			if event.type == pygame.MOUSEMOTION:
				if LeftClick:
					tile = grid.get_tile_with_pos(mouse_pos[0],mouse_pos[1])
					if tile and len(reservation) > 0 and not finalise_reservation:
						last_tile = reservation[-1]
						second_last_tile = reservation[-2] if len(reservation) > 1 else None
						if tile not in reservation:
							if tile in grid.get_neighbours(last_tile,'path'):
								reservation.append(tile)
							if tile.type == f'{final_reservation_colour}_end' and tile in grid.get_neighbours(last_tile,f'{final_reservation_colour}_end'):
								reservation.append(tile)
								finalise_reservation = True

						if tile is second_last_tile:
							removed = reservation.pop()
							if "_end" not in removed.type:
								removed.type = 'path'
								removed.colour = (255,255,255)

						for tile in reservation:
							if "_end" not in tile.type:
								tile.colour = final_reservation_colour
								tile.type = f'{final_reservation_colour}_route'

			#if the user is not using the mouse buttons
			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1: #if not left clicking
					LeftClick = False
					if finalise_reservation and len(reservation) > 0:
						for tile in reservation:
							tile.is_reserved = True
						reservations.append(reservation)
					if not finalise_reservation and len(reservation) > 0:
						for tile in reservation:
							if "_end" not in tile.type:
								tile.type = 'path'
								tile.colour = (255,255,255)
					reservation = []
					final_reservation_colour = None
				if event.button == 3: #if not right clicking
					RightClick = False

		if len(reservations) == PAIRS:
			print("ALL PAIRS MADE")
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