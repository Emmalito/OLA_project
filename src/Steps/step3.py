"""
    Implementation of the third step
"""


import sys
sys.path.append("./src")
from Simulator.User import User
from Simulator.Graph import Graph
from Simulator.Product import Product
from Simulator.Simulator import Simulator
from Learner.learner import TS_Learner
from Algorithme import optimization



def getConversionRates():
    """Simulation of the step3 environment """

    #Create the simulation environment
    # We use only 1 user that reflects the agregated data
    user = User([0.2,0.3,0.2,0.3], 100, 6, 15)
    # We create the products
    prod1 = Product(0, [4, 2], [1, 2, 4, 8])
    prod2 = Product(1, [0, 4], [2, 3, 5, 13])
    prod3 = Product(2, [1, 3], [2, 5, 8, 10])
    prod4 = Product(3, [2, 0], [3, 5, 6, 9])
    prod5 = Product(4, [3, 1], [4, 7, 9, 13])
    weights = [[0.7, 0.4], [0.6, 0.2], [0.9, 0.1], [0.6, 0.5], [0.2, 0.1]]
    # We suppose that it is the agregated graph
    graph = Graph(0.9, [prod1, prod2, prod3, prod4, prod5], weights)

    simulator = Simulator([graph], [user])  #The simulator

    #Learners for 4 conversions rates
    l1 = TS_Learner(4)
    l2 = TS_Learner(4)
    l3 = TS_Learner(4)
    l4 = TS_Learner(4)
    l5 = TS_Learner(4)

    for _ in range(10):
        #We choose the arm to pull
        pulled_arm1 = l1.pull_arm()
        pulled_arm2 = l2.pull_arm()
        pulled_arm3 = l3.pull_arm()
        pulled_arm4 = l4.pull_arm()
        pulled_arm5 = l5.pull_arm()
        #We change the price in function
        prod1.changePrice(pulled_arm1)
        prod2.changePrice(pulled_arm2)
        prod3.changePrice(pulled_arm3)
        prod4.changePrice(pulled_arm4)
        prod5.changePrice(pulled_arm5)
        #We get the corresponding rewards
        _, rewards1, _, nbImpress = simulator.runDay(1000)
        nbImpress = list(nbImpress.values())
        rewards1 = list(rewards1.values())
        rewards0 = [nbImpress[i] - rewards1[i] for i in range(len(rewards1))]
        #We update the distribution
        l1.update(pulled_arm1, rewards0[0], rewards1[0])
        l2.update(pulled_arm2, rewards0[1], rewards1[1])
        l3.update(pulled_arm3, rewards0[2], rewards1[2])
        l4.update(pulled_arm4, rewards0[3], rewards1[3])
        l5.update(pulled_arm5, rewards0[4], rewards1[4])

    convRates = []
    learners = [l1, l2, l3, l4, l5]
    for learn in learners:
        beta = learn.getBetaParameters()
        convRates.append([beta[elem][0]/(beta[elem][0]+beta[elem][1]) for elem in range(len(beta))])

    return convRates


if __name__ == "__main__":
    #1 - We learn the conversion rates
    conversionRates = getConversionRates()

    #2 - We fix the others parameters
    margin = [[1, 2, 4, 8], [2, 3, 5, 13],
              [2, 5, 8, 10], [3, 5, 6, 9], [4, 7, 9, 13]]
    alphas = [0.2,0.3,0.2,0.3]
    nbItemSold = [50, 42, 33, 77, 58]
    nbUsers = 15
    graphWeights = [0.2,0.3,0.2,0.3]

    #3 - We play the algorithm
    bestPrices, bestTotalmargin, _ = optimization(margin, conversionRates, alphas, nbItemSold, nbUsers, graphWeights)
    for idx in range(len(bestPrices)):
        print("For the product ", idx, " the best price is ", margin[idx][bestPrices[idx]])
    print("The total margin with this configuration is ", bestTotalmargin)
