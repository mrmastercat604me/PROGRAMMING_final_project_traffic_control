import pygame, random
from functions import *

class Button():
	def __init__(self, x:int, y:int, width:int, height:int, surface:pygame.Surface,color:tuple):
		'''
		Initialise the object of the "Button" class with these parameters (which turn into attributes)
		
		"x" and "y" are positions on the "surface".

		"width" and "height" are the parameters to determine the size of the button when drawing the button.

		Returns an object or an instance
		'''
		self.x, self.y = x, y
		self.width, self.height = width, height
		self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
		self.surface = surface
		self.color = color
		self.text = False
	
	def centerx(self, x:int):
		'''
		Centres the button's width using a centre x-value
		'''
		self.rect.centerx = x
	
	def collidepoint(self, pos:tuple)->bool:
		'''
		Checks if the button's rectangle is colliding with a specified position.
		
		Returns a bool.
		'''
		return self.rect.collidepoint(pos)
	
	def set_text(self, text:str, font, color:tuple):
		'''
		Gives the button text to be drawn in the draw method.

		"font" is a pygame font
		'''
		self.text = True
		self.text = text
		self.font = font
		self.text_color = color
	
	def draw(self):
		'''
		Draws the button on the surface and text if there is text.
		'''
		temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
		temp_surface.fill(self.color)
		self.surface.blit(temp_surface, self.rect)
		#if the instance has text, draw the text
		if self.text != None:
			draw_text(self.text ,self.font,self.text_color, self.surface, 0,0, self.rect)

class Tile:
	def __init__(self,x:int,y:int,type:str,colour=(255,255,255)):
		'''
		Initiliases an instance of the class using the marked parameters.
		
		"x" and "y" are indexes in a grid.

		"type" is a str ("path","route","obstacle","drawn_[int]")

		Returns an instance of the class.

		'''
		self.x = x
		self.y = y
		self.pos = (x,y)
		self.type = type
		self.colour = colour
		self.g = float('inf')
		self.h = float('inf')
		self.f = float('inf')
		self.parent_node = None
	
	def __lt__(self,node:'Tile') -> bool:
		'''
		Compares two tiles based off of their f value.
		
		Returns a bool.
		'''
		return self.f < node.f

	def __eq__(self,node:tuple | Tile) -> bool:
		'''
		Compares self to a tile or a position (of indexes in the grid) and determines if they are the same based on position.

		Returns a bool.
		'''
		#check the status based on "node" being a Tile
		if isinstance(node, Tile):
			return (self.x == node.x) and (self.y == node.y)
		#check the status based on "node" being a tuple
		if isinstance(node, tuple):
			node_x, node_y = node
			return (self.x == node_x) and (self.y == node_y)
	
	def __hash__(self):
		'''
		Compares tiles based on their position.

		Used in sets/queues

		Returns the hash value
		'''
		return hash((self.x,self.y))
	
	def __repr__(self):
		'''
		How to represent the tile when printing the tile.

		Returns a string
		'''
		return f"({self.x}, {self.y})"
	
	def generate_manhattan_distance(self,node:'Tile') -> int:
		'''
		Use the self node and create a manhattan distance between itself and the "node" parametre.

		Returns an integer distance.
		'''
		self_node = (self.x, self.y)
		node_1 = (node.x, node.y)
		temp_manhattan_distance = manhattan_distance(self_node, node_1)
		return temp_manhattan_distance
	
	def set_tile_values(self,g:int,h:int,f:int):
		'''
		Changes the tile's values using the parametres.
		'''
		self.g = g
		self.h = h
		self. f = (f) if (g+h==f) else (g+h)

	def get_tile_values(self):
		'''
		Returns the current tile's g, h, and f values.
		'''
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
	
	def get_direction(self,tile):
		'''
		Returns the direction the current tile is from the specified tile.
		'''
		#(0,0) and (2,0)
		dx = self.x - tile.x
		dy = self.y - tile.y
		
		if (dx, dy) in DIRECTIONS:
			return (dx, dy)
		else:
			return None
class Grid:
	def __init__(self, width:int, height:int,x:int=0,y:int=0,grid=None):
		'''
		Initialise an instance of the class.

		"width" and "height" are values to specify the index range of the grid.

		"x" and "y" are positions to place the grid on a surface.

		Returns an instance of the class.
		'''
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		#if the grid parametres is a list, use that specified list
		if isinstance(grid,list):
			self.grid = grid
		#otherwise, create a new blank grid of obstacles
		else:
			self.grid = []
			#iterate throght the height
			for y in range(height):
				row = []
				#iterate through the width
				for x in range(width):
					col = Tile(x+self.x, y+self.y,type='obstacle')
					row.append(col)
				self.grid.append(row)
	
	def list_of_tiles(self,count:int)->list:
		'''
		Returns a list of count many random different tiles.
		'''
		#iterate through the entire grid adding EVERY tile to this list
		all_tiles = [tile for row in self.grid for tile in row]
		tiles = list(random.sample(all_tiles,k=count))
		return list(tiles)

	def get_tile_with_index(self, x:int, y:int) -> 'Tile':
		'''
		Return a tile using a specified index based off of visual x and y.
		'''
		if (0 <= x and x < self.width) and (0 <= y and y < self.height):
			return self.grid[y][x]
		else:
			return None
	
	def get_tile_with_pos(self,x:int,y:int) -> 'Tile':
		'''
		Returns a tile using the x and y on the surface/screen.
		'''
		grid_x = ((x-self.x) // TILE_SIZE_WIDTH) -1
		grid_y = ((y-self.y) // TILE_SIZE_HEIGHT) -1
		return self.get_tile_with_index(x=grid_x, y=grid_y)
	
	def get_neighbours(self,tile:'Tile',only_type='path') -> list:
		'''
		Returns a list of all "only_type" direct neighbours using a "tile" as a starting position.
		'''
		neighbours = []
		#iterate through all of the directions
		for direction in DIRECTIONS:
			x_shift, y_shift = direction
			x = tile.x + x_shift
			y = tile.y + y_shift
			neighbour = self.get_tile_with_index(x,y)
			#check if the neighbour is not None
			if neighbour:
				#check if the "only_type" parametre is a str
				if isinstance(only_type,str):
					#if it is, and the neighbour's type matches, add it to the return list
					if neighbour.type == only_type:
						neighbours.append(neighbour)
				#if the "only_type" parametre is a list
				elif isinstance(only_type,list):
					#check if the current neighbour's type matches one of the values, if so: add it to the list.
					if neighbour.type in only_type:
						neighbours.append(neighbour)
		return neighbours
	
	def generate_neighbour_values(self,tile:'Tile',start_tile:'Tile',goal_tile:'Tile'):
		'''
		Generate the tile values for every neighbour of a specified "tile" using a "start_tile" and a "goal_tile"
		'''
		#iterate through each neighbour of the specified tile
		for neighbour in self.get_neighbours(tile):
			neighbour.generate_tile_values(start_tile,goal_tile,grid=self)

	def copy(self):
		'''
		Copy the grid instance using the current grid's grid list
		Return a new instance of the Grid class using the current grid's grid list
		'''
		temp_instance = Grid(self.width,self.height,grid=self.grid)
		return temp_instance
	
#if the user tries to run THIS file.
if __name__ == "__main__":
	print()
	print("Cannot run this file :(")
	print()