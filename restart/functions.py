import pygame
from variables import *

def draw_text(text:str,font:'pygame.font',color:str,surface:'pygame.Surface',x:int,y:int,centerSurface=None,width:int=None,height:int=None):
		'''
		Draws text on a surface using the specified text, font, colour, and position.
		Draws text based on optional parametres of "centerSurface" "width", and "height
		'''
		textobj = font.render(text, 1, color)
		original_font_size = font.get_height()
		text_width, text_height = textobj.get_size()
		text_rect = textobj.get_rect()
		#if there is a specified surface to make the size match or a width and height to match
		if centerSurface or (width and height):
			#if there is a width and a height make the rectangle to be the same size
			if width and height:
				scale_x = width
				scale_y = height
			else:
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
		#otherwise place at x,y no matter the size
		else:
			text_rect.topleft = (x,y)
		surface.blit(textobj,text_rect)

def percent_of(percent:float,total:float) -> float:
		'''
		Calculates and returns a float amount based off of a percent and a total
		'''
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
	#iterate through the amount of tiles needed +1
	for i in range(0,int(tiles)):
		surface.blit(image,((scroll+(i*image_width)), y))
	scroll -= 1
	#if scroll is bigger than the image_width, reset scroll to 0 (helps with avoiding HUGE numbers which are needed for comparison)
	if abs(scroll) > image_width:
		scroll = 0
	return scroll

def extract_coords(object)->tuple:
	'''
	Return x and y coordinates from an object
	'''
	if isinstance(object, tuple):
		return object
	elif hasattr(object,'x') and hasattr(object,'y'):
		return (object.x, object.y)
	else:
		raise Exception("Object is not a tuple or does not have a 'x' and 'y'")

def manhattan_distance(pos1,pos2):
	'''
	Calculates and returns the manhattan distance from one point to another taking many types
	'''
	#extract the coordinates from the positions
	pos1_x, pos1_y = extract_coords(pos1)
	pos2_x, pos2_y = extract_coords(pos2)
		
	manhattan_distance = abs(pos1_x - pos2_x) + abs(pos1_y - pos2_y)
	return manhattan_distance

#if the user tries to run THIS file.
if __name__ == "__main__":
	print()
	print("Cannot run this file :(")
	print()