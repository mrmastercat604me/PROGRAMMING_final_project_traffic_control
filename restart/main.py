import pygame, sys
from functions import *
from classes import Button
from variables import *
from game import game
from levels import levels_screen

pygame.init()

def main_menu():
	'''
	Creates the main screen with no parameters.

	All-powerful function to do EVERY aspect of the game using helper functions.

	Returns nothing.
	'''
	
	#create the main screen
	pygame.display.set_caption("Maze-Flow-Connect")
	screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),0,32)
	#create the main surface for EVERYTHING
	surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SRCALPHA).convert_alpha()
	#create background
	BackgroundImage = pygame.image.load("assets/background.png").convert()
	BackgroundImage = pygame.transform.scale(BackgroundImage,(SCREEN_WIDTH,SCREEN_HEIGHT))
	#scrolling background variables
	scroll = 0

	#create the buttons
	maze_button = Button(percent_of(25,SCREEN_WIDTH),percent_of(2,SCREEN_HEIGHT),percent_of(50,SCREEN_WIDTH),percent_of(8,SCREEN_HEIGHT),surface,(255,255,255,20))
	flow_button = Button(percent_of(25,SCREEN_WIDTH),percent_of(10,SCREEN_HEIGHT),percent_of(50,SCREEN_WIDTH),percent_of(8,SCREEN_HEIGHT),surface,(255,255,255,20))
	connect_button = Button(percent_of(25,SCREEN_WIDTH),percent_of(18,SCREEN_HEIGHT),percent_of(50,SCREEN_WIDTH),percent_of(8,SCREEN_HEIGHT),surface,(255,255,255,20))

	start_button = Button(percent_of(25,SCREEN_WIDTH),percent_of(35,SCREEN_HEIGHT),percent_of(25,SCREEN_WIDTH),percent_of(10,SCREEN_HEIGHT),surface,(200,200,200))
	levels_button = Button(percent_of(25,SCREEN_WIDTH),percent_of(50,SCREEN_HEIGHT),percent_of(25,SCREEN_WIDTH),percent_of(10,SCREEN_HEIGHT),surface,(200,200,200))
	exit_button = Button(percent_of(25,SCREEN_WIDTH),percent_of(65,SCREEN_HEIGHT),percent_of(25,SCREEN_WIDTH),percent_of(10,SCREEN_HEIGHT),surface,(200,200,200))
	#centre buttons
	start_button.centerx(percent_of(50,SCREEN_WIDTH))
	levels_button.centerx(percent_of(50,SCREEN_WIDTH))
	exit_button.centerx(percent_of(50,SCREEN_WIDTH))
	#set text for the buttons
	maze_button.set_text("MAZE",font,(255,69,0))
	flow_button.set_text("FLOW",font,(255,69,0))
	connect_button.set_text("CONNECT",font,(255,69,0))
	start_button.set_text("Start",font,(0,0,0))
	levels_button.set_text("Levels",font,(0,0,0))
	exit_button.set_text("Exit",font,(0,0,0))

	#OTHER VARIABLES
	LeftClick = False
	RightClick = False

	in_game = False
	running = True
	#while the user has not quit
	while running:
		#----UPDATE-SCREEN-BACKGROUND-SCROLL-------#
		scroll = horz_scroll_image(BackgroundImage,surface,scroll=scroll)
		#----------------------------------------#
		#----------DRAW-TITLE-AND-BUTTONS------#
		maze_button.draw()
		flow_button.draw()
		connect_button.draw()
		start_button.draw()
		levels_button.draw()
		exit_button.draw()
		#--------------------------------------------#
		#----------BUTTON-LOGIC--------#
		mouse_x,mouse_y = pygame.mouse.get_pos()
		if connect_button.collidepoint((mouse_x,mouse_y)):
			if LeftClick:
				pass
			if RightClick:
				pass
		if start_button.collidepoint((mouse_x,mouse_y)):
			if LeftClick:
				in_game = True
			if RightClick:
				pass
		if levels_button.collidepoint((mouse_x,mouse_y)):
			if LeftClick:
				levels_screen(screen,surface)
		if exit_button.collidepoint((mouse_x,mouse_y)):
			if LeftClick:
				running = False
		LeftClick = False
		RightClick = False
		#------------------------------------------#
		#----------PYGAME-EVENT-HANDLING----------#
		#iterate through all of the events in pygame
		for event in pygame.event.get():
			if event.type == pygame.QUIT: #if hit the corner x
				running = False
			if event.type == pygame.MOUSEBUTTONDOWN: #if mouse button is clicked
				if event.button == 1: #if left click
					LeftClick = True
				if event.button == 3: #if right click
					RightClick = True
			if event.type == pygame.MOUSEBUTTONUP: #if mouse button is not clicked
				if event.button == 1: #if left not clicked
					LeftClick = False
				if event.button == 3: #if right not clicked
					RightClick = False
		if in_game:
			in_game = game(screen,surface)
		#-----------------------------------------#
		#-----DRAW-THE-SURFACE-TO-THE-SCREEN-PROPERLY----------#
		screen.fill((0,0,0))
		screen.blit(surface, (0,0))
		pygame.display.flip()
		mainClock.tick(FPS)
		#----------------------#

#if the user runs this file
if __name__ == "__main__":
	main_menu()
	pygame.quit()
	sys.exit()