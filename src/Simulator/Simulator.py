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
		self.rewards = {}
		self.visited = {}
		self.graphs = graphs


	#Accesors
	def getGraph(self, index):
		""" Return the graph corresponding to the index"""
		return self.graphs[index]
	

	# Old Methods
	def entrance(self, alphas):
		"""Define the 1st webpage"""
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
	def generateAlpha(self):
		"""Return the noisy alphas for each user class"""
		alphas = []
		for user in self.users:
			alphas.append(user.generateAlpha())
		return alphas


	def runDay(self, numberCustomer):
		"""Simulate a sale day on the ecommerce website"""
		noisyAlphas = self.generateAlpha()
		for prod in range(self.graphs[0].getNbProduct()):
			self.cart[prod] = 0      #Total number of item sold
			self.rewards[prod] = 0   #Total of products sold
			self.visited[prod] = 0
		for _ in range(numberCustomer):
			user = randint(0, len(self.users)-1)
			self.runUser(self.users[user], self.graphs[user], noisyAlphas[user])
		rewards = self.getRewardsPerRound(numberCustomer)
		return self.cart, self.rewards, rewards, self.visited  # Return the 2 dictionnary
	

	def runUser(self, user, graph, alphas):
		"""Simulate a sale day for one class of customer"""
		product = self.entrance(alphas)
		if product != None:   	#If we not on the competitor webpage
			self.runProduct(product, user, alphas, graph)
			graph.restoreVisited()


	def runProduct(self, product, user, alphas, graph):
		"""Simulate the sale of one product for an user"""
		if graph.alreadyVisited(product):
			return None #We stop
		graph.prodVisited(product)
		self.visited[product] += 1
		if user.buyOrNot(graph.getProduct(product).getCurrentPrice()):
			self.rewards[product] += 1
			self.cart[product] += user.nmbItemToBuy()   #We add the number of item in the cart
			nextProducts = graph.getNextProduct(product) #Get the next product(s)
			for nextProd in nextProducts:
				self.runProduct(nextProd, user, alphas, graph)
	

	def getRewardsPerRound(self, nbVisitor):
		"""Simulation of the rewards for each 
		current prices products"""
		rewards = []
		for elem in self.rewards:
			proba = self.rewards.get(elem)/nbVisitor
			rewards.append(np.random.binomial(1,proba))
		return rewards
