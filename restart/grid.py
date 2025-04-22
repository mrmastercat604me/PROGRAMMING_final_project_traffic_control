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

			create_rect = pygame.Rect(x*TILE_SIZE_WIDTH,y*TILE_SIZE_HEIGHT,TILE_SIZE_WIDTH,TILE_SIZE_HEIGHT)

			#handle the type drawing logic here
			if tile.type == 'path':
				pygame.draw.rect(surface,tile.colour,create_rect)
				#draw black border around tile
				pygame.draw.rect(surface,(0,0,0),create_rect, 1)
			elif tile.type == 'obstacle':
				pygame.draw.rect(surface,(0,0,0),create_rect)
				#draw white border around tile
				pygame.draw.rect(surface,(255,255,255),create_rect,1)
			
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

# def populate_destinations(grid,settings):
# 	colour_count = settings.get("colour_count") #return an int
# 	colours_dict = settings.get("colour_list") #return a dict of colours and names
# 	colours_list = random.sample(list(colours_dict.values()),colour_count)
# 	pairs = settings.get("pairs")
# 	tiles_in_pairs = []
# 	for colour in colours_list:
# 		for pair in range(pairs):
# 			location1, location1_edge = select_edge_tile(grid,1,edge_range=edge_range,except_tile=tiles_in_pairs)
# 			tiles_in_pairs.append(location1)
# 			location2, location2_edge = select_edge_tile(grid,1,edge_range=edge_range,except_tile=tiles_in_pairs,except_edge=location1_edge)
# 			tiles_in_pairs.append(location2)
# 			pair1 = DestinationPair(grid,location1,location2,colour)

# def is_surrounded_by_walls(grid,tile):
# 	'''
# 	Checks if all surrounding tiles are obstacles (o.e., walls).
# 	'''
# 	surrounding = grid.get_neighbours(tile, only_type=['obstacle','endpoint','path'])
# 	if not surrounding:
# 		return False

# 	return sum(1 for n in surrounding if n.type == 'obstacle') >= len(surrounding)-1

# def get_valid_neighbours(grid,tile):
# 	"""
# 	Returns a list of valid neighbour coordinates that can be used to carve the maze.
# 	A valid neighbour is an 'obstacle' tile that is surrounded by walls.
# 	"""
# 	valid_neighbours = []

# 	# Use your method to get all neighbours of type 'obstacle'
# 	obstacle_neighbours = grid.get_neighbours(tile, only_type='obstacle')
# 	#shuffle the obstacle neighbours list for more random exploration
# 	random.shuffle(obstacle_neighbours)
# 	for neighbour in obstacle_neighbours:
# 		if is_surrounded_by_walls(grid, neighbour):
# 			valid_neighbours.append(neighbour)

# 	return valid_neighbours

# def generate_labyrinth(grid,start_x,start_y):
# 	#start with a grid of walls
# 	for row in grid.grid:
# 		for tile in row:
# 			tile.type = 'obstacle'
	
# 	#Random Depth-First-Search
# 	stack = [(start_x,start_y)]
# 	grid.get_tile_with_index(start_x,start_y).type = 'path' #set the start tile as a path

# 	#introduce complexity through limit of backtracks
# 	backtrack_limit = 5
# 	while stack:
# 		x, y = stack[-1]
# 		current_tile = grid.get_tile_with_index(x,y)
# 		neighbours = get_valid_neighbours(grid,current_tile)
		
# 		if neighbours:
# 			#randomly choose a neighbour to move to
# 			next_tile = random.choice(neighbours)
# 			#make a path to neighbour
# 			next_tile.type = 'path'
# 			#push the current tile to the stack and move to the next tile
# 			stack.append((next_tile.x,next_tile.y))
# 		#allow backtracking after a few moves
# 		elif len(stack) > backtrack_limit:
# 			stack.pop()
# 		else:
# 			#backtrack if there are no valid neighbours
# 			stack.pop()

def add_branching(grid,chance=0.05):
	#iterate through the grid
	for row in grid.grid:
		for tile in row:
			if tile.type != 'obstacle':
				continue
			elif tile.type == 'obstacle':
				#get the obstacle's neighbours
				path_neighbours = grid.get_neighbours(tile,only_type='path')
				#if there is 2 or more neighbours, and a random chance that random.random() is < 0.05
				if len(path_neighbours) >= 2 and random.random() < chance:
					# make the current obstacle tile a path tile.
					tile.type = 'path'

