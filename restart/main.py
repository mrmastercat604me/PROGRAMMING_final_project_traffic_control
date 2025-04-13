import pygame, sys
from functions import *
from classes import *

pygame.init()

#GLOBAL VARIABLES
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

#PYGAME SPECIFIC VARIABLES
font = pygame.font.SysFont(None,75)
mainClock = pygame.time.Clock()
FPS = 60

#create the main screen
pygame.display.set_caption("Game Name")
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),0,32)
#create the main surface for EVERYTHING
surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SRCALPHA).convert_alpha()
#create background
BackgroundImage = pygame.image.load("assets/background.png").convert()
BackgroundImage = pygame.transform.scale(BackgroundImage,(SCREEN_WIDTH,SCREEN_HEIGHT))
BackgroundImage_width = BackgroundImage.get_width()
#scrolling background variables
scroll = 0
tiles = (SCREEN_WIDTH // BackgroundImage_width) + 1

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

#TOGGLE-ABLE VARIABLES
LeftClick = False
RightClick = False

def main_menu():
	global scroll
	LeftClick = False
	RightClick = False
	while True:
		#----UPDATE-SCREEN-BACKGROUND-SCROLL-------#
		for i in range(0, tiles):
			surface.blit(BackgroundImage,((i*BackgroundImage_width)+scroll,0))
		scroll -= 1
		#reset scroll
		if abs(scroll) > BackgroundImage_width:
			scroll = 0
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
			if RightClick:
				print("Play Right Click")
		if options_button.collidepoint((mouse_x,mouse_y)):
			if LeftClick:
				print("Options Menu")
			if RightClick:
				print("Options Right Click")
		LeftClick = False
		RightClick = False
		#------------------------------------------#
		#----------PYGAME-EVENT-HANDLING----------#
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
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