import pygame, sys, random
from functions import *
from classes import *
from variables import *

pygame.init()

def draw_grid(surface, grid, settings)->'pygame.Surface':
	surface.fill((230,200,200))
	for y in range(grid.height):
		for x in range(grid.width):
			tile = grid.grid[y][x]

			create_rect = pygame.Rect(x*TILE_SIZE,y*TILE_SIZE,TILE_SIZE,TILE_SIZE)
			
			#handle the type logic here

			pygame.draw.rect(surface,(255,255,255),create_rect)
			#draw border around tile
			pygame.draw.rect(surface,(0,0,0),create_rect, 1)
	return surface