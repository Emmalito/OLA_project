"""
    Implementation othe object 'Product' that represents a product
	in the project but also a node of a weigthed graph
"""


class Product:
	"""Class which represents a node in a graph"""

	# Initialisation
	def __init__(self, id, infos):
		""" Initialisation of a Product

		Args:
			p1, p2 (int) : secondary display nodes when self is primary, in this order
			w1, w2 (int) : weights associated to them if they are in the first slots 
			id 	   (int) : nb of the node
			visited(bool): tell if the node has already been display
		Return:
			none
		"""
		self.p1,self.w1,self.p2, self.w2 = infos
		self.id = id
		self.prices = []
		self.currentPrice = None  #Int => Index of the current price
		self.visited = False
	
	# Accessor
	def getP1(self):
		"""return first secondary product

		Return:
			int : p1
		"""
		return self.p1

	def getP2(self):
		"""return second secondary product

		Return:
			int : p2
		"""
		return self.p2
	
	def getWeight1(self):
		"""return first weight

		Return:
			int : w1
		"""
		return self.w1
	
	def getWeight2(self):
		"""return second weight

		Return:
			int : w2
		"""
		return self.w2

	def getVisited(self):
		"""tell if the node has been visited

		Return:
			bool : visited
		"""
		return self.visited

	def getPrice(self):
		"""Return the product's list of price
		
		Return:
			list : prices
		"""
		return self.prices

	def getCurrentPrice(self):
		"""Return the current price
		
		Return:
			int: currentPrice
		"""
		return self.prices[self.currentPrice]
	

	# Mutator
	def isVisited(self):
		"""set the node as visited"""
		self.visited = True
	
	def addPrices(self, prices):
		"""Add a list of prices"""
		if len(prices) < 1:
			raise ValueError("The list can not be empty!")
		self.prices = prices
		self.currentPrice = 0
	

	# Methode
	def getNextPrice(self):
		"""Increment the current price and return
		the next price """
		if self.currentPrice == None:
			return None
		if self.currentPrice == len(self.prices) - 1:
			return None
		self.currentPrice += 1
		return self.prices[self.currentPrice]
	
	def __str__(self) -> str:
		string = 'Product n° {} => Primary: {}, Secondary: {}, Status:{}'.format(self.id, (self.p1, self.w1),
																	(self.p2, self.w2), self.visited) 
		return string
	
	def __repr__(self) -> str:
		return "Product()"
