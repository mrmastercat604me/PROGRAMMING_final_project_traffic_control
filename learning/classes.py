import pygame
import random
import string

#WINDOW / GRID VARIABLES
TILE_SIZE:int = 50
GRID_WIDTH:int = 20
GRID_HEIGHT:int = 20
WINDOW_WIDTH:int = TILE_SIZE * (GRID_WIDTH+2) #add spacing on all sides
WINDOW_HEIGHT:int = TILE_SIZE * (GRID_HEIGHT+2)

class Car:
	def __init__(self, start, destination, speed:int=2,name:str=""):
		if isinstance(start,tuple):
			self.start = start
			self.x, self.y = self.start
		elif isinstance(start,Location):
			self.start = start
			self.x, self.y = self.start.x, self.start.y
		if isinstance(destination,tuple):
			self.destination = destination
		elif isinstance(destination,Location):
			self.destination = (destination.x, destination.y)
		self.speed = speed
		self.name = name

	def move_to(self,location):
		# use a-star algorithm to move the car to the location via valid pathways
		if isinstance(location,tuple):
			location_x, location_y = location
		elif isinstance(location,Location):
			location_x, location_y = location.x, location.y
		
		self.x = location_x
		self.y = location_y
	
	def arrived(self) -> bool:
		destination_x, destination_y = self.destination
		if self.x == destination_x and self.y == destination_y:
			return True
		else:
			return False
	
	def __repr__(self) -> str:
		return f"{self.name if self.name != "" else "Car"} at Pos: ({self.x}, {self.y})"

class Location:
	def __init__(self,x:int=0,y:int=0,name:str="",pairing_id:str=None):
		self.x = x
		self.y = y
		self.name = name
		self.pairing_id = pairing_id
		self.max_cars = 1
	
	def __repr__(self) -> str:
		return f"{self.name if self.name != "" else "location"} at ({self.x}, {self.y})"


class DestinationPair:
	def __init__(self,spawner_pos:tuple,destination_pos:tuple,spawner_name:str=None,destination_name:str=None,pairing_id:str=None):
		spawner_x, spawner_y = spawner_pos
		self.pairing_id = pairing_id if pairing_id else f"{random.randint(2,128)}{random.choice(string.ascii_lowercase)}{random.randint(128,256)}"
		self.spawner = Location(spawner_x,spawner_y,spawner_name,self.pairing_id)
		destination_x, destination_y = destination_pos
		self.destination = Location(destination_x,destination_y,destination_name,self.pairing_id)
		self.cars = []
	
	def move_car(self,index_of_car:int,destination):
		if len(self.cars) > index_of_car:
			if isinstance(destination,tuple):
				x,y = destination
			elif isinstance(destination,'Location'):
				x,y = destination.x, destination.y
			car = self.cars[index_of_car]
			car.move_to((x,y))
	def make_car(self):
		self.cars.append(Car(self.spawner,self.destination,name="blue_car"))

if __name__ == "__main__":
	print("\n"*3)
	# start = (0,0)
	# end = (3,5)
	# c1 = Car(start,end)

	# for x_step in range(1,4):
	# 	for y_step in range(1,6):
	# 		print(c1)
	# 		if c1.arrived():
	# 			print("The car has arrived at it's destination!")
	# 			playing = False
	# 			break
	# 		input("Enter to step forward")
	# 		c1.move_to((x_step,y_step))
	blue_pair = DestinationPair((0,0),(4,4),"Blue Home","Blue Work")
	print(blue_pair.spawner)
	print(blue_pair.destination)
	print(blue_pair.pairing_id)
	print()
	print("-"*30)
	print()

	print(blue_pair.cars)
	blue_pair.make_car()
	print(blue_pair.cars)
	blue_pair.move_car(0,(1,0))
	print(blue_pair.cars)
			
