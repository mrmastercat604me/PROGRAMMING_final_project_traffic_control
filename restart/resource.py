import pygame
import random
import string
import classes as classes


#WINDOW / GRID VARIABLES
TILE_SIZE:int = 20
GRID_WIDTH:int = 30
GRID_HEIGHT:int = 30
SPACING = 2 * TILE_SIZE
WINDOW_WIDTH:int = TILE_SIZE * (GRID_WIDTH) + SPACING
WINDOW_HEIGHT:int = TILE_SIZE * (GRID_HEIGHT) + SPACING
DIRECTIONS:list = [(0,-1),(0,1),(-1,0),(1,0)] #up, down, left, right


class Tile:
	def __init__(self, x:int, y:int, is_walkable:bool=True):
		self.x = x
		self.y = y
		self.is_walkable = is_walkable
		self.is_start:bool = False
		self.is_goal:bool = False
		self.g = float('inf') #make the self.g a float number that is infinitely large
		self.h = float('inf') #manhattan distance < and ^
		self.f = float('inf') #this is the sum of self.g and self.h
		self.parent_node = None #used for backtracking nodes
		self.highlighted = False
	
	def __lt__(self,node:'Tile'):
		return self.f < node.f

	def __eq__(self,node:'Tile') -> bool:
		return (self.x == node.x) and (self.y == node.y)

	def generate_manhattan_distance(self,target_node:'Tile') -> int: 
		pos1_x, pos1_y = self.x, self.y
		pos2_x, pos2_y = target_node.x, target_node.y
		manhattan_distance = abs(pos1_x - pos2_x) + abs(pos1_y - pos2_y)
		return manhattan_distance

	def generate_tile_values(self,start_tile:'Tile',goal_tile:'Tile'):
		g = self.generate_manhattan_distance(start_tile)
		h = self.generate_manhattan_distance(goal_tile)
		f = g + h
		self.set_tile_values(g,h,f)
	
	def set_tile_values(self,g:int,h:int,f:int):
		self.g = g
		self.h = h
		self.f = 0
		self.f = (f) if (g+h==f) else (g+h)
	
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
			f= self.f
		return g, h, f

	def move(self,tile:'Tile'):
		if tile.is_walkable:
			tile.is_start = self.is_start
			tile.is_goal = self.is_goal
			tile.g = float('inf')
			tile.h = float('inf')
			tile.f = float('inf')
			tile.highlighted = self.highlighted

			self.__init__(self.x,self.y)

