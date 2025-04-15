import pygame, sys
from functions import *
from classes import *
from variables import *
from popups import *

pygame.init()


def game(screen, surface:pygame.Surface, settings:list)->list:
    '''
    Function to create a new "window" by blanking the surface and drawing everything to the surface. The surface is then blit to the screen.

    screen = pygame.display.set_mode(), surface = pygame.Surface, settings = list (custom or preset)

    Uses surface to draw all the new features. The settings is used for certain difficulty information.
    The screen paramtre is used to blit the surface to the screen properly.

    return settings list to be able to be modified and kept while the window stays active.
    '''
    #create any and all objects

    LeftClick = False
    RightClick = False
    score = []

    running = True
    while running:
        #--------------UPDATE-BACKGROUND---------#
        surface.fill((0,0,0,0))
        #---------------------------------------#
        #----------DRAW-EVERYTHING--------------#
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