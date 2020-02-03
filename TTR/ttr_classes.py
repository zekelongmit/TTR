import ttr_info as info
import math
import itertools
import random

class Map(object):
	"""docstring for Map"""
	def __init__(self, city_map, possible_tickets):
		self.city_map = city_map
		self.possible_tickets = possible_tickets
		self.nodes = self.get_nodes()

	def get_nodes(self):

		nodes = {}

		for i in self.city_map:
			nodes[i] =  Node(i, self.city_map[i])
		return nodes

	def remove_edge(self, road):

		start = self.nodes[road[0]]
		end = self.nodes[road[1]]

		start.remove_neighbor(road[1])
		end.remove_neighbor(road[0])
		del self.city_map[road[0]][road[1]]
		del self.city_map[road[1]][road[0]]
		self.nodes = self.get_nodes()

	def astar(self, start, end):
		# Create start and end node
		start_node = start
		start_node.g = start_node.h = start_node.f = 0
		end_node = end
		end_node.g = end_node.h = end_node.f = 0

		# Initialize both open and closed list
		open_list = []
		closed_list = []

		# Add the start node
		open_list.append(start_node)

		while open_list:

			# Get Current Node
			current_node = open_list[0]
			current_index = 0
			for index, item in enumerate(open_list):
				if item.f < current_node.f: # if the f is less than the "current node" then make it the current node
					current_node = item
					current_index = index
			
			# Pop current off open list, add to closed list
			# print(current_node.name)
			open_list.pop(current_index)
			closed_list.append(current_node)

			# End Condition
			if current_node == end_node:
				total = 0
				car_total = 0
				path = []
				current = current_node
				while current is not None:
					if current.parent is not None:
						total+=current.adj_list[current.parent.name]
						car_total+=info.car_price[current.adj_list[current.parent.name]]
					path.append(current.name)
					current = current.parent
				return path[::-1], total, car_total # Return reversed path


			children = []
			for child in current_node.adj_list:
				this_child = Node(child, self.nodes[child].adj_dict, current_node)
				children.append(this_child)

			# Loop through adjaceny list
			for child in children:

				# Child is on the closed list
				for closed_child in closed_list:
					if child == closed_child:
						continue

				# Create the f, g, and h values
				child.g = current_node.g + 1/child.adj_list[current_node.name]# + info.car_price[child.adj_list[current_node.name]]/5
				if child == end_node:
					child.h = 0
				else: 
					child.h = (((child.pos[0] - end_node.pos[0]) ** 2) + ((child.pos[1] - end_node.pos[1]) ** 2))/100
				child.f = child.g + child.h

				# Child is already in the open list
				for open_node in open_list:
					if child == open_node and child.g > open_node.g:
					    continue

				# Add the child to the open list
				open_list.append(child)


	def best_path_tickets(self, tickets):
		destination_cities = set()	
		for i in tickets:
			destination_cities.add(i[0])
			destination_cities.add(i[1])

		l=list(itertools.permutations(destination_cities))
		paths = []
		car_total_path = []
		total_path = []
		for permutation in l:
			permutation_total = 0
			permutation_car_total = 0
			permutation_path = []
			for i in range(len(permutation)):
				if i != len(permutation)-1:
					path, total, car_total = self.astar(self.nodes[permutation[i]], self.nodes[permutation[i+1]])				
					permutation_path += path
					permutation_total += total
					permutation_car_total += car_total

			paths.append(permutation_path)
			car_total_path.append(permutation_car_total)
			total_path.append(permutation_total)

		min_value = min(total_path)
		min_cars = car_total_path[total_path.index(min_value)]
		min_path = paths[total_path.index(min_value)]

		return min_path, min_cars, min_value


class Node(object):
	"""docstring for Node"""
	def __init__(self, name, adj_dict, parent = None):
		self.name = name
		self.adj_dict = adj_dict
		self.adj_list = self.get_adj_list()
		self.adj_color = self.get_adj_color()
		self.pos = self.get_pos(info.lat_long)
		self.parent = parent
		self.pixel = self.get_pix()

		self.h = 0
		self.f = 0
		self.g = 0


	def __eq__(self, other):
		return self.pos == other.pos

	def get_adj_list(self):
		adj_list = {}
		
		for i in self.adj_dict:
			adj_list[i] = self.adj_dict[i][0]
		return adj_list

	def get_adj_color(self):
		adj_color = {}
		
		for i in self.adj_dict:
			adj_color[i] = self.adj_dict[i][1]
		return adj_color

	def get_pos(self, lat_long):
		return lat_long[self.name]

	def remove_neighbor(self, other):
		del self.adj_list[other]
		del self.adj_color[other]

	def get_pix(self):
		x = 52 - (self.pos[1] - 71)
		y = 26 - (self.pos[0] - 25)
		return((x,y))







if __name__ == '__main__':
	sample_tickets = (("Denver","El Paso"),("Kansas City","Houston"),("New York City","Atlanta"))
	nyc = Node('New York City', info.city_map['New York City'])
	boston = Node('Boston', info.city_map['Boston'])
	denver = Node('Denver',info.city_map['Denver'])
	la = Node('Los Angeles', info.city_map['Los Angeles'])
	vancouver = Node('Vancouver', info.city_map['Vancouver'])
	game_map = Map(info.city_map,info.possible_tickets)

	print(nyc.adj_list)
	game_map.remove_edge((nyc.name,boston.name))
	print(game_map.nodes[nyc.name].adj_list)