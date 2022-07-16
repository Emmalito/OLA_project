# Tests Class Graph

import sys
sys.path.append("./src/Simulator")
from Product import Product
from Graph import Graph


def main():
	prod1 = Product(0, [1,0.7, 2,0.3], [7, 11, 13])
	prod2 = Product(1, [0,0.7, 2,0.3], [2, 11, 13])
	prod3 = Product(2, [0,0.7, 1,0.5], [10, 11, 13])

	graph1 = Graph(0.5, [prod1, prod2, prod3])
	graph2 = Graph(0.2, [prod1, prod2, prod3])
	graph3 = Graph(1, [prod1, prod2, prod3])

	# Accessor
	print("List of products = ", graph1.getProduct(0), graph1.getProduct(1), graph1.getProduct(2))
	print("Nb product = ", graph1.getNbProduct())

	#Mutator
	for i in range(3):
		graph1.prodVisited(i)
	try:
		graph1.prodVisited(3)
	except IndexError:
		print("Good")

	# Methods
	graph2.prodVisited(1)
	print("True = ", graph2.alreadyVisited(1))
	graph2.restoreVisited()
	print("False = ", graph2.alreadyVisited(1))

	for _ in range(10):
		print(graph3.getNextProduct(1))
		graph3.restoreVisited()
	

if __name__ == "__main__":
	main()
