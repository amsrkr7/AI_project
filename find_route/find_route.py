
import sys

class Node:
	def __init__(self, city, parent_info,cum_cost, depth,f_of_n):
		self.city = city
		self.parent_info = parent_info
		self.cum_cost = cum_cost
		self.depth = depth
		self.f_of_n = f_of_n

def read_inFile(inFile):
	inFile_content = []

	data = open(inFile)

	for line in data:
		inFile_content.append(line)
	
	data.close()
	return inFile_content

def read_hFile(hFile):
	hFile_content = []

	h_data = open(hFile)

	for line in h_data:
		hFile_content.append(line)
	h_data.close()
	return hFile_content

def expand(arcs,fringe,closed):
	parent_node = fringe[0]
	city = parent_node.city
	cost = parent_node.cum_cost

	closed.append(city)

	del fringe[0]

	for each_arc in arcs:
		if city in each_arc:
			if each_arc[0] == city and not(each_arc[1] in closed):
				new_city_node = Node(each_arc[1],parent_node,float(cost)+float(each_arc[2]),float(each_arc[2]),None)
				fringe.append(new_city_node)

			elif each_arc[1] == city and not(each_arc[0] in closed):
				new_city_node = Node(each_arc[0],parent_node,float(cost)+float(each_arc[2]),float(each_arc[2]),None)
				fringe.append(new_city_node)
	return fringe

def fringe_list(arcs, source, destination):
	fringe = []
	closed = []
	fringe.append(source)

	while True:
		 if not fringe:
		 	return None
		 if (fringe[0].city == destination):
		 	return fringe[0]

		 fringe = expand(arcs,fringe,closed)

		 fringe = sorted(fringe, key=lambda node:node.cum_cost) 


def backtrack(fringe_content):

	print('distance: %f Km' % fringe_content.cum_cost)
	print('route:')
	parent_city = []
	cost_involved = []

	while fringe_content:
		parent_city.append(fringe_content.city)
		cost_involved.append(fringe_content.depth)
		fringe_content = fringe_content.parent_info
	parent_city.reverse()
	cost_involved.reverse()

	del cost_involved[0]

	
	for i in range(0,len(parent_city) - 1):
		print ('%s to %s, %.1f Km' % (parent_city[i][0].upper()+parent_city[i][1:], parent_city[i+1][0].upper()+parent_city[i+1][1:], cost_involved[i]))

def uniform_cost_search(arcs, source, destination):
	fringe_content = fringe_list(arcs, source, destination)
	if fringe_content is None:

		print ('distance:infinity')
		print('route:')
		print ('None')
	else:
		backtrack(fringe_content)


def a_star_expand_node(arcs,h_values,closed_state,fringe):
	parent_node = fringe[0]
	city = parent_node.city
	cost = parent_node.cum_cost
	closed_state.append(city)

	del fringe[0]
	for each_arc in arcs:
		if city in each_arc:
			if each_arc[0] == city and not(each_arc[1] in closed_state):
				for line in h_values:
					if city in line:
						if line[0] == city:
							new_city_node = Node(each_arc[1],parent_node,float(cost)+float(each_arc[2]),float(each_arc[2]),float(cost)+float(each_arc[2])+float(line[1]))
							fringe.append(new_city_node)

			elif each_arc[1] == city and not(each_arc[0] in closed_state):
				for line in h_values:
					if city in line:
						if line[0] == city:
							new_city_node =  Node(each_arc[0],parent_node,float(cost)+float(each_arc[2]),float(each_arc[2]),float(cost)+float(each_arc[2])+float(line[1]))
							fringe.append(new_city_node)

def a_star_fringe(arcs,h_values,source,destination):
	fringe = []
	closed_state = []

	fringe.append(source)

	while True:
		if not fringe:
			return None

		if fringe[0].city == destination:
			return fringe[0]

		a_star_expand_node(arcs,h_values,closed_state,fringe)



		fringe = sorted(fringe, key = lambda node:node.f_of_n)

	
def a_star_search(arcs,h_values,source,destination):
	goal_content = a_star_fringe(arcs,h_values,source,destination)

	
	if goal_content is None:

		print ('distance:infinity')
		print('route:')
		print ('none')
	else:
		backtrack(goal_content)

def main():
	if len(sys.argv) == 4:
		inFile = sys.argv[1]
		source = sys.argv[2].lower()
		destination = sys.argv[3].lower()

	elif len(sys.argv) == 5:
		inFile = sys.argv[1]
		source = sys.argv[2].lower()
		destination = sys.argv[3].lower()
		hFile = sys.argv[4]

	inFile_content = read_inFile(inFile)
	del inFile_content[len(inFile_content) -1]
	
	arcs = []
	for line in inFile_content:
		arcs.append(line.lower().split())
	
	if len(sys.argv) == 4:
		graph_node = Node(source,None, 0,0,None)
		uniform_cost_search(arcs, graph_node, destination)


	if len(sys.argv) == 5:
		h_values = []
		hFile_content = read_hFile(hFile)
		del hFile_content[len(hFile_content) - 1]
		for heuristic in hFile_content:
			h_values.append(heuristic.lower().split())
		
		for heuristic in h_values:
			if source in heuristic:
				if heuristic[0] == source:
					graph_node = Node(source,None,0,0,float(heuristic[1]))

		a_star_search(arcs,h_values,graph_node,destination)


if __name__ == "__main__":
	main()