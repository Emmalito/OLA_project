"""
Implementation of a graph structure
"""

## Libraries
from numpy.random import binomial
#from src import *


class Node:
	"""Class which represents a node in a graph"""

	# Initialisation
	def __init__(self, number, infos):
		p1, w1, p2, w2 = infos
		self.number = number
		self.p1 = p1
		self.weight1 = w1
		self.p2 = p2
		self.weight2 = w2
		self.visited = 0
	
	# Accessor
	def getP1(self):
		return self.p1

	def getP2(self):
		return self.p2
	
	def getWeight1(self):
		return self.weight1
	
	def getWeight2(self):
		return self.weight2

	def getVisited(self):
		return self.visited
	
	# Mutator
	def isVisited(self):
		self.visited = 1

	# Methode
	def __str__(self) -> str:
		string = 'Node {} => Primary: {}, Secondary: {}'.format(self.number, (self.p1, self.weight1),
																	(self.p2, self.weight2)) 
		return string
	
	def __repr__(self) -> str:
		return "Node()"




class Graph:
	"""Class which represents a graph"""

	def __init__(self, alphas, Lambda, infos):
		self.Lambda = Lambda
		self.alphas = alphas
		self.current = 0
		self.nodes = []
		for num in range(len(infos)):
			self.nodes.append(Node(num, infos[num]))

	# Accesseur
	def getNode(self, num):
		return self.nodes[num]

	# Methods
	def getNextNode(self):
		"""Choose with a bernoulli distrib the next node"""
		p1, w1 = self.nodes[self.current].getP1(), self.nodes[self.current].getWeight1()
		p2, w2 = self.nodes[self.current].getP2(), self.nodes[self.current].getWeight2()
		if self.nodes[p1].getVisited() == 0: #If is not visited
			if(binomial(1,w1)):  #If he clicks
				self.current = p1  #Go to p1
				return p1
		if self.nodes[p2].getVisited() == 0:
			if(binomial(1, w2*self.Lambda)):
				self.current = p2
				return p2
		return None

	def __str__(self) -> str:
		strings = ""
		for node in self.nodes:
			strings += "\n" + str(node)
		return strings
		


"""
class Graph:
	def __init__(self, nodes):
		self.vertices = {}
		self.lamb = 0.5

	def add_vertex(self, id, alpha):
		self.vertices[id] = Vertex(id,alpha)
	
	def add_edge(self, frm, to):
		beta = self.vertices[to].get_alpha()
		self.vertices[frm].add_neighbor(to, beta)
	
	# This function
	def clear(self):
		self.vertices = {}

	def remove_vertex(self, vertex):
		keys = list(self.vertices.keys())[:]
		for key in keys:
			if key == vertex:
				del self.vertices[key]
			else:
				self.vertices[key].remove_connection(vertex)

	def pick_new_product(self, start):
		display = self.vertices[start].pick_display()

		if display == "exit":
			return "exit"
		elif (np.random.uniform() < display[1]):
			self.remove_vertex(start)
			return display[0]
		elif len(display) == 2:
			return "exit"
		elif (np.random.uniform() < display[3] * self.lamb):
			self.remove_vertex(start)
			return display[2]
		else:
			return "exit"


	# A test function to test the picking based on beta distributed values
	def test(self):
		self.clear()
		self.add_vertex("P1", 60)
		self.add_vertex("P2", 30)
		self.add_vertex("P3", 10)
		self.add_vertex("P4", 5)
		self.add_edge("P1","P2")
		self.add_edge("P1","P3")
		self.add_edge("P1","P4")
		self.add_edge("P2","P1")
		self.add_edge("P2","P3")
		self.add_edge("P2","P4")
		self.add_edge("P3","P1")
		self.add_edge("P3","P2")
		self.add_edge("P3","P4")
		return self.vertices["P1"].pick_display()

	def testMC(self, n):
		primaries = []
		secondaries = []
		for i in range(n):
			print("progress: " + str(i/n))
			result = self.test()
			primaries.append(result[0])
			secondaries.append(result[2])

		print("primaries:")
		print(primaries.count("P2"))
		print(primaries.count("P3"))
		print(primaries.count("P4"))
		print("secondaries:")
		print(secondaries.count("P2"))
		print(secondaries.count("P3"))
		print(secondaries.count("P4"))

	def test_pick(self):
		self.test()
		picks = []
		pick = "P1"
		picks.append("P1")
		while pick != "exit":
			pick = self.pick_new_product(pick)
			picks.append(pick)
		print(picks)
"""
infos = [[2,0.3,4,0.3], [2,0.6,4,0.3], [2,0.6,4,0.3], [2,0.6,4,0.3], [2,0.6,4,0.3]]
g = Graph(1,0.2, infos)
#print(g)

n = Node(0, [2,1.6,4,0.3])
#print(n)

#a = g.getNextNode()
#while a == None:
#	a = g.getNextNode()
#	print(a)
#print("Winner ", a)