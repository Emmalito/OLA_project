"""
    Implementation of the fifth step
"""


import sys
sys.path.append("./src")
import numpy.random as npr
from Simulator.Environment import environment
from Learner.learner import UCB1
from Algorithme import optimization


#Global variable for the simulation
nbCustomer = 1000
nbDays = 50


def getConversionRates(simulator, lambdaValue):
    """UCB1 learner for step 5"""
    #Learners for graph probabilities
    learners = [UCB1(simulator.getNbProducts()) for _ in range(2)]

    for _ in range(nbDays):
        #We choose the arm to pull
        pulled_arms = [learner.pull_arm() for learner in learners]

        #We simulate one day
        _, _, _, _ = simulator.runDay(nbCustomer)
        rewards = simulator.getSecondary()

        #We update the distribution
        for index in range(len(learners)):
            reward = rewards[pulled_arms[index]][index]
            learners[index].update(pulled_arms[index], reward.count(0), reward.count(1))

    weights = []
    for learner in learners:
        expected = learner.getExpectedPayoff()
        weights.append([elem for elem in expected])

    #Lambda correction
    weights[1] = [weight * 1/lambdaValue for weight in weights[1]]
 

    return weights


if __name__ == "__main__":
    #0 - We recupere our environment
    simulator, _ = environment()

    #1 - We learn the conversion rates
    lambdaValue = simulator.getGraph(0).getLambda()
    weights = getConversionRates(simulator, lambdaValue)
    print(weights)

    #2 - We fix the others parameters
    #margin = [product.getPrices() for product in products] #We fix the price as the margin
    #alphas = simulator.getUsers()[0].getAlphas()           #We recupere the expected alphas
    #nbItemMax = simulator.getUsers()[0].get_nbItemMax()
    #nbItemSold = [npr.binomial(nbItemMax, 0.7) for _ in range(5)]
    #totalUsers = nbCustomer * nbDays
    #graphWeights = [0.2,0.3,0.2,0.3]

    ##3 - We play the algorithm
    #bestPrices, bestTotalmargin, _ = optimization(margin, conversionRates, alphas,
    #                                            nbItemSold, totalUsers, graphWeights)
    #for idx in range(len(bestPrices)):
    #    print("For the product ", idx, " the best price is ",
    #          margin[idx][bestPrices[idx]])
    #print("The total margin with this configuration is ", bestTotalmargin)
