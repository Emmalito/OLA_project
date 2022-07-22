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
    user = User([0.2, 0.1, 0.2, 0.1, 0.2, 0.2], 100, 5, 15)  #1 user that reflects the agregated data

    #We create the 5 products
    prod1 = Product(0, [4, 2], [1, 2, 4, 8])
    prod2 = Product(1, [0, 4], [2, 3, 5, 13])
    prod3 = Product(2, [1, 3], [2, 5, 8, 10])
    prod4 = Product(3, [2, 0], [3, 5, 6, 9])
    prod5 = Product(4, [3, 1], [2, 4, 7, 9])

    #We define the weights
    weights = [[0.7, 0.4], [0.6, 0.2], [0.9, 0.1], [0.6, 0.5], [0.2, 0.1]]

    #We use one common graph for these stpes
    graph = Graph(0.9, [prod1, prod2, prod3, prod4, prod5], weights)

    #The simulator
    simulator = Simulator([graph], [user])

    products = [prod1, prod2, prod3, prod4, prod5]

    return simulator, products


def bigEnvironment():
    """Set up the environment for the step 7"""

    #Create the 3 users'classes
    user1 = User([0.2, 0.1, 0.2, 0.1, 0.2, 0.2], 100, 6, 15)
    user2 = User([0.1, 0.3, 0.3, 0.1, 0.1, 0.1], 150, 12, 20)
    user3 = User([0.4, 0.1, 0.05, 0.25, 0.05, 0.15], 175, 9, 10)

    #We create the 5 products
    prod1 = Product(0, [4, 2], [1, 2, 4, 8])
    prod2 = Product(1, [0, 4], [2, 3, 5, 13])
    prod3 = Product(2, [1, 3], [2, 5, 8, 10])
    prod4 = Product(3, [2, 0], [3, 5, 6, 9])
    prod5 = Product(4, [3, 1], [2, 4, 7, 9])
    products = [prod1, prod2, prod3, prod4, prod5]

    #We define the weights
    weights1 = [[0.7, 0.4], [0.6, 0.2], [0.9, 0.1], [0.6, 0.5], [0.2, 0.1]]
    weights2 = [[0.3, 0.4], [0.2, 0.2], [0.6, 0.4], [0.8, 0.7], [0.6, 0.3]]
    weights3 = [[0.5, 0.5], [0.4, 0.3], [0.2, 0.1], [0.6, 0.5], [0.7, 0.5]]

    #We use one common graph for these stpes
    graph1 = Graph(0.9, products, weights1)
    graph2 = Graph(0.3, products, weights2)
    graph3 = Graph(0.7, products, weights3)


    #The simulator
    simulator1 = Simulator([graph1], [user1])
    simulator2 = Simulator([graph2], [user2])
    simulator3 = Simulator([graph3], [user3])



    return [simulator1, simulator2, simulator3], products 
