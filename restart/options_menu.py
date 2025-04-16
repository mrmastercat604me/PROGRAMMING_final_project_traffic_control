import pygame, sys
from functions import *
from classes import *
from variables import *

pygame.init()

def options_menu(screen, surface:pygame.Surface, BackgroundImage, scroll:int, difficulty:str="Normal"):
	'''
	Function to create a new "window" by blanking the surface and drawing everyhting to the surface. The surface is then blit to the screen.

	screen = pygame.display.set_mode(), surface = pygame.Surface, BackgroundImage = pygame.image.load(), scroll = int

	Uses surface to draw all the new features. BackgroundImage and scroll are used to continue the scroll from where it left off.
	The screen parametre is used to blit the surface to the screen properly.

	return scroll and a dict of modified settings.
	'''
	#create the buttons
	title_button = Button(percent_of(25,SCREEN_WIDTH),percent_of(10,SCREEN_HEIGHT),percent_of(50,SCREEN_WIDTH),percent_of(10,SCREEN_HEIGHT),surface,(255,255,255,0))
	difficulty_button = Button(percent_of(25,SCREEN_WIDTH),percent_of(35,SCREEN_HEIGHT),percent_of(25,SCREEN_WIDTH),percent_of(10,SCREEN_HEIGHT),surface,(200,200,200))
	#centre the buttons
	difficulty_button.centerx(percent_of(50,SCREEN_WIDTH))
	#set text for the buttons
	title_button.set_text("Options",font,(0,0,0))
	difficulty_button.set_text(difficulty,font,(0,0,0))

	#TOGGLE_ABLE VARIABLES
	LeftClick = False
	RightClick = False
	settings = {}
	
	running = True
	while running:
		#---------------UPDATE-BACKGROUND---------#
		surface.fill((0,0,0,0))
		scroll = horz_scroll_image(BackgroundImage,surface,scroll=scroll)
		#---------------------------------------#
		#---------DRAW-THE-BUTTONS-----------------#
		title_button.draw()
		difficulty_button.draw()
		#---------------------------------------#
		#------BUTTON-LOGIC--------------#
		mouse_x, mouse_y = pygame.mouse.get_pos()
		if difficulty_button.collidepoint((mouse_x,mouse_y)):
			if LeftClick:
				current_difficulty_index = difficulties_list.index(difficulty)
				new_difficulty_index = current_difficulty_index + 1
				if new_difficulty_index >= len(difficulties_list):
					new_difficulty_index = 0
				difficulty = difficulties_list[new_difficulty_index]
				difficulty_button.set_text(difficulty,font,(0,0,0))
			if RightClick:
				#logic for advanced options that returns the custom settings
				pass
		LeftClick = False
		RightClick = False
		#------PYGAME-EVENT-HANDLING--------#
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					if difficulty in difficulties_list: #if difficulty is a preset
						settings = difficulties_dict.get(difficulty)
					return scroll, (difficulty, settings)
				
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
		#-----------------------------------------#
		#-----DRAW-THE-SURFACE-TO-THE-SCREEN-PROPERLY----------#
		screen.fill((0,0,0))
		screen.blit(surface, (0,0))
		pygame.display.flip()
		mainClock.tick(FPS)
		#----------------------#

if __name__ == "__main__":
	print()
	print("Cannot run this file :(")
	print()