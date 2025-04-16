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

class Tile:
	def __init__(self,x:int,y:int,type:str,colour=(255,255,255)):
		self.x = x
		self.y = y
		self.type = type
		self.colour = colour
		self.g = float('inf')
		self.h = float('inf')
		self.f = float('inf')
		self.parent_node = None
	
	def __lt__(self,node:'Tile') -> bool:
		return self.f < node.f

	def __eq__(self,node:'Tile') -> bool:
		return (self.x == node.x) and (self.y == node.y)
	
	def generate_manhattan_distance(self,node:'Tile') -> int:
		self_node = (self.x, self.y)
		node_1 = (node.x, node.y)
		manhattan_distance = manhattan_distance(self_node,node_1)
		return manhattan_distance
	
	def set_tile_values(self,g:int,h:int,f:int):
		self.g = g
		self.h = h
		self. f = (f) if (g+h==f) else (g+h)

	def get_tile_values(self):
		if self.g == float('inf'):
			g = None
		else:
			g = self.g
		if self.h == float('inf'):
			h = None
		else:
			h = self.h
		if self.f == float('inf'):
			f = None
		else:
			f = self.f
		return g, h, f
	
class Grid:
	def __init__(self, width:int, height:int,x:int=0,y:int=0):
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.grid = []
		for y in range(height):
			row = []
			for x in range(width):
				col = Tile(x+self.x, y+self.y,type='#fill this later')
				row.append(col)
			self.grid.append(row)
	
	def get_tile_with_index(self, x:int, y:int) -> 'Tile':
		if (0 <= x and x < self.width) and (0 <= y and y < self.height):
			return self.grid[y][x]
		else:
			return None
	
	def get_tile_with_pos(self,x:int,y:int) -> 'Tile':
		grid_x = ((x-self.x) // TILE_SIZE) -1
		grid_y = ((y-self.y) // TILE_SIZE) -1
		return self.get_tile_with_index(x=grid_x, y=grid_y)
	
	def get_neighbours(self,tile:'Tile',valid_path_only:bool=True) -> list:
		neighbours = []
		if self.get_tile_with_index(tile.x, tile.y):
			for direction in DIRECTIONS:
				x = tile.x
				y = tile.y
				x_shift, y_shift = direction
				x += x_shift
				y += y_shift
				if self.get_tile_with_index(x,y) and ((valid_path_only and self.grid[y][x].type == "path") or not valid_path_only):
					neighbours.append(self.grid[y][x])
			return neighbours
		else:
			return None
	
	def generate_neighbour_values(self,tile:'Tile',home_tile:'Tile',goal_tile:'Tile'):
		for neighbour in self.get_neighbours(tile):
			neighbour.generate_tile_values(home_tile,goal_tile,grid=self)

class DestinationPair:
	def __init__(self, grid:'Grid', spawn_pos, destination_pos, colour:tuple):
		if isinstance(spawn_pos,tuple):
			spawner_x, spawner_y = spawn_pos
			self.spawner_tile = grid.get_tile_with_index(x=spawner_x,y=spawner_y)
		elif isinstance(spawn_pos,Tile):
			self.spawner_tile = spawn_pos

		if isinstance(destination_pos,tuple):
			destination_x, destination_y = destination_pos
			self.destination_tile = grid.get_tile_with_index(x=destination_x,y=destination_y)
		elif isinstance(destination_pos,Tile):
			self.destination_tile = destination_pos

		self.colour = colour
		self.pair = [self.spawner_tile,self.destination_tile]
		self.update_visual()
	
	def update_visual(self):
		for tile in self.pair:
			tile.colour = self.colour