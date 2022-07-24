# Tests Class Graph

import sys
import unittest
sys.path.append("./src/Simulator")
from Product import Product
from Graph import Graph



class TestGraphMethods(unittest.TestCase):

	def setUp(self) -> None:
		self.prod1 = Product(0, [1, 2], [7, 11, 13])
		self.prod2 = Product(1, [0, 2], [2, 11, 13])
		self.prod3 = Product(2, [0, 1], [10, 11, 13])

		self.weights1 = [[0.7, 0.4], [0.6, 0.2], [0.9, 0.1]]
		self.weights2 = [[0.9, 0.1], [0.8, 0.5], [0.6, 0.2]]
		self.weights3 = [[0.6, 0.2], [0.7, 0.4], [0.7, 0.5]]

		self.graph1 = Graph(0.5, [self.prod1, self.prod2, self.prod3], self.weights1)
		self.graph2 = Graph(0.2, [self.prod1, self.prod2, self.prod3], self.weights2)
		self.graph3 = Graph(1, [self.prod1, self.prod2, self.prod3], self.weights3)
		return super().setUp()
	
	def test_accessor(self):
		self.assertEqual(self.graph1.getNbProduct(), 3)
		self.assertEqual(self.graph1.getProduct(0), self.prod1)
		self.assertEqual(self.graph1.getProduct(1), self.prod2)
		self.assertEqual(self.graph1.getProduct(2), self.prod3)

	def test_methods(self):
		self.graph2.prodVisited(0)
		self.graph2.prodVisited(1)

		self.assertTrue(self.graph2.alreadyVisited(0))
		self.assertTrue(self.graph2.alreadyVisited(1))
		self.assertFalse(self.graph2.alreadyVisited(2))

		self.graph2.restoreVisited()
		self.assertFalse(self.graph2.alreadyVisited(0))

	def test_prodVisited(self):
		with self.assertRaises(IndexError):
			self.graph3.prodVisited(4)
		with self.assertRaises(IndexError):
			self.graph3.prodVisited(-2)


if __name__ == "__main__":
	unittest.main(verbosity=2)