class Grid:
	def __init__(self, width:int, height:int):
		self.width = width
		self.height = height
		self.grid = []
		for y in range(height):
			row = []
			for x in range(width):
				col = Tile(x,y)
				row.append(col)
			self.grid.append(row)
	
	def toggle_obstacle(self, x:int, y:int):
		if 0 <= x < self.width:
			if 0 <= y < self.height:
				self.grid[y][x].is_walkable = not self.grid[y][x].is_walkable
	
	def get_tile_within_area(self, x:int, y:int) -> 'Tile':
		if 0 <= x < self.width and 0 <= y < self.height:
			return self.grid[y][x]
		else:
			return None
	
	def get_tile_with_pos(self,x:int,y:int) -> object:
		grid_x = (x // TILE_SIZE) -1
		grid_y = (y // TILE_SIZE) -1
		if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
			return self.grid[grid_y][grid_x]
		else:
			return None
	
	def set_goal_tile(self,tile:'Tile'):
		for row in self.grid:
			for tile_itr in row:
				if tile_itr != tile:
					tile_itr.is_goal = False
		if not tile.is_start:
			tile.is_goal = not tile.is_goal

	def get_goal_tile(self) -> object:
		for row in self.grid:
			for tile in row:
				if tile.is_goal:
					return tile
		return None
	
	def set_start_tile(self,tile:'Tile'):
		for row in self.grid:
			for tile_itr in row:
				if tile_itr != tile:
					tile_itr.is_start = False
		if not tile.is_goal:
			tile.is_start = not tile.is_start

	def get_start_tile(self) -> object:
		for row in self.grid:
			for tile in row:
				if tile.is_start:
					return tile
		return None
	
	def get_neighbours(self,tile:'Tile',only_walkable:bool=True) -> list:
		#return list of tiles that are directly adjacent to the tile specified and that are not out of bounds and that are not obstacles
		neighbours = []
		if self.get_tile_within_area(tile.x, tile.y):
			for direction in DIRECTIONS:
				x = tile.x
				y = tile.y
				x_shift, y_shift = direction
				x += x_shift
				y += y_shift
				if self.get_tile_within_area(x,y) and ((only_walkable and self.grid[y][x].is_walkable) or not only_walkable):
					neighbours.append(self.grid[y][x])
			return neighbours
		else:
			return None
	
	def generate_neighbour_values(self,tile:'Tile',start_tile:'Tile',goal_tile:'Tile'):
		for neighbour in self.get_neighbours(tile):
			neighbour.generate_tile_values(start_tile, goal_tile,grid=self)

	def reset_grid(self):
		#reset all g, h, f, and parent nodes for all tiles
		for row in self.grid:
			for tile in row:
				tile.parent_node = None
				tile.g = float('inf')
				tile.h = float('inf')
				tile.f = float('inf')
				tile.highlighted = False


######################################################################
#		PYGAME VISUAL FUNCTION(S)		#
######################################################################

def draw_grid(screen, grid):
	screen.fill((255,255,255))

	for y in range(grid.height):
		for x in range(grid.width):
			tile = grid.grid[y][x]

			create_rect = pygame.Rect(x*TILE_SIZE+(SPACING//2), y*TILE_SIZE+(SPACING//2), TILE_SIZE, TILE_SIZE)
			if tile.is_start:
				colour = (0, 255, 0)
			elif tile.is_goal:
				colour = (255,0,0)
			elif not tile.is_walkable: #if the tile is an obstacle
				colour = (0,0,0)
			elif tile.highlighted:
				colour = (100,100,255)
			else:
				colour = (255,255,255)

			pygame.draw.rect(screen,colour, create_rect)
			#draw black border around each tile
			pygame.draw.rect(screen, (0,0,0), create_rect, 1)
	
	pygame.display.flip()

########################################################################
#		PATHFINDING ALGORITH			#
########################################################################

def find_path_astar(grid:'Grid',start_tile:'Tile',goal_tile:'Tile',only_walkable:bool=True) -> list:
	ToSearchNodes = []
	ProcessedNodes = []

	#reset start tile values
	g = 0
	h = start_tile.generate_manhattan_distance(goal_tile)
	f = g + h
	start_tile.set_tile_values(g,h,f)
	#add start tile to ToSearchNodes
	ToSearchNodes.append(start_tile)
	
	while ToSearchNodes:
		#select the node with the LOWEST f-cost, or with the lowest h-cost if the f-cost is the same
		currentNode = ToSearchNodes[0]
		for node in ToSearchNodes:
			if (node.f < currentNode.f) or (node.f == currentNode.f and node.h < currentNode.h):
				currentNode = node

		ProcessedNodes.append(currentNode)
		ToSearchNodes.remove(currentNode)

		#if the goal is reached
		if currentNode == goal_tile:
			#make the path backwards
			currentPathTile = goal_tile
			path = []
			while currentPathTile != start_tile:
				path.append(currentPathTile)
				currentPathTile = currentPathTile.parent_node
			path.append(start_tile)
			#fix the path direction
			path.reverse()
			return path

		#test each neighbour to find the best neighbour
		for neighbour in grid.get_neighbours(currentNode,only_walkable):
			if neighbour in ProcessedNodes:
				continue

			costToNeighbourNode = currentNode.g + currentNode.generate_manhattan_distance(neighbour)

			if (neighbour not in ToSearchNodes) or (costToNeighbourNode < neighbour.g):
				g = costToNeighbourNode #g can possibly change depending on the path we took
				h = neighbour.generate_manhattan_distance(goal_tile)
				f = g + h
				neighbour.set_tile_values(g,h,f)
				neighbour.parent_node = currentNode

				if (neighbour not in ToSearchNodes):
					ToSearchNodes.append(neighbour)
	#if no path is found, return an empty path
	return []

########################################################################
#		CREATE A VALID PATH FUNCTION	#
########################################################################

def create_valid_path(grid:'Grid',path:list) -> list:
	if len(path) > 0:
		for index, tile in enumerate(path):
			if index < len(path)-1:
				section = [path[index],path[index+1]]
				mini_path = find_path_astar(grid,path[index],path[index+1],False)
				for tile in section:
					path.remove(tile)
				path[index:index+1] = mini_path
		return path
	else:
		return None

########################################################################
if __name__ == "__main__":
	pygame.init()
	screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
	pygame.display.set_caption("Grid Window")
	clock = pygame.time.Clock()

	grid = Grid(GRID_WIDTH,GRID_HEIGHT)

	#make every tile start out as an obstacle
	for row in range(grid.height):
		for col in range(grid.width):
			tile = grid.grid[row][col]
			grid.toggle_obstacle(tile.x, tile.y)


	running = True
	left_click = False
	tile_toggle_path = []
	while running:

		for event in pygame.event.get():

			mouse_x, mouse_y = pygame.mouse.get_pos()

			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				running = False

			if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
				tile = grid.get_tile_with_pos(mouse_x,mouse_y)
				if tile and tile.is_walkable:
					grid.reset_grid()
					grid.set_start_tile(tile)
			
			if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
				grid.reset_grid()
				for row in grid.grid:
					for tile in row:
						if tile.is_goal:
							tile.is_goal = False
						if tile.is_start:
							tile.is_start = False
						if tile.is_walkable:
							tile.is_walkable = False

			if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
				tile = grid.get_tile_with_pos(mouse_x,mouse_y)
				if tile and tile.is_walkable:
					grid.reset_grid()
					grid.set_goal_tile(tile)
			
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				#now make a clear and concise path that adjusts diagonal corners 
				tile_toggle_path = create_valid_path(grid,tile_toggle_path)
				for tile in tile_toggle_path:
					grid.toggle_obstacle(tile.x,tile.y)

				left_click = False
				tile_toggle_path= []

			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				left_click = True
				tile = grid.get_tile_with_pos(mouse_x,mouse_y)
				if tile:
					if (not tile.is_goal) and (not tile.is_start) and (tile not in tile_toggle_path):
						# grid.toggle_obstacle(tile.x, tile.y)
						tile_toggle_path.append(tile)

			if (event.type == pygame.MOUSEMOTION) and left_click:
				tile = grid.get_tile_with_pos(mouse_x,mouse_y)
				if tile:
					if (not tile.is_goal) and (not tile.is_start) and (tile not in tile_toggle_path):
						# grid.toggle_obstacle(tile.x, tile.y)
						tile_toggle_path.append(tile)

			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: # if right click
				tile = grid.get_tile_with_pos(mouse_x,mouse_y)
				if tile:

					start_tile = grid.get_start_tile()
					goal_tile = grid.get_goal_tile()

					if start_tile and goal_tile:
						path = find_path_astar(grid,start_tile,goal_tile)
						if path:
							for node in path:
								node.highlighted = True
						else:
							print("No Path Was Found!!")
						

			
		draw_grid(screen,grid)

		clock.tick(60)
	pygame.quit()

# * NOW WORK ON TILE OBSTACLE_TOGGLE TO WORK WITH A DRAGGING MOUSE (CHECK?)
# * THEN, MAKE A START TILE AND GOAL TILE SHARE SOME ATTRIBUTE SO THEY ARE CONNECTED,
# THAT WAY WE CAN HAVE MULTIPLE STARTS AND GOAL THAT ARE TIED TO THE PROPER CONNECTION