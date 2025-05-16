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
	#this while loop iterates while there are nodes to search.
	#It looks at each node (that needs to be searched) looks at it's neighbours, and finds the neighbour that is closest to the goal.
	while ToSearchNodes:
		#iterate through all of the search nodes
		currentNode = ToSearchNodes[0]
		for node in ToSearchNodes:
			#select the node with the LOWEST f-cost, or with the lowest h-cost if the f-cost is the same (does this because we want the lowest f-cost (closest to the goal) to reach the goal faster)
			if (node.f < currentNode.f) or (node.f == currentNode.f and node.h < currentNode.h):
				currentNode = node
		
		#add the current node to the processed nodes and remove it from the tosearch nodes
		ProcessedNodes.append(currentNode)
		ToSearchNodes.remove(currentNode)

		#if the goal is reached recreate the path using parents and return that path
		if currentNode == goal_tile:
			#make the path backwards
			currentPathTile = goal_tile
			path = []
			#while loop to create a path using parent nodes
			while currentPathTile != start_tile:
				path.append(currentPathTile)
				currentPathTile = currentPathTile.parent_node
			path.append(start_tile)
			#fix the path direction
			path.reverse()
			return path

		#iterate through all of the neighbours of the currentNode
		for neighbour in grid.get_neighbours(currentNode,only_type):
			#ignore the neighbours that have been processed already
			if neighbour in ProcessedNodes:
				continue
			
			#calculate the cost from the start node to the current neighbour node
			costToNeighbourNode = currentNode.g + currentNode.generate_manhattan_distance(neighbour)

			#if the neighbour is not already needing to be searched, add it to that list.
			#OR if the calculated cost above is less than the neighbours cost from the start node (meaning this path is better than the one to get here)
			if (neighbour not in ToSearchNodes) or (costToNeighbourNode < neighbour.g):
				g = costToNeighbourNode #g can possibly change depending on the path we took
				h = neighbour.generate_manhattan_distance(goal_tile)
				f = g + h
				neighbour.set_tile_values(g,h,f)
				neighbour.parent_node = currentNode
				#add the neighbour in to the ToSearchNodes list so it can be searched and processed.
				if (neighbour not in ToSearchNodes):
					ToSearchNodes.append(neighbour)

	#if no path is found, return an empty path
	return []

#if the user tries to run THIS file.
if __name__ == "__main__":
	print()
	print("Cannot run this file :(")
	print()