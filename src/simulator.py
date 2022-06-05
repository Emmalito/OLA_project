"""
Short Def
"""

# This is the file for the simulator. Its intended to be imported into other files for use.
# Vertex and Graph would be private but python does not allow such. They are not intended to be used outside this file.

# Inspired by https://www.bogotobogo.com/python/python_graph_data_structures.php

## Libraries
import numpy as np
from src import *


class Simulator:

	def __init__(self):
		self.g = Graph()

	def generate_beta_graph(self):
		self.g.add_vertex("P1")
		self.g.add_vertex("P2")
		self.g.add_vertex("P3")
		self.g.add_vertex("P4")
		self.g.add_vertex("P5")

	def generate_alphas(self, n):
		# Generate N + 1 number of alphas. One for each and one for the competitors


