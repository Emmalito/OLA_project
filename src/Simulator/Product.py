"""
    Implementation othe object 'Product' that represents a product
	in the project but also a node of a weigthed graph
"""


class Product:
	"""Class which represents a node in a graph"""

	# Initialisation
	def __init__(self, index, infos, prices):
		""" Initialisation of a Product

		Args:
			index (int): The product's index
			infos (list): List of [p1, w1, p2, w2]
				p1, p2 (int) : Secondary products to display
				w1, w2 (int) : weights associated to them if they are in the first slots
			prices (list): List of the product's prices
		"""
		self.id = index
		self.p1,self.w1,self.p2, self.w2 = infos
		self.prices = prices
		self.prices.sort()  #We sort the prices
		self.currentPrice = 0  #Int => Index of the current price
	
	# Accessor
	def getId(self):
		"""Return the product's index"""
		return self.id

	def getP1(self):
		"""return first secondary product"""
		return self.p1

	def getP2(self):
		"""return second secondary product"""
		return self.p2
	
	def getWeight1(self):
		"""return first weight"""
		return self.w1
	
	def getWeight2(self):
		"""return second weight"""
		return self.w2

	def getPrices(self):
		"""Return the product's list of price"""
		return self.prices

	def getCurrentPrice(self):
		"""Return the current price"""
		return self.prices[self.currentPrice]


	# Mutator
	def nextPrice(self):
		"""Increment the current price"""
		if self.currentPrice < len(self.prices) - 1:
			self.currentPrice += 1


	# Methode
	def __str__(self) -> str:
		string = 'Product n° {} => Primary: {}, Secondary: {}'.format(self.id, (self.p1, self.w1),
																	(self.p2, self.w2)) 
		return string
	
	def __repr__(self) -> str:
		return "Product()"
