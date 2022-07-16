"""
    File that generate the simulation of the environment
    thanks to a simulator object
"""

from User import User
from Graph import Graph
from Product import Product
from Simulator import Simulator



def main():
    """Simulation of a environment"""
    user1 = User([0.2,0.3,0.2,0.3], 100, 5, 15)
    user2 = User([0.4,0.1,0.3,0.2], 200, 12, 23)
    user3 = User([0.1,0.1,0.3,0.5], 60, 9, 8)

    prod1 = Product(0, [1,0.7, 2,0.3], [7, 11, 13])
    prod2 = Product(1, [0,0.7, 2,0.3], [2, 11, 13])
    prod3 = Product(2, [0,0.7, 1,0.3], [10, 11, 13])

    graph1 = Graph(0.9, [prod1, prod2, prod3])
    graph2 = Graph(0.2, [prod2, prod1, prod3])
    graph3 = Graph(0.5, [prod1, prod3, prod2])

    simulator = Simulator([graph1, graph2, graph3], [user1, user2, user3])

    # Accessor
    print(simulator.getGraph(1))

    cart = simulator.runDay()
    print(cart)

if __name__ == "__main__":
    for _ in range(100000):
        main()
        print("\n")



# you need to resort to social influence techniques 
# to evaluate the probabilities with which the user 
# reaches the webpage with some specific primary product.

#    infos, mus, alphas, nbGraphs