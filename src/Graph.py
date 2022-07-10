"""
	Implementation of a products graph structure
"""

## Libraries
from numpy.random import binomial
from Product import Product


class Graph:
	"""Class which represents a graph"""

	def __init__(self, mu, infos):
		"""
			Initialisation of a graph
			Args:
			mu (int) : Lambda for the project
			info (list of list) : for each product, it is the list of
								2 products and their weights associated (p1, w1, p2, w2)
		Return:
			none
		"""
		self.mu = mu
		self.products = []
		for num in range(len(infos)):
			self.products.append(Product(num, infos[num]))


	# Accesseur
	def getProduct(self, index):
		""" Return the product with the right index"""
		return self.products[index]


	# Methods
	def getNextProduct(self, current):
		"""Choose with a bernoulli distrib the next product"""
		p1, w1 = self.products[current].getP1(), self.products[current].getWeight1()
		p2, w2 = self.products[current].getP2(), self.products[current].getWeight2()
		if not self.products[p1].getVisited(): #If is not visited
			if(binomial(1,w1)):  #If he clicks
				return p1
		if not self.products[p2].getVisited():
			if(binomial(1, w2*self.mu)):
				return p2
		return None

	def prodVisited(self, index):
		"""Set the visit status of a product"""
		self.products[index].isVisited()

	def __str__(self) -> str:
		"""String for the standard output"""
		strings = ""
		for product in self.products:
			strings += "\n" + str(product)
		return strings
