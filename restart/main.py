import pygame, sys
from functions import *
from classes import *
from variables import *
from options_menu import options_menu
from game import game

pygame.init()

def main_menu():
	#create the main screen
	pygame.display.set_caption("Game Name")
	screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),0,32)
	#create the main surface for EVERYTHING
	surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SRCALPHA).convert_alpha()
	#create background
	BackgroundImage = pygame.image.load("assets/background.png").convert()
	BackgroundImage = pygame.transform.scale(BackgroundImage,(SCREEN_WIDTH,SCREEN_HEIGHT))
	#scrolling background variables
	scroll = 0

	#create the buttons
	title_button = Button(percent_of(25,SCREEN_WIDTH),percent_of(10,SCREEN_HEIGHT),percent_of(50,SCREEN_WIDTH),percent_of(10,SCREEN_HEIGHT),surface,(255,255,255,0))
	start_button = Button(percent_of(25,SCREEN_WIDTH),percent_of(35,SCREEN_HEIGHT),percent_of(25,SCREEN_WIDTH),percent_of(10,SCREEN_HEIGHT),surface,(200,200,200))
	options_button = Button(percent_of(25,SCREEN_WIDTH),percent_of(50,SCREEN_HEIGHT),percent_of(25,SCREEN_WIDTH),percent_of(10,SCREEN_HEIGHT),surface,(200,200,200))
	#centre buttons
	start_button.centerx(percent_of(50,SCREEN_WIDTH))
	options_button.centerx(percent_of(50,SCREEN_WIDTH))
	#set text for the buttons
	title_button.set_text("Game Name",font,(0,0,0))
	start_button.set_text("Start",font,(0,0,0))
	options_button.set_text("Options",font,(0,0,0))

	#OTHER VARIABLES
	LeftClick = False
	RightClick = False
	difficulty = "Easy"
	settings = difficulties_dict.get("Normal")

	running = True
	while running:
		#----UPDATE-SCREEN-BACKGROUND-SCROLL-------#
		scroll = horz_scroll_image(BackgroundImage,surface,scroll=scroll)
		#----------------------------------------#
		#----------DRAW-TITLE-AND-BUTTONS------#
		title_button.draw()
		start_button.draw()
		options_button.draw()
		#--------------------------------------------#
		#----------BUTTON-LOGIC--------#
		mouse_x,mouse_y = pygame.mouse.get_pos()
		if title_button.collidepoint((mouse_x,mouse_y)):
			if LeftClick:
				print("Secret")
			if RightClick:
				print("Secret Right Click")
		if start_button.collidepoint((mouse_x,mouse_y)):
			if LeftClick:
				print("Play Game")
				score = game(screen,surface,settings)
				#call function from other files and run #just like in blastroids project
			if RightClick:
				print("Play Right Click")
		if options_button.collidepoint((mouse_x,mouse_y)):
			if LeftClick:
				print("Options Menu")
				scroll, settings = options_menu(screen,surface,BackgroundImage,scroll,difficulty)
				if "difficulty" in list(settings.keys()):
					difficulty = settings.get("difficulty")
			if RightClick:
				print("Options Right Click")
		LeftClick = False
		RightClick = False
		#------------------------------------------#
		#----------PYGAME-EVENT-HANDLING----------#
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
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
	main_menu()
	pygame.quit()
	sys.exit()