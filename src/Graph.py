"""
Implementation of a graph structure
"""

## Libraries
from distutils.log import info
from numpy.random import binomial
from Node import Node


class Graph:
	"""Class which represents a graph"""

	def __init__(self, mu, infos):
		self.mu = mu
		self.nodes = []
		for num in range(len(infos)):
			self.nodes.append(Node(num, infos[num]))

	# Accesseur
	def getNode(self, num):
		return self.nodes[num]

	# Methods
	def getNextNode(self, current):
		"""Choose with a bernoulli distrib the next node"""
		p1, w1 = self.nodes[current].getP1(), self.nodes[current].getWeight1()
		p2, w2 = self.nodes[current].getP2(), self.nodes[current].getWeight2()
		if not self.nodes[p1].getVisited(): #If is not visited
			if(binomial(1,w1)):  #If he clicks
				return p1
		if not self.nodes[p2].getVisited():
			if(binomial(1, w2*self.mu)):
				return p2
		return None

	def __str__(self) -> str:
		strings = ""
		for node in self.nodes:
			strings += "\n" + str(node)
		return strings

	def nodeVisited(self, id):
		self.nodes[id].isVisited()
		

def main():
	infos = [[2,0.5,4,1], [2,0.6,4,0.3], [2,0.6,4,0.3], [2,0.6,4,0.3], [2,0.6,4,0.3]]
	g = Graph(1,0.5, infos)
	print(g)
	a = None
	while(a==None):
		a = g.getNextNode(0)
		print(a)

if __name__ == "__main__":
	main()


#a = g.getNextNode()
#while a == None:
#	a = g.getNextNode()
#	print(a)
#print("Winner ", a)