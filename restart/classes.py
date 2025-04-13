import pygame
from functions import *

class Button():
	def __init__(self, x, y, width, height, surface,color):
		self.x, self.y = x, y
		self.width, self.height = width, height
		self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
		self.surface = surface
		self.color = color
		self.text = False
	
	def centerx(self, x:int):
		self.rect.centerx = x
	
	def collidepoint(self, pos):
		return self.rect.collidepoint(pos)
	
	def set_text(self, text, font, color):
		self.text = True
		self.text = text
		self.font = font
		self.text_color = color
	
	def draw(self):
		temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
		temp_surface.fill(self.color)
		self.surface.blit(temp_surface, self.rect)
		if self.text != None:
			draw_text(self.text ,self.font,self.text_color, self.surface, 0,0, self.rect)
