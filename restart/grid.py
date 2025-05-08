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
				# pygame.draw.rect(surface,(255,255,255),create_rect,1)
			
	return surface

def select_edge_tile(grid,count:int=1,edge_range:int=3,except_tile=None,except_edge:str=None):
	'''
	The argument "count" is how many tiles to output.

	The argument "except_tile" is a tile or tile.type to avoid.

	The argument "except_edge" is an edge to avoid generating a tile from, edges include: 'top', 'left', 'bottom', 'right'

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
			if (isinstance(except_tile,Tile) and ((random_tile != except_tile) or (random_tile.type != except_tile))):
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

def iterate_grid(grid,condition=None):
	for row in grid.grid:
		for tile in row:
			if (condition is None) or condition(tile):
				yield tile

def add_branching(grid,chance=0.05):
	#iterate through the grid
	for tile in iterate_grid(grid, lambda t: t.type == 'obstacle'):
		path_neighbours = grid.get_neighbours(tile, only_type='path')
		#if there is 2 or more neighbours, and a random chance that random.random() is < 0.05
		if len(path_neighbours) >= 2 and random.random() < chance:
			# make the current obstacle tile a path tile.
			tile.type = 'path'

			#extra randomness
			if random.random() < 0.3:
				neighbours = grid.get_neighbours(tile, only_type='obstacle')
				for neighbour in neighbours:
					if random.random() < 0.2:
						neighbour.type = 'path'

def generate_labyrinth_prims(grid,start_x=0,start_y=0):
	'''Generate a Labyrinth using Prim's Method'''
	#start with a grid of walls
	for tile in iterate_grid(grid):
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
		if itr > 1999: #prevent infinite loop (for testing)
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

def is_connected(grid):
	'''Basic Breadth First Search to check if all path tiles are connected.'''
	all_path_tiles = set(iterate_grid(grid, lambda t: t.type == 'path'))
	if not all_path_tiles:
		return False
	
	#Use the set as a queue
	start = next(iter(all_path_tiles))
	visited = set()
	queue = [(start.x, start.y)]
	visited.add((start.x, start.y))

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

	return visited == all_path_tiles

def bfs_region(grid,start_tile):
	visited = set()
	queue = [(start_tile.x, start_tile.y)]
	region = set()
	# visited.add((start_tile.x, start_tile.y))

	while queue:
		x, y = queue.pop(0)
		region.add((x,y))
		tile = grid.get_tile_with_index(x,y)
		for neighbour in grid.get_neighbours(tile,only_type='path'):
			coord = (neighbour.x, neighbour.y)
			if coord not in visited:
				visited.add(coord)
				queue.append(coord)
	return region

def find_isolated_regions(grid):
	'''Find all isolated regions of path tiles using a BFS.'''
	if is_connected(grid):
		return True
	#Try to connect disconnected regions by adding new paths
	visited = set()
	regions = []

	for tile in iterate_grid(grid, lambda t: t.type =='path'):
		coord = (tile.x, tile.y)
		if coord not in visited:
			region = bfs_region(grid,tile)
			regions.append(region)
			visited.update(region)

	return regions

def find_closest_region(region1,region2):
	'''Find the closest straight path between two regions'''
	min_distance = float('inf')
	closest_pair = None

	for (x1, y1) in region1:
		for (x2, y2) in region2:
			distance = manhattan_distance((x1,y1),(x2,y2))
			if distance < min_distance:
				min_distance = distance
				closest_pair = ((x1,y1),(x2,y2))
	return closest_pair

def create_path(grid, start, end, protected_types:list=[]):
	'''Create a straight path between two tiles.'''
	x1, y1 = start
	x2, y2 = end
	path_tiles = []

	#Horizontal path
	if x1 == x2:
		for y in range(min(y1,y2), max(y1,y2)+1):
			tile = grid.get_tile_with_index(x1,y)
			if tile.type not in protected_types:
				tile.type = 'path'
			path_tiles.append((x1,y))
	
	#vertical path
	elif y1 == y2:
		for x in range(min(x1,x2), max(x1,x2)+1):
			tile = grid.get_tile_with_index(x,y1)
			if tile.type not in protected_types:
				tile.type = 'path'
			path_tiles.append((x,y1))
	
	#horizontal path
	#go horizonal first,, then vertical
	else:
		#random order
		if random.choice([True,False]):
			for x in range(min(x1,x2), max(x1,x2)+1):
				tile = grid.get_tile_with_index(x,y1)
				if tile.type not in protected_types:
					tile.type = 'path'
				path_tiles.append((x,y1))
			for y in range(min(y1, y2), max(y1, y2)+1):
				tile = grid.get_tile_with_index(x2,y)
				if tile.type not in protected_types:
					tile.type = 'path'
				path_tiles.append((x2,y))
		else:
			for y in range(min(y1, y2), max(y1, y2)+1):
				tile = grid.get_tile_with_index(x2,y)
				if tile.type not in protected_types:
					tile.type = 'path'
				path_tiles.append((x2,y))
			for x in range(min(x1,x2), max(x1,x2)+1):
				tile = grid.get_tile_with_index(x,y1)
				if tile.type not in protected_types:
					tile.type = 'path'
				path_tiles.append((x,y1))
	
	#return
	return path_tiles

