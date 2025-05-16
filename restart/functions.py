import pygame
from variables import *
from classes import Tile

def draw_text(text:str,font:'pygame.font',color:str,surface:'pygame.Surface',x:int,y:int,centerSurface=None,width:int=None,height:int=None):
		textobj = font.render(text, 1, color)
		original_font_size = font.get_height()
		text_width, text_height = textobj.get_size()
		text_rect = textobj.get_rect()
		if width and height:
				final_width ,final_height = width, height
		if centerSurface:
			#calculate scale and create scale factor
			scale_x = centerSurface.width / text_width
			scale_y = centerSurface.height / text_height
			scale = min(scale_x, scale_y)
			#calculate font size using scale factor and create new font
			new_font_size = int(font.get_height() * scale)
			#make sure the font size does not exceed the original font size
			new_font_size = min(new_font_size, original_font_size)
			new_font = pygame.font.Font(pygame.font.get_default_font(), new_font_size)
			#render the text with new font size
			textobj = new_font.render(text, 1, color)
			#change the text rect to blit the proper sized text
			text_rect = textobj.get_rect()
			text_rect.center = centerSurface.center
		else:
			text_rect.topleft = (x,y)
		surface.blit(textobj,text_rect)

def percent_of(percent:float,total:float) -> float:
		return (percent * total) / 100

def horz_scroll_image(image,surface,y_pos=0,scroll=0)->int:
	'''
	Handles the logic to scroll an image across the screen from right to left.

	image = pygame.image.load(), surface = pygame.Surface,
	
	y_pos = y | Default is 0 | , scroll = int | Default is 0 | 

	Funtion returns scroll value to be plugged back into this function.
	Need a starting scroll value of 0 to be created before any main loop.
	'''
	scroll = scroll
	y = y_pos
	image_width = image.get_width()
	tiles = (SCREEN_WIDTH // image_width) + 1
	for i in range(0,int(tiles)):
		surface.blit(image,((scroll+(i*image_width)), y))
	scroll -= 1
	if abs(scroll) > image_width:
		scroll = 0
	return scroll

def manhattan_distance(pos1,pos2):
	if isinstance(pos1,tuple):
		pos1_x, pos1_y = pos1
	elif isinstance(pos1,Tile):
		pos1_x, pos1_y = pos1.x, pos1.y
	if isinstance(pos2,tuple):
		pos2_x, pos2_y = pos2
	elif isinstance(pos2,Tile):
		pos2_x, pos2_y = pos2.x, pos2.y
		
	manhattan_distance = abs(pos1_x - pos2_x) + abs(pos1_y - pos2_y)
	return manhattan_distance