def generate_labyrinth_prims(grid,start_x,start_y):
	#start with a grid of walls
	for row in grid.grid:
		for tile in row:
			tile.type = 'obstacle'
	
	#mark the start tile tile as part of the path
	start_tile = grid.get_tile_with_index(start_x,start_y)
	start_tile.type = 'path'

	#Initialise the set of the walls
	walls_set = set()

	#add the neighbouring walls of the start tile
	for neighbour in grid.get_neighbours(start_tile,only_type='obstacle'):
		walls_set.add(neighbour)
	
	#Implementing Prim's Algorithm
	itr = 0
	while walls_set:
		# print(f"Iteration {itr}, Walls left: {len(walls_set)}")

		if itr > 2000: #prevent infinite loop (for testing)
			print("Maximum iterations reached")
			break

		#randomly select a wall
		wall = random.choice(list(walls_set))
		#generate the surrounding path tiles
		neighbours = grid.get_neighbours(wall, only_type='path')

		#if the tile is adjacent to exactly one path, then it can be carved into the final path
		if len(neighbours) == 1:
			wall.type = 'path'

			#add the tile's neighbours to the walls list
			for neighbour in grid.get_neighbours(wall, only_type='obstacle'):
				if (neighbour not in walls_set):
					walls_set.add(neighbour)
		#remove the wall from the walls list
		walls_set.remove(wall)
		itr += 1
	# print(f"Total iterations: {itr}")
	add_branching(grid)

def is_connected(grid):
	'''Basic Breadth First Search to check if all path tiles are connected.'''
	visited = set()
	all_path_coords = set()
	for row in grid.grid:
		for tile in row:
			if tile.type == 'path':
				all_path_coords.add((tile.x, tile.y))
	if not all_path_coords:
		return False
	
	#Use the set as a queue
	start = next(iter(all_path_coords))
	queue = [(start.x, start.y)]
	visited.add(start)

	while queue:
		x, y = queue.pop(0)
		if (x,y) in visited:
			continue
		tile = grid.get_tile_with_index(x,y)
		for neighbour in grid.get_neighbours(tile,only_type='path'):
			coord = (neighbour.x,neighbour.y)
			if coord not in visited:
				visited.add(coord)
				queue.append(coord)

	return visited == all_path_coords

def find_isolated_regions(grid):
	'''Find all isolated regions of path tiles using a BFS.'''
	if is_connected(grid):
		return True
	#Try to connect disconnected regions by adding new paths
	visited = set()
	regions = []

	for row in grid.grid:
		for tile in row:
			if tile.type == 'path' and (tile.x, tile.y) not in visited:
				#BFS to discover the full region
				region = set()
				queue = [(tile.x,tile.y)]
				visited.add((tile.x,tile.y))
				while queue:
					x,y = queue.pop(0)
					region.add((x,y))
					current_tile = grid.get_tile_with_index(x,y)
					for neighbour in grid.get_neighbours(current_tile,only_type='path'):
						coord = (neighbour.x, neighbour.y)
						if coord not in visited:
							visited.add(coord)
							queue.append(coord)
				regions.append(region)
	return regions

def find_closest_region(region1,region2):
	pass

def control_density(grid,target_density=0.5,preserve_tiles=None):
	if preserve_tiles is None:
		preserve_tiles = set()
	#count the total path tiles
	path_tiles:list = []
	for row in grid.grid:
		for tile in row:
			if tile.type == 'path':
				path_tiles.append(tile)
	#total tiles
	total_tiles:int = grid.width * grid.height
	#calculate current density
	current_density:float = len(path_tiles) / total_tiles

	#adjust current_density to meet target_density
	if current_density < target_density:
		#get the obstacle tiles
		obstacle_tiles:list = []
		for row in grid.grid:
			for tile in row:
				if tile.type == 'obstacle':
					obstacle_tiles.append(tile)
		#shuffle the list
		random.shuffle(obstacle_tiles)

		for tile in obstacle_tiles:
			if (tile.x, tile.y) in preserve_tiles:
				continue
			#check if changing this tile to a path would increase the density to closer to the target_density
			tile.type = 'path'
			if is_connected(grid):
				path_tiles.append(tile)
				current_density:float = len(path_tiles) / total_tiles
				if current_density >= target_density:
					break
			else:
				tile.type = 'obstacle'
	elif current_density > target_density:
		#add more obstacles (NOT TYPICALLY USED)
		pass

def populate(grid):
	pass