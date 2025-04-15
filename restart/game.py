import pygame, sys
from functions import *
from classes import *
from variables import *

pygame.init()

def game(screen, surface, settings):
    #create any and all objects

    LeftClick = False
    RightClick = False
    score = []

    running = True
    while running:
        #--------------UPDATE-BACKGROUND---------#
        surface.fill((0,0,0,0))
        #---------------------------------------#
        #-------------INPUT-LOGIC----------------#
        LeftClick = False
        RightClick = False
        #-----------------------------------------#
        #------------PYGAME-EVENT-HANDLING----------#
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return score
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #if left click
                    LeftClick = True
                if event.button == 3: #if right click
                    RightClick = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    LeftClick = False
                if event.butotn == 3:
                    RightClick = False
        #--------------------------------------------------#
        #----------DRAW-THE-SURFACE-TO-THE-SCREEN-----------#
        screen.fill((0,0,0))
        screen.blit(surface, (0,0))
        pygame.display.flip()
        mainClock.tick(FPS)
        #---------------------------#

if __name__ == "__main__":
    print()
    print("Cannot run this file :(")
    print()