def connect_isolated_regions(grid,max_region_size=10):
	'''Connect isolated regions of path tiles to ensure a fully connected grid.'''
	regions = find_isolated_regions(grid)

	made_progress = True
	while (len(regions) > 1) and (made_progress):
		made_progress = False
		#find the closest pair of regions
		closest_pair = None
		min_distance = float('inf')
		region1, region2 = None, None

		#for loop iterate through regions, index and regions
		for i, r1 in enumerate(regions):
			for j, r2 in enumerate(regions):
				if i>= j:
					#if we are at the same region or we have already compared the two regions together
					continue
				combined_size = len(r1) + len(r2)
				if combined_size > max_region_size:
					#skip if combining exceeds the max size
					continue
				pair = find_closest_region(r1,r2)
				if pair:
					pos1, pos2 = pair
					distance = manhattan_distance(pos1,pos2)
					if distance < min_distance:
						min_distance = distance
						closest_pair = pair
						region1, region2 = r1, r2
		#now that we have found the closest isolated regions
		#create a path between these two regions
		if closest_pair:
			start, end = closest_pair
			create_path(grid, start, end)

			#make the two regions into one region to reduce the count of regions
			new_region = region1.union(region2)
			regions.remove(region1)
			regions.remove(region2)
			regions.append(new_region)
			made_progress = True
		else:
			break
	#return
	return grid

def control_density(grid,target_density=0.5,preserve_tiles=None):
	'''Control density of path_tiles'''
	if preserve_tiles is None:
		preserve_tiles = set()
	#count the total path tiles
	path_tiles:list = list(iterate_grid(grid, lambda t: t.type == 'path'))
	#total tiles
	total_tiles:int = grid.width * grid.height
	#calculate current density
	current_density:float = len(path_tiles) / total_tiles

	#adjust current_density to meet target_density
	if current_density < target_density:
		#get the obstacle tiles
		obstacle_tiles:list = list(iterate_grid(grid,lambda t: t.type == 'obstacle'))
		#shuffle the list
		random.shuffle(obstacle_tiles)

		for tile in obstacle_tiles:
			if (tile.x, tile.y) in preserve_tiles:
				continue
			#check if changing this tile to a path would increase the density to closer to the target_density
			tile.type = 'path'
			path_tiles:list = list(iterate_grid(grid, lambda t: t.type == 'path'))
			current_density = len(path_tiles) / total_tiles
			
			if current_density >= target_density:
				break
			elif not is_connected(grid):
				tile.type = 'obstacle'
				path_tiles:list = list(iterate_grid(grid, lambda t: t.type == 'path'))
	
	elif current_density > target_density:
		#add more obstacles if density is too high
		path_tiles:list = list(iterate_grid(grid, lambda t: t.type == 'path'))
		random.shuffle(path_tiles)
		for tile in path_tiles:
			if (tile.x, tile.y) not in preserve_tiles:
				tile.type = 'obstacle'
				path_tiles:list = list(iterate_grid(grid, lambda t: t.type == 'path'))
				current_density:float = len(path_tiles) / total_tiles

				if current_density <= target_density:
					break
				elif not is_connected(grid):
					tile.type = 'path'

def connect_corners_to_center(grid):
	width, height = grid.width, grid.height
	corners = [(0,0), (width-1,0), (0,height-1), (width-1, height-1)]
	center = (width // 2, height // 2)

	for corner in corners:
		create_path(grid, corner, center)

def random_cross_connect(grid, count=3, min_distance=5):
	path_coords = [(t.x, t.y) for t in iterate_grid(grid, lambda t: t.type == 'path')]
	random.shuffle(path_coords)

	connections = 0
	for i, start in enumerate(path_coords):
		for end in path_coords[i+1:]:
			if manhattan_distance(start, end) >= min_distance:
				create_path(grid, start, end)
				connections += 1
				break
		if connections >= count:
			break

#===========================================================================#

def populate(grid):
	# print("Generating Labyrinth...")

	generate_labyrinth_prims(grid, (grid.width-1)//2, (grid.height-1)//2)

	# print("Labyrinth Generated.")
	# print()
	# print("Adding Branching...")

	add_branching(grid)

	# print("Branching Added.")
	# print()
	# print("Connecting Isolated Regions...")

	grid = connect_isolated_regions(grid)

	# print("Isolated Regions Connected.")
	# print()
	# print("Controlling density...")

	# control_density(grid,0.01)
	
	# print("Density Controlled")
	# print()
	# print("Connecting corners to center...")

	# connect_corners_to_center(grid)

	# print("Corners connected.")
	# print()
	# print("Adding long-range cross connections...")

	# random_cross_connect(grid, count=4)

	# print("Long-range cross sections connected.")
	return grid
