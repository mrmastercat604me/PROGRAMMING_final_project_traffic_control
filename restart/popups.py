import pygame, sys
from functions import *
from classes import *
from variables import *

pygame.init()

def confirm_game_exit_popup(screen,surface):
    #-----------CREATE-A-TRANSPARENT-SURFACE----------#
    transparent_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    transparent_surface.fill((96,96,96,153))
    #------------------------------------------------#
    #----------------CREATE-THE-BUTTONS--------------#
    confirm_text = Button(percent_of(25,SCREEN_WIDTH),percent_of(10,SCREEN_HEIGHT),percent_of(50,SCREEN_WIDTH),percent_of(10,SCREEN_HEIGHT),surface,(255,255,255,))
    confirm_text2 = Button(percent_of(25,SCREEN_WIDTH),percent_of(20,SCREEN_HEIGHT),percent_of(50,SCREEN_WIDTH),percent_of(10,SCREEN_HEIGHT),surface,(255,255,255,))
    continue_button = Button(percent_of(25,SCREEN_WIDTH),percent_of(35,SCREEN_HEIGHT),percent_of(25,SCREEN_WIDTH),percent_of(10,SCREEN_HEIGHT),surface,(200,200,200,245))
    leave_button = Button(percent_of(25,SCREEN_WIDTH),percent_of(50,SCREEN_HEIGHT),percent_of(25,SCREEN_WIDTH),percent_of(10,SCREEN_HEIGHT),surface,(255,10,10,245))
    #centre the buttons
    confirm_text.centerx(percent_of(50,SCREEN_WIDTH))
    confirm_text2.centerx(percent_of(50,SCREEN_WIDTH))
    continue_button.centerx(percent_of(50,SCREEN_WIDTH))
    leave_button.centerx(percent_of(50,SCREEN_WIDTH))
    #set the text for the buttons
    confirm_text.set_text("Are you sure you want to leave?",font,(0,0,0))
    confirm_text2.set_text("Score will be saved, game will reset.",font,(0,0,0))
    continue_button.set_text("Continue Game",font,(0,0,0))
    leave_button.set_text("Leave to Menu",font,(0,0,0))
    #------------------------------------------------#
    #VARIABLES
    LeftClick = False
    RightClick = False

    running = True
    while running:
        #--------UPDATE-BACKGROUND-----------------#
        surface.blit(transparent_surface,(0,0))
        #------------------------------------------#
        #----------DRAW-THE-BUTTONS----------------#
        confirm_text.draw()
        confirm_text2.draw()
        continue_button.draw()
        leave_button.draw()
        #-------------------------------------------#
        #-------------BUTTON-LOGIC--------------------#
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if continue_button.collidepoint((mouse_x,mouse_y)):
            if LeftClick:
                return False
        if leave_button.collidepoint((mouse_x,mouse_y)):
            if LeftClick:
                return True
        LeftClick = False
        #----------------------------------#
        #-------PYGAME-EVENT-HANDLING----------#
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #left click
                    LeftClick = True
                if event.button == 3: #right click
                    RightClick = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: #left click
                    LeftClick = False
                if event.button == 3: #right click
                    RightClick = False
        #--------------------------------------------------#
        #----------DRAW-EVERYTHING-TO-THE-SCREEN-------------#
        screen.blit(surface,(0,0))
        pygame.display.flip()
        mainClock.tick(FPS)
        #----------------------#

if __name__ == "__main__":
    print()
    print("Cannot run this file :(")
    print()