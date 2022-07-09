"""
Short Def
"""

# This is the file for the simulator. Its intended to be imported into other files for use.
# Vertex and Graph would be private but python does not allow such. They are not intended to be used outside this file.

# Inspired by https://www.bogotobogo.com/python/python_graph_data_structures.php

## Libraries
import numpy as np
from Graph import Graph
from Node import Node
import random


class Simulator:

	def __init__(self, infos, mu, alphas,nb_classes):
		self.graphs = []
		self.current = []
		for graph in range(nb_classes):
			#print("step ", graph)
			#print(self.generate_alpha(alphas[graph]),mu[graph],infos[graph], sep="\n")
			self.graphs.append(Graph(self.generate_alpha(alphas[graph]),mu[graph],infos[graph]))
			self.current.append(self.entrance(graph))
		


	def generate_alpha(self, alpha):
		alphas = []
		n_MAX_customers = 1000
		alpha_ratio = np.random.multinomial(n_MAX_customers, alpha)
		alphas = np.random.dirichlet(alpha_ratio)
		return alphas

	def getGraph(self, classe):
		return self.graphs[classe]
	
	def getPrimary(self, classe):
		return self.current[classe]
	
	def click(self, classe):
		current = self.getPrimary(classe)
		if current == None:
			return exit # case where either on competitor site, or no more product can be click because all have already been display
		new_primary = self.graphs[classe].getNextNode(current)
		self.graphs[classe].nodeVisited(current) # mettre a visiter au moment on ou click dessus ou quand on part de la page?
		self.current[classe] = new_primary
		return new_primary

	def entrance(self, classe):
		alphas = self.getGraph(classe).getAlphas()
		nb_prod = len(alphas)
		first_arrival = np.random.choice(np.arange(0, nb_prod), p=alphas)
		if first_arrival == 0 :#competitor
			return None
		else :
			return first_arrival-1 #id of node

	
def generate_infos(size, nb_product):
	infos = []
	pick  = [e for e in range(nb_product)]
	for node in range(size):
		#random.randint(0,10)/10 to have human readable probabilities
		#random.randint(0,nb_product) fix the secondary product to display (can it be itself ? if not : random.choice(pick.copy().remove(node)))
		pick_tmp = pick.copy()
		pick_tmp.remove(node)
		tmp = [[random.choice(pick_tmp),random.randint(0,10)/10,random.choice(pick_tmp),random.randint(0,10)/10] for _ in range(nb_product)]
		infos.append(tmp)
	return infos

def generate_mu(size):
	mu = []
	for node in range(size):
		mu.append(random.randint(0,10)/10)
	return mu

def main():
	nb_classes = 3
	nb_product = 5
	expected_alphas = [[0.1,0.2,0.7],[0.3,0.4,0.3],[0.5,0.1,0.4]]
	simu = Simulator(generate_infos(nb_classes,nb_product), generate_mu(nb_classes), expected_alphas, nb_classes)
	for i in range(len(simu.graphs)):
		print(simu.graphs[i])
		print('current : ',simu.current[i])
		print("after click ", simu.click(i))
	




if __name__ == "__main__":
	main()


