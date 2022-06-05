"""
Short Def
"""

## Libraries
import numpy as np
from src import *

class Vertex:
	def __init__(self, node, alpha):
		self.id = node
		self.alpha = alpha
		self.adjacent = {}

	def add_neighbor(self, neighbor, beta=0):
		self.adjacent[neighbor] = beta

	# This function draws numbers from a beta distribution based on the alpha values of the connections.
	# The largest draw is then the product shown as the first secondary, then the second is picked in the same way
	# among the remaining connections.
	# Also the random variables are normalized and returned to be used as probabilities
	# NOTE: if there are only one connections this will probably crash
	def pick_display(self):
		edges = self.get_connections()

		if len(edges) == 0:
			return "exit"
		elif len(edges) == 1:
			return [edges[0], np.random.beta(self.get_beta(edges[0]), self.alpha, size=None)]

		rolls = []
		for edge in edges:
			rolls.append(np.random.beta(self.get_beta(edge), self.alpha, size=None))
		x1 = max(rolls)
		first = edges[rolls.index(x1)]
		rolls[rolls.index(x1)] = 0
		x2 = max(rolls)
		second = edges[rolls.index(x2)]
		x2 = x2 / (sum(rolls) + x1) 
		x1 = x1 / (sum(rolls) + x1)
		return [first, x1, second, x2]

	def get_connections(self):
		return list(self.adjacent.keys())
	
	def get_id(self):
		return self.id

	def get_alpha(self):
		return self.alpha
	
	def get_beta(self, neighbor):
		return self.adjacent[neighbor]

	def remove_connection(self, connection):
		if connection in self.adjacent.keys():
			del self.adjacent[connection]
