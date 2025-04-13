import pygame, sys
from functions import *

pygame.init()

#GLOBAL VARIABLES
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
font = pygame.font.SysFont(None,70)


mainClock = pygame.time.Clock()

#create the main screen
pygame.display.set_caption("Game Name")
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),0,32)
surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SRCALPHA)
BackgroundImage = pygame.image.load("assets/background.png")
BackgroundImageRect = BackgroundImage.get_rect()
BackgroundImageRect.topleft = (0,0)
BackgroundImage = pygame.transform.scale(BackgroundImage,(SCREEN_WIDTH,SCREEN_HEIGHT))



LeftClick = False
RightClick = False

def main_menu():
	LeftClick = False
	RightClick = False
	while True:
		#----DRAW-SCREEN-BACKGROUND-------#
		screen.fill((0,0,0))
		screen.blit(surface, (0,0))
		surface.blit(BackgroundImage,BackgroundImageRect)
		#----------------------------------------#
		#----------DRAW-TITLE-AND-BUTTONS------#
		mouse_x,mouse_y = pygame.mouse.get_pos()
		secret_button = pygame.Rect(percent_of(25,SCREEN_WIDTH),percent_of(10,SCREEN_HEIGHT),percent_of(50,SCREEN_WIDTH),percent_of(10,SCREEN_HEIGHT))
		start_button = pygame.Rect(percent_of(25,SCREEN_WIDTH),percent_of(35,SCREEN_HEIGHT),percent_of(25,SCREEN_WIDTH),percent_of(10,SCREEN_HEIGHT))
		options_button = pygame.Rect(percent_of(25,SCREEN_WIDTH),percent_of(50,SCREEN_HEIGHT),percent_of(25,SCREEN_WIDTH),percent_of(10,SCREEN_HEIGHT))
		start_button.centerx = percent_of(50,SCREEN_WIDTH)
		options_button.centerx = percent_of(50,SCREEN_WIDTH)
		pygame.draw.rect(surface,(200,200,200),start_button)
		pygame.draw.rect(surface,(200,200,200),options_button)
		draw_text("Game Name",font,(0,0,0),surface,0,0,secret_button)
		draw_text("Start",font,(0,0,0),surface,0,0,start_button)
		draw_text("Options",font,(0,0,0),surface,0,0,options_button)
		#--------------------------------------------#
		#----------BUTTON-LOGIC--------#
		if secret_button.collidepoint((mouse_x,mouse_y)):
			if LeftClick:
				print("Secret")
		if start_button.collidepoint((mouse_x,mouse_y)):
			if LeftClick:
				print("Play Game")
		if options_button.collidepoint((mouse_x,mouse_y)):
			if LeftClick:
				print("Options Menu")
		LeftClick = False
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
		pygame.display.update()
		mainClock.tick(60)

if __name__ == "__main__":
	main_menu()