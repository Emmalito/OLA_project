# Test of the Node class

import sys
sys.path.append("./src")
from Node import *


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
