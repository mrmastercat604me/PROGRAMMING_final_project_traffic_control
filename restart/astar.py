import pygame
pygame.init()
from classes import Grid, Tile


def find_path_astar(grid:'Grid',start_tile:'Tile',goal_tile:'Tile',only_type:list=['path']) -> list:
	'''
	Uses A* search algorithm to find a valid path of only_type between start_tile and goal_tile.
	
	"start_tile" is a tile to start from.
	
	"goal_tile" is a tile to end at.

	"only_type" is a list of tile.types that are accepted in the search.

	Returns a path from the start_tile to the goal_tile including those two,
	The path is a list of Tiles.
	'''
	#create two lists to separate different 'nodes' visited and needing to search
	ToSearchNodes = []
	ProcessedNodes = []

	#reset start tile values
	g = 0
	h = start_tile.generate_manhattan_distance(goal_tile)
	f = g + h
	start_tile.set_tile_values(g,h,f)
	#add start tile to ToSearchNodes
	ToSearchNodes.append(start_tile)
	
	#while there are nodes to search
	while ToSearchNodes:
		#select the node with the LOWEST f-cost, or with the lowest h-cost if the f-cost is the same
		currentNode = ToSearchNodes[0]
		for node in ToSearchNodes:
			if (node.f < currentNode.f) or (node.f == currentNode.f and node.h < currentNode.h):
				currentNode = node
		
		#add the current node to the processed nodes and remove it from the tosearch nodes
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
		for neighbour in grid.get_neighbours(currentNode,only_type):
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
