"""
	Implementation of the class Simulator which is used
	for simulate the Environment of the project. The simulator
	runs a simulation for every kind of user and so, contains
	all needed information for the simulation
"""

## Libraries
from random import randint
import numpy as np


class Simulator:
	"""Class which represents a Simulator of an
	environment with graphs"""

	#Initialisation
	def __init__(self, graphs, users):
		"""
			Args:
			graphs (list): List of users graphs
			users (list): List of user's class
		"""
		self.users = users
		self.cart = {}
		self.graphs = graphs


	#Accesors
	def getGraph(self, index):
		""" Return the graph corresponding to the index"""
		return self.graphs[index]
	

	# Old Methods
	def entrance(self, classe):
		"""Define the 1st webpage"""
		alphas = self.alphas[classe]
		nb_prod = len(alphas)
		first_arrival = np.random.choice(np.arange(0, nb_prod), p=alphas)
		if first_arrival == 0 :#competitor
			return None
		else :
			return first_arrival-1 #id of node

	def click(self, classe):
		current = self.getPrimary(classe)
		if current == None:
			return exit # case where either on competitor site, or no more product can be click because all have already been display
		new_primary = self.graphs[classe].getNextProduct(current)
		self.graphs[classe].nodeVisited(current) # mettre a visiter au moment on ou click dessus ou quand on part de la page?
		self.current[classe] = new_primary
		return new_primary

	# Methods
	def runDay(self, numberCustomer):
		"""Simulate a sale day on the ecommerce website"""
		for num in range(self.graphs[0].getNbProduct()):
			self.cart[num] = 0    #Total number of item sold
		for _ in range(numberCustomer):
			user = randint(0, 2)
			self.runUser(user, self.graphs[user])
		#index = 0
		#for user in self.users:
		#	self.runUser(user, self.graphs[index])
		#	index += 1
		return self.cart # Return the number of products sold
	
	def runUser(self, user, graph):
		"""Simulate a sale day for one class of customer"""
		for product in range(graph.getNbProduct()):
			self.runProduct(product, user, user.generateAlpha(), graph)
			graph.restoreVisited()

	def runProduct(self, product, user, alphas, graph):
		"""Simulate the sale of one product for an user"""
		if graph.alreadyVisited(product):
			return None #We stop
		graph.prodVisited(product)
		if user.buyOrNot(graph.getProduct(product).getCurrentPrice()):
			self.cart[product] += user.nmbItemToBuy()   #We add the number of item in the cart
			nextProducts = graph.getNextProduct(product) #Get the next product(s)
			for nextProd in nextProducts:
				self.runProduct(nextProd, user, alphas, graph) #

		



	
	
