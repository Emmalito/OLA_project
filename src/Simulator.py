"""
	Implementation of the class Simulator
	which is used for simulate the Environment of the project
"""

## Libraries
import numpy as np
from Graph import Graph


class Simulator:
	"""Class which represents a Simulator of an
	environment with graphs"""

	#Initialisation
	def __init__(self, infos, mus, alphas, nbGraphs):
		"""
			Args:
			infos (list of list of list): List of infos for one graph
			mus (list): List of the lambda for each graphs 	
			alphas (list of list): List of alphas for each graphs
			nbClasses (int): Number of graph

			Return:
				None
		"""
		self.graphs = []
		self.current = []
		self.alphas = alphas
		for graph in range(nbGraphs):
			self.graphs.append(Graph(mus[graph], infos[graph]))
			self.current.append(self.entrance(graph))


	#Accesors
	def getGraph(self, classe):
		""" Return the graph in position 'classe' """
		return self.graphs[classe]
	
	def getPrimary(self, classe):
		"""Return the Current state of the graph"""
		return self.current[classe]
	

	# Methods
	def click(self, classe):
		current = self.getPrimary(classe)
		if current == None:
			return exit # case where either on competitor site, or no more product can be click because all have already been display
		new_primary = self.graphs[classe].getNextNode(current)
		self.graphs[classe].nodeVisited(current) # mettre a visiter au moment on ou click dessus ou quand on part de la page?
		self.current[classe] = new_primary
		return new_primary

	def entrance(self, classe):
		"""Define the 1st webpage"""
		alphas = self.alphas[classe]
		nb_prod = len(alphas)
		first_arrival = np.random.choice(np.arange(0, nb_prod), p=alphas)
		if first_arrival == 0 :#competitor
			return None
		else :
			return first_arrival-1 #id of node

	def generateAlpha(self, expectedAlphas):
		"""Generate the noisy alphas"""
		noisyAlphas = []
		n_MAX_customers = 1000
		alpha_ratio = np.random.multinomial(n_MAX_customers, expectedAlphas)
		noisyAlphas = np.random.dirichlet(alpha_ratio)
		return noisyAlphas
