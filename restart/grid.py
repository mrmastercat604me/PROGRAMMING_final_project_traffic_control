import pygame, sys, random
from functions import *
from classes import *
from variables import *

pygame.init()

def draw_grid(surface, grid)->'pygame.Surface':
	surface.fill((230,200,200))
	for y in range(grid.height):
		for x in range(grid.width):
			tile = grid.grid[y][x]

			create_rect = pygame.Rect(x*TILE_SIZE,y*TILE_SIZE,TILE_SIZE,TILE_SIZE)

			#handle the type drawing logic here
			pygame.draw.rect(surface,tile.colour,create_rect)
			#draw border around tile
			pygame.draw.rect(surface,(0,0,0),create_rect, 1)
	return surface

def select_edge_tile(grid,count:int=1,edge_range:int=3,except_tile:'Tile'=None,except_edge:str=None):
	'''
	The argument "count" is how many tiles to output.

	The argument "except_tile" is a tile to avoid.

	The argument "except_edge" is an edge to avoid generating a tile from

	The argument "avoid_radius" needs "except_tile"

	Return a tuple of (tile, edge) if count == 1,

	Returns a list of tuples [(tile,edge),(tile,edge)...] if count > 1
	'''
	if count > 4 or count <= 0:
		raise ValueError("Count must be greater than 0 and less than or equal to 4.")
	if count == 4 and except_edge != None:
		raise ValueError("Count cannot be 4 when there is an except_edge.")
	if except_edge:
		except_edge.lower()
		if except_edge not in ["top","left" ,"bottom","right"]:
			raise SyntaxError("Except edge must be a valid edge.")
	
	x_max = grid.width -1
	#0 to x_max are valid indexes
	y_max = grid.height -1
	#0 to y_max are valid indexes
	#-----DECLARE-EDGES-AND-LAMBDA-TO-CREATE-RANDOM-X,Y-VALUES-----#
	edges = {
		#edge name		#(generate random x value, generate random y value) when called
		"top": lambda: (random.randint(0,x_max),random.randint(0,edge_range-1)),
		"left": lambda: (random.randint(0,edge_range-1),random.randint(0,y_max)),
		"bottom": lambda: (random.randint(0,x_max),random.randint(y_max-edge_range-1,y_max)),
		"right": lambda: (random.randint(x_max-edge_range-1,x_max),random.randint(0,y_max))
	}
	#----------#
	#-----GENERATE-LIST-OF-RANDOM-TILES-----#
	random_tiles_list = []
	return_list = []
	for edge, coord_func in edges.items():
		if except_edge:
			if edge == except_edge:
				continue
		finding = True
		while finding:
			x, y = coord_func() #call each lambda
			random_tile = grid.get_tile_with_index(x=x,y=y)
			if except_tile is None:
				random_tiles_list.append((random_tile,edge))
				finding = False
				break #break out of loop to continue to next edge tile
			if (isinstance(except_tile,Tile) and random_tile != except_tile):
				random_tiles_list.append((random_tile,edge))
				finding = False
				break
			if (isinstance(except_tile,list) and random_tile not in except_tile):
				random_tiles_list.append((random_tile,edge))
				finding = False
				break
	#----------#
	#-----RETURN-TILE(S)-----#
	if count == 1:
		return random.choice(random_tiles_list) #return (tile, edge)
	else:
		return_list = list(random.sample(population=random_tiles_list,k=count)) #takes count many items from the population without any repeating elements
		return return_list #[(tile,edge),(tile,edge)...]

def populate_destinations(grid,settings):
	colour_count = settings.get("colour_count") #return an int
	colours_dict = settings.get("colour_list") #return a dict of colours and names
	colours_list = random.sample(list(colours_dict.values()),colour_count)
	pairs = settings.get("pairs")
	edge_range = settings.get("edge_range")
	tiles_in_pairs = []
	for colour in colours_list:
		for pair in range(pairs):
			location1, location1_edge = select_edge_tile(grid,1,edge_range=edge_range,except_tile=tiles_in_pairs)
			tiles_in_pairs.append(location1)
			location2, location2_edge = select_edge_tile(grid,1,edge_range=edge_range,except_tile=tiles_in_pairs,except_edge=location1_edge)
			tiles_in_pairs.append(location2)
			pair1 = DestinationPair(grid,location1,location2,colour)