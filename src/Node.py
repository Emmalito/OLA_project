from more_itertools import first


class Node:
	"""Class which represents a node in a graph"""

	# Initialisation
	def __init__(self, id, infos):
		""" Initialisation of a node

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
		self.visited = False
	
	# Accessor
	def getP1(self):
		"""return first secondary product

		Returns:
			int : p1
		"""
		return self.p1

	def getP2(self):
		"""return second secondary product

		Returns:
			int : p2
		"""
		return self.p2
	
	def getWeight1(self):
		"""return first weight

		Returns:
			int : w1
		"""
		return self.w1
	
	def getWeight2(self):
		"""return second weight

		Returns:
			int : w2
		"""
		return self.w2

	def getVisited(self):
		"""tell if the node has been visited

		Returns:
			bool : visited
		"""
		return self.visited
	
	# Mutator
	def isVisited(self):
		"""set the node as visited"""
		self.visited = True

	# Methode
	def __str__(self) -> str:
		string = 'Node {} => Primary: {}, Secondary: {}, Status:{}'.format(self.id, (self.p1, self.w1),
																	(self.p2, self.w2), self.visited) 
		return string
	
	def __repr__(self) -> str:
		return "Node()"



def main():
	first_node = Node(0, [1,0.5,2,0.3])
	second_node = Node(1, [0,0.4,2,0.4])
	third_node = Node(2, [0,0.7,1,0.3])
	print(first_node.getP1(), first_node.getP2(),first_node.getWeight1(),first_node.getWeight2(), first_node.getVisited())
	print(first_node)
	first_node.isVisited()
	print(first_node)
	print(second_node)
	print(third_node)
	
if __name__ == "__main__":
	main()