"""
    Implementation of the third step
"""


import sys
sys.path.append("./src")
from Simulator.Environment import environment
from Learner.learner import UCB1
from Algorithme import optimization



def getConversionRates(simulator, products):
    """UCB1 learner for step 3 """
    #We fix the dayli number of customers and the number of day simulation
    nbCustomer = 1000
    nbDays = 20

    #Learners for 4 conversions rates
    learners = [UCB1(4) for _ in range(5)]

    for _ in range(nbDays):
        #We choose the arm to pull
        pulled_arm = [learner.pull_arm() for learner in learners]

        #We change the price in function
        for index in range(len(products)):
            products[index].changePrice(pulled_arm[index])

        #We get the corresponding rewards
        _, rewards1, _, nbImpress = simulator.runDay(nbCustomer)
        nbImpress = list(nbImpress.values())
        rewards1 = list(rewards1.values())
        rewards0 = [nbImpress[i] - rewards1[i] for i in range(len(rewards1))]

        #We update the distribution
        for index in range(len(learners)):
            learners[index].update(pulled_arm[index], rewards0[index], rewards1[index])

    convRates = []
    for learner in learners:
        expected = learner.getExpectedPayoff()
        convRates.append([elem for elem in expected])

    return convRates


if __name__ == "__main__":
    #0 - We recupere our environment
    simulator, products, _ = environment()

    #1 - We learn the conversion rates
    conversionRates = getConversionRates(simulator, products)

    #2 - We fix the others parameters
    margin = [[1, 2, 4, 8], [2, 3, 5, 13],
              [2, 5, 8, 10], [3, 5, 6, 9], [4, 7, 9, 13]]
    alphas = [0.2,0.3,0.2,0.3]
    nbItemSold = [10, 10, 10, 10, 10]
    nbUsers = 15
    graphWeights = [0.2,0.3,0.2,0.3]

    #3 - We play the algorithm
    bestPrices, bestTotalmargin, _ = optimization(margin, conversionRates, alphas, nbItemSold, nbUsers, graphWeights)
    for idx in range(len(bestPrices)):
        print("For the product ", idx, " the best price is ", margin[idx][bestPrices[idx]])
    print("The total margin with this configuration is ", bestTotalmargin)
