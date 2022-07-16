# Test of the Product class

import sys
sys.path.append("./src/Simulator")
from Product import Product


def main():
	#Initialisation
	first_prod = Product(0, [1,0.7, 2,0.3], [7, 11, 13])
	second_prod = Product(1, [0,0.7, 2,0.3], [2, 11, 13])
	third_prod = Product(2, [0,0.7, 1,0.3], [10, 11, 13])

	#Accessor
	print(first_prod.getP1(), first_prod.getP2(),first_prod.getWeight1(),first_prod.getWeight2())
	print("Prices: ", first_prod.getPrices(), " current price: ", first_prod.getCurrentPrice())
	
	#Mutator
	print(first_prod.getCurrentPrice())
	first_prod.nextPrice()
	print(first_prod.getCurrentPrice())

	for i in range(10):
		print("index ", i, " price = ", second_prod.getCurrentPrice())
		second_prod.nextPrice()


	#Methods
	print("Product n° ", third_prod.getId())
	print(third_prod)


if __name__ == "__main__":
	main()
