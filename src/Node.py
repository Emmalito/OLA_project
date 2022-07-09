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

