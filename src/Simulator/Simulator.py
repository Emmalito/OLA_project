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
			users (list): List of user's class
			graphs (list): List of users graphs
		"""
		self.users = users
		self.cart = {}
		self.rewards = {}
		self.visited = {}
		self.pageEntrance = []
		self.graphs = graphs

	#Methods
	def entrance(self, alphas):
		"""Define the 1st webpage for an user"""
		nb_prod = len(alphas)
		first_arrival = np.random.choice(np.arange(0, nb_prod), p=alphas)
		if first_arrival == 0 :#competitor
			return None
		else :
			return first_arrival-1 #id of node


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
		self.pageEntrance = [0 for _ in range(self.graphs[0].getNbProduct()+1)] #Restore the entrance webpage
		for _ in range(numberCustomer):
			user = randint(0, len(self.users)-1)
			self.runUser(self.users[user], self.graphs[user], noisyAlphas[user])
		return self.cart, self.rewards, self.pageEntrance, self.visited  # Return the 2 dictionnary
	

	def runUser(self, user, graph, alphas):
		"""Simulate a sale day for one class of customer"""
		product = self.entrance(alphas)
		if product == None:
			self.pageEntrance[0] += 1
		if product != None:   	#If we not on the competitor webpage
			self.pageEntrance[product+1] += 1
			self.runProduct(product, user, alphas, graph)
			graph.restoreVisited()


	def runProduct(self, product, user, alphas, graph):
		"""Simulate the sale of one product for an user"""
		if graph.alreadyVisited(product):
			return None #We stop
		graph.prodVisited(product)
		self.visited[product] += 1
		price = graph.getProduct(product).getCurrentPrice()
		if user.buyOrNot(price):
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
