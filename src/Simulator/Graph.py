"""
	Implementation of a products graph structure
"""

## Libraries
from numpy.random import binomial


class Graph:
	"""Class which represents a graph"""

	def __init__(self, mu, products):
		"""
			Initialisation of a graph
			Args:
			mu (int) : Lambda for the project
			product (list) : Products' list
		"""
		self.visited = []
		self.mu = mu
		self.products = products


	# Accessor
	def getProduct(self, index):
		""" Return the product with the right index"""
		return self.products[index]
	
	def getNbProduct(self):
		"""Return the number of product in the graph"""
		return len(self.products)

	# Mutator
	def prodVisited(self, index):
		if index < len(self.products):
			self.visited.append(index)
		else:
			raise IndexError("The product ", index, " is not in the graph")


	# Methods
	def alreadyVisited(self, index):
		"""Return if the product is already visited"""
		return index in self.visited

	def restoreVisited(self):
		"""Restore the list of visited product"""
		self.visited = []
	
	def getNextProduct(self, current):
		"""Choose with a bernoulli distrib the next product"""
		p1, w1 = self.products[current].getP1(), self.products[current].getWeight1()
		p2, w2 = self.products[current].getP2(), self.products[current].getWeight2()
		nextProducts = []
		if not p1 in self.visited:    #If is not visited
			if(binomial(1,w1)):       #If he clicks
				nextProducts.append(p1)
		if not p2 in self.visited:
			if(binomial(1, w2*self.mu)):
				nextProducts.append(p2)
		return nextProducts


	def __str__(self) -> str:
		"""String for the standard output"""
		strings = ""
		for product in self.products:
			strings += "\n" + str(product)
		return strings
