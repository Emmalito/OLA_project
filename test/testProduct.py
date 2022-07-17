# Test of the Product class

import sys
import unittest
sys.path.append("./src/Simulator")
from Product import Product



class TestProductMethods(unittest.TestCase):

	def setUp(self):
		self.first_prod = Product(0, [1, 2], [7, 11, 13])
		self.second_prod = Product(1, [0, 2], [2, 11, 13])
		self.third_prod = Product(2, [0, 1], [10, 11, 13])

	def test_accessor(self):
		self.assertEqual(self.first_prod.getP1(), 1)
		self.assertEqual(self.first_prod.getP2(), 2)
		self.assertEqual(self.first_prod.getPrices(), [7, 11, 13])
		self.assertEqual(self.first_prod.getCurrentPrice(), 7)

	def test_mutator(self):
		self.first_prod.nextPrice()
		self.assertEqual(self.first_prod.getCurrentPrice(), 11)

	def test_change_price(self):
		for _ in range(20):
			self.second_prod.nextPrice()
			self.assertTrue(self.second_prod.getCurrentPrice() != None)
	
	def test_id(self):
		self.assertTrue(self. third_prod.getId(), 2)


if __name__ == "__main__":
	unittest.main(verbosity=2)
