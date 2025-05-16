import pygame, random
from functions import *
from classes import *
from variables import *

pygame.init()

def draw_grid(surface:pygame.Surface, grid:Grid)->'pygame.Surface':
	'''
	Draws the grid with all of the tiles with their respective colours and borders.

	"surface" is a pygame.Surface to pass in.

	"grid" is a Grid to pass in.

	Returns the updated coloured surface to be used.
	'''
	surface.fill((230,200,200))
	for y in range(grid.height):
		for x in range(grid.width):
			tile = grid.grid[y][x]

			create_rect = pygame.Rect(x*TILE_SIZE_WIDTH,y*TILE_SIZE_HEIGHT,TILE_SIZE_WIDTH,TILE_SIZE_HEIGHT)

			#handle the type drawing logic here
			if tile.type == 'path' or tile.type == 'route':
				pygame.draw.rect(surface,tile.colour,create_rect)
				#draw black border around tile
				pygame.draw.rect(surface,(0,0,0),create_rect, 1)
			elif tile.type == 'obstacle':
				pygame.draw.rect(surface,(0,0,0),create_rect)
			
	return surface

def iterate_grid(grid:Grid,condition=None):
	'''
	Iterate through the "grid" yielding all tiles with "condition" if any (otherwise yield all tiles).
	
	"condition" is a lambda to assess the tile(s) by.
	
	ex: (lambda tile: tile.type == "path")

	---This returns all tiles that have the type of "path"

	Yields all tiles with "condition"
	'''
	for row in grid.grid:
		for tile in row:
			if (condition is None) or condition(tile):
				yield tile

def add_branching(grid:Grid,chance:float=0.05):
	'''
	Iterate through the "obstacle" tiles and randomly select a tile that has two or more "path" neighbours.

	"chance" is a float between 0 and 1 that determines the random chance a tile is turned into a "path".

	Returns None
	'''
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

def generate_labyrinth_prims(grid:Grid,start_x:int=0,start_y:int=0)->Grid:
	'''
	Generate a Labyrinth using Prim's Method
	
	"start_x" is an optional int value for a starting x (default is 0)

	"start_y" is an optional int value for a starting y (default is 0)

	Returns an updated grid
	'''
	#turn all tiles in the grid into obstacles
	for tile in iterate_grid(grid):
		tile.type = 'obstacle'
	
	#mark the "start_tile" tile as part of the path
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
	return grid

def is_connected(grid:Grid,type:str='path'):
	'''
	Basic Breadth First Search to check if all "type" tiles are connected.

	"type" is a tile.type to check if all tiles of the same type are connected (default is 'path').

	Returns a bool (True or False) depending on if all tiles can reach all other tiles.
	'''
	all_path_tiles = set(iterate_grid(grid, lambda t: t.type == type))
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

def bfs_region(grid:Grid,start_tile:Tile)->set[tuple[int,int]]:
	'''
	Find all tiles that are connected (the same type as start_tile) using the start_tile as a starting position.

	Finds regions using a Breadth First Search approach.

	"start_tile" is a tile to start from and to branch away from.

	Returns a set of all of the tiles' positions in a region.
	'''
	visited = set()
	queue = [(start_tile.x, start_tile.y)]
	region = set()
	# visited.add((start_tile.x, start_tile.y))

	while queue:
		x, y = queue.pop(0)
		region.add((x,y))
		tile = grid.get_tile_with_index(x,y)
		for neighbour in grid.get_neighbours(tile,only_type=start_tile.type):
			coord = (neighbour.x, neighbour.y)
			if coord not in visited:
				visited.add(coord)
				queue.append(coord)
	return region

def bfs_tile(grid:Grid,start_tile:Tile, goal_tile:Tile,only_type:list[str] =['path'],exclude_tiles:list[Tile]=[]) ->list[Tile]:
	'''
	Find a "goal_tile" from a "start_tile" using a Breadth First Search.

	"start_tile" is a tile in the grid to start from.

	"goal_tile" is a different tile in the grid to end at.

	"only_type" is a type(s) of tile.type to only include in the search.

	"exclude_tiles" is a list of tiles to exclude in the search.

	Returns a list of the path found (Returns [] if no path is found)
	'''
	total_useable_tiles = []
	for tile_type in only_type:
		current_useable_tiles = list(iterate_grid(grid,lambda t:t.type == tile_type))
		total_useable_tiles += current_useable_tiles
	print('finding route using BFS')

	queue = [start_tile]
	explored = [start_tile]
	start_tile.parent_node = None

	while len(queue) != 0:
		print('in while loop')
		currentNode = queue.pop(0)
		if currentNode == goal_tile:
			print('goal tile reached in while loop')
			#make path out and return the path
			currentPathNode = goal_tile
			path = []
			while currentPathNode != None:
				path.append(currentPathNode)
				currentPathNode = currentPathNode.parent_node
			path.reverse()
			return path
		print('current node is not goal_tile')
		for neighbour in grid.get_neighbours(currentNode):
			# print(f'append {neighbour} to the explored and to the queue')
			if neighbour not in explored and neighbour in total_useable_tiles and neighbour not in exclude_tiles:
				explored.append(neighbour)
				# print("make the neighbour's parent node the current node")
				neighbour.parent_node = currentNode
				queue.append(neighbour)
	return []

