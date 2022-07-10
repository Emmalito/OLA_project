# Test of the Product class

import sys
sys.path.append("./src")
from Product import Product


def main():
	#Initialisation
	first_prod = Product(0, [1,0.5,2,0.3], [5,7,11,9])
	second_prod = Product(1, [0,0.4,2,0.4], [5,7,11,9])
	third_prod = Product(2, [0,0.7,1,0.3], [5,7,11,9])

	#Accessor
	print(first_prod.getP1(), first_prod.getP2(),first_prod.getWeight1(),first_prod.getWeight2(), first_prod.getVisited())
	print("Prices: ", first_prod.getPrice(), " current price: ", first_prod.getCurrentPrice())
	
	#Mutator
	print(first_prod)
	first_prod.isVisited()
	print(first_prod)

	#Methods
	print(second_prod)
	print(third_prod)
	print(first_prod.getCurrentPrice())
	print(first_prod.getNextPrice())
	print(first_prod.getCurrentPrice())

	
if __name__ == "__main__":
	main()
