# Tests Class Graph

import sys
sys.path.append("./src")
from Graph import *


def main():
	infos = [[2,0.5,4,1], [2,0.6,4,0.3], [2,0.6,4,0.3], [2,0.6,4,0.3], [2,0.6,4,0.3]]
	g = Graph(0.5, infos)
	print(g)

	a = None
	while(a==None):
		a = g.getNextNode(0)
		print("Primary product is ", a)

if __name__ == "__main__":
	main()