def find_isolated_regions(grid:Grid)-> bool | list[set[tuple[int,int]]]:
	'''
	Find all isolated regions of path tiles using a BFS.
	
	Each region is a set of connected tiles' positions { (x, y), (x, y), ...}.

	Returns a list of all isolated regions
	'''
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

def find_closest_region(region1:set[tuple[int,int]] | list[tuple[int,int]] ,region2:set[tuple[int,int]] | list[tuple[int,int]])->tuple:
	'''
	Finds the closest straight path between two regions.

	"region1" is a region or a set of tiles that are connected.
	"region2" is a second region.

	Returns the two closest tiles' positions from each region ( (x1, y1), (x2, y2) )
	'''
	min_distance = float('inf')
	closest_pair = None

	for (x1, y1) in region1:
		for (x2, y2) in region2:
			distance = manhattan_distance((x1,y1),(x2,y2))
			if distance < min_distance:
				min_distance = distance
				closest_pair = ((x1,y1),(x2,y2))
	return closest_pair

def create_path(grid:Grid, start:tuple[int,int], end:tuple[int,int], protected_types:list[str]=[]) -> list:
	'''
	Create a *straight* path between two tiles by turning the connecting tiles into the same type as the start and end tiles.
	
	"start" is a starting tile's position.
	
	"end" is an ending tile's position.

	"protected_types" is a list containing all of the tile types that cannot be modified.

	"start" and "end" have to have the same type otherwise a path cannot be made.

	Returns a list of the connecting path tiles' postitions. [ (x, y), (x, y), ... ]
	'''

	x1, y1 = start
	x2, y2 = end
	path_tiles = []
	start_tile_type = grid.get_tile_with_index(x1,y1).type
	goal_tile_type = grid.get_tile_with_index(x2,y2).type
	if start_tile_type == goal_tile_type:
		tile_type = start_tile_type
	else:
		raise Exception("'start' and 'end' should be postions of tiles of the same types.")

	#Horizontal path
	if x1 == x2:
		for y in range(min(y1,y2), max(y1,y2)+1):
			tile = grid.get_tile_with_index(x1,y)
			if tile.type not in protected_types:
				tile.type = tile_type
			path_tiles.append((x1,y))
	
	#vertical path
	elif y1 == y2:
		for x in range(min(x1,x2), max(x1,x2)+1):
			tile = grid.get_tile_with_index(x,y1)
			if tile.type not in protected_types:
				tile.type = tile_type
			path_tiles.append((x,y1))
	
	#L-shaped path
	#go horizonal first, then vertical
	else:
		#random order
		if random.choice([True,False]):
			for x in range(min(x1,x2), max(x1,x2)+1):
				tile = grid.get_tile_with_index(x,y1)
				if tile.type not in protected_types:
					tile.type = tile_type
				path_tiles.append((x,y1))
			for y in range(min(y1, y2), max(y1, y2)+1):
				tile = grid.get_tile_with_index(x2,y)
				if tile.type not in protected_types:
					tile.type = tile_type
				path_tiles.append((x2,y))
		else:
			for y in range(min(y1, y2), max(y1, y2)+1):
				tile = grid.get_tile_with_index(x2,y)
				if tile.type not in protected_types:
					tile.type = tile_type
				path_tiles.append((x2,y))
			for x in range(min(x1,x2), max(x1,x2)+1):
				tile = grid.get_tile_with_index(x,y1)
				if tile.type not in protected_types:
					tile.type = tile_type
				path_tiles.append((x,y1))
	
	#return
	return path_tiles

def connect_isolated_regions(grid:Grid,max_region_size:int=10)->Grid:
	'''
	Connect isolated regions of path tiles to ensure a fully connected grid.

	"max_region_size" is an integer for the max tiles in a region (default is 10).

	Returns the updated Grid
	'''
	regions:list[set] | bool = find_isolated_regions(grid)
	if isinstance(regions, bool) and regions == True:
		return grid

	made_progress = True
	while (len(regions) > 1) and (made_progress):
		made_progress = False
		#find the closest pair of regions
		closest_pair = None
		min_distance = float('inf')
		region1, region2 = set(), set()

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

