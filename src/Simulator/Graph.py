"""
	Implementation of a products graph structure
"""

## Libraries
from numpy import product
from numpy.random import binomial


class Graph:
	"""Class which represents a graph"""

	def __init__(self, mu, products, weights):
		"""
			Initialisation of a graph
			Args:
			mu (int): Lambda for the project
			product (list): Products' list
			weights (list): Graph's weights for secondary products
		"""
		self.visited = []
		self.mu = mu
		self.products = products
		self.weights = weights


	# Accessor
	def getLambda(self):
		"""Return the lambda value"""
		return self.mu
		
	def getProduct(self, index):
		""" Return the product with the right index"""
		return self.products[index]
	
	def getNbProduct(self):
		"""Return the number of product in the graph"""
		return len(self.products)

	# Mutator
	def prodVisited(self, index):
		if -1 < index < len(self.products):
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
		p1, p2 = self.products[current].getP1(), self.products[current].getP2()
		w1, w2 = self.weights[current]
		nextProducts = []
		if(binomial(1,w1)):       #If he clicks
			nextProducts.append(p1)
		if(binomial(1, w2*self.mu)):
			nextProducts.append(p2)
		while None in nextProducts:
			nextProducts.remove(None)
		return nextProducts


	def __str__(self) -> str:
		"""String for the standard output"""
		strings = ""
		for product in self.products:
			strings += "\n" + str(product)
		return strings
