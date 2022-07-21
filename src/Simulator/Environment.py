"""
    File that generate the simulation of the environment
    thanks to a simulator object
"""

from Simulator.User import User
from Simulator.Graph import Graph
from Simulator.Product import Product
from Simulator.Simulator import Simulator



def environment():
    """Set up the environment for the steps"""

    #Create the simulation environment for the steps 3-4-5
    user = User([0.2, 0.1, 0.2, 0.1, 0.2, 0.2], 100, 6, 15)  #1 user that reflects the agregated data

    #We create the 5 products
    prod1 = Product(0, [4, 2], [1, 2, 4, 8])
    prod2 = Product(1, [0, 4], [2, 3, 5, 13])
    prod3 = Product(2, [1, 3], [2, 5, 8, 10])
    prod4 = Product(3, [2, 0], [3, 5, 6, 9])
    prod5 = Product(4, [3, 1], [4, 7, 9, 13])

    #We define the weights
    weights = [[0.7, 0.4], [0.6, 0.2], [0.9, 0.1], [0.6, 0.5], [0.2, 0.1]]

    #We use one common graph for these stpes
    graph = Graph(0.9, [prod1, prod2, prod3, prod4, prod5], weights)

    #The simulator
    simulator = Simulator([graph], [user])

    products = [prod1, prod2, prod3, prod4, prod5]

    return simulator, products, user.get_nbItemMax()
