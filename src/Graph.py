"""
	Implementation of a graph structure
"""

## Libraries
from numpy.random import binomial
from Node import Node


class Graph:
	"""Class which represents a graph"""

	def __init__(self, mu, infos):
		"""
			Initialisation of a graph
			Args:
			mu (int) : Lambda of the 
			info (list of list) : for each product, it is the list of
								2 products and their weights associated (p1, w1, p2, w2)
		Return:
			none
		"""
		self.mu = mu
		self.nodes = []
		for num in range(len(infos)):
			self.nodes.append(Node(num, infos[num]))


	# Accesseur
	def getNode(self, num):
		""" Return the node number 'num' """
		return self.nodes[num]

	# Methods
	def getNextNode(self, current):
		"""Choose with a bernoulli distrib the next node"""
		p1, w1 = self.nodes[current].getP1(), self.nodes[current].getWeight1()
		p2, w2 = self.nodes[current].getP2(), self.nodes[current].getWeight2()
		if not self.nodes[p1].getVisited(): #If is not visited
			if(binomial(1,w1)):  #If he clicks
				return p1
		if not self.nodes[p2].getVisited():
			if(binomial(1, w2*self.mu)):
				return p2
		return None

	def nodeVisited(self, id):
		"""Set the visit status of a node"""
		self.nodes[id].isVisited()

	def __str__(self) -> str:
		"""String for the standard output"""
		strings = ""
		for node in self.nodes:
			strings += "\n" + str(node)
		return strings