def connect_corners_to_center(grid:Grid) -> None:
	'''
	Creates paths from the corners in towards the center of the grid.

	Returns Nothing
	'''
	width, height = grid.width, grid.height
	corners = [(0,0), (width-1,0), (0,height-1), (width-1, height-1)]
	center = (width // 2, height // 2)

	for corner in corners:
		create_path(grid, corner, center)
#===========================================================================#

def create_maze(grid:Grid)->Grid:
	'''
	Creates a randomized maze using a grid.

	"grid" is a Grid.

	Returns the updated grid.
	'''
	# print("Generating Labyrinth...")

	generate_labyrinth_prims(grid, (grid.width-1)//2, (grid.height-1)//2)

	add_branching(grid)

	grid = connect_isolated_regions(grid)

	connect_corners_to_center(grid)

	return grid

def return_edge_tiles(grid,edge_range:int=3,except_tile:Tile=None,type='path')->dict:
	'''
	The argument "edge_range" is how far from the edge to include the tiles from.

	The argument "except_tile" is a tile(s) to avoid.

	The argument "type" is a tile.type to only include in the search.
	
	Returns a dict of edges and a list of the tiles in that edge (one tile may be in more than one edge). {'edge': [tile,tile,...]}
	'''
	#-----GENERATE-LIST-OF-ALL-AVAILABLE-TILES----#
	total_tiles = []
	for tile in iterate_grid(grid,lambda t:t.type == type):
		if isinstance(except_tile,Tile):
			if tile == except_tile:
				continue
		elif isinstance(except_tile,list):
			if tile in except_tile:
				continue
		else:
			if tile not in total_tiles:
				total_tiles.append(tile)
	#---------------------------------------------#
	#---make-the-temp-edge-lists---#
	temp_top = []
	temp_left = []
	temp_bottom = []
	temp_right = []
	#---------------#
	#-----SORT-TILES-AND-ADD-TO-THE-PROPER-LIST-----#
	for tile in total_tiles:
		#if the tile is on the top edge
		if tile.y < edge_range:
			if tile not in temp_top:
				temp_top.append(tile)
		#if the tile is on the left edge
		if tile.x < edge_range:
			if tile not in temp_left:
				temp_left.append(tile)
		#if the tile is on the bottom edge
		if tile.y > (grid.height-1-edge_range):
			if tile not in temp_bottom:
				temp_bottom.append(tile)
		#if the tile is on the right edge
		if tile.x > (grid.width-1-edge_range):
			if tile not in temp_right:
				temp_right.append(tile)
	#----------#
	#------UPDATE-edge_tiles-----#
	edge_tiles = {
		'top': temp_top,
		'left':temp_left,
		'bottom':temp_bottom,
		'right':temp_right
	}
	#-----RETURN-TILE(S)-----#
	return edge_tiles

def create_valid_locations(grid,pairs:int=3,max_global_attempts:int=50,max_pair_attempts:int=50,edge_range:int=3,avoid_radius:int=7)->list:
	'''
	Creates "pairs" many paths of tiles that don't intersect.

	"pairs" is an integer of how many paths to attempt to create"

	"max_global_attempts" is an integer of how many total attempts to make all three pairs.

	"max_pair_attempts" is an integer of how mnay total attempts to make one pair.

	"edge_range" is an integer to determine what edge tiles are to be selected for starting and ending points.

	"avoid_radius" is an integer to determine a minimum manhattan radius (not length) of each route.

	Returns a list of paths where each path is a list that contains tiles
	'''
	temp_grid = grid.copy()
	edge_tiles_dict = return_edge_tiles(temp_grid,edge_range,type='path')

	attempt = 0
	while attempt <= max_global_attempts:
		attempt += 1
		#place each pair
		exclude_tiles = []
		reservations = []
		for pair_num in range(pairs):
			pair_made = False
			pair_attempts = 0
			while pair_made is False:
				if pair_attempts > max_pair_attempts:
					return None
				else:
					pair_attempts += 1
				#PROBLEM HERE WHERE EVENTUALLY (POSSIBLY) THE CHOSEN EDGE MAY ONLY HAVE TILES THAT ARE IN THE EXCLUDE_TILES
				start_edge = random.choice(list(edge_tiles_dict.keys()))
				while True:
					start_tile = random.choice(edge_tiles_dict[start_edge])
					if start_tile not in exclude_tiles:
						break
				#------#
				while True:
					goal_edge = random.choice(list(edge_tiles_dict.keys()))
					if goal_edge != start_edge:
						goal_tile = random.choice(edge_tiles_dict[goal_edge])
						if (goal_tile != start_tile) and (manhattan_distance((start_tile.x,start_tile.y),(goal_tile.x,goal_tile.y)) > avoid_radius) and (goal_tile not in exclude_tiles):
							break

				route = bfs_tile(temp_grid,start_tile,goal_tile,'path',exclude_tiles)

				if route:
					reservations.append(route)
					for tile in route:
						exclude_tiles.append(tile)
					pair_made = True

				if pair_made is False:
					for tile in reservations[-1]:
						exclude_tiles.remove(tile)
					reservations.pop(-1)
		if len(reservations) == pairs:
			return reservations