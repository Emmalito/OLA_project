"""
    Implementation of the fourth step
"""


import sys
sys.path.append("./src")
from Simulator.Environment import environment
from Learner.learner import UCB1
from Algorithme import optimization



def getRates(simulator, products, nbItemMax):
    """Simulation of the step3 environment """
    #We fix the some parameters for the simulation
    nbCustomer = 1000
    nbDays = 50

    #Learners for conversions rates
    learners = [UCB1(4) for _ in range(5)]

    #Learner for the alpha ratios
    l_alphas = UCB1(6)

    #Learner for the nb Item sold per product per price
    l_nbItem = UCB1(5)

    for _ in range(nbDays):
        #We choose the arm to pull
        pulled_arm = [learner.pull_arm() for learner in learners]
        pulled_arm_alpha = l_alphas.pull_arm()
        pulled_arm_item = l_nbItem.pull_arm()

        #We change the price in function
        for index in range(len(products)):
            products[index].changePrice(pulled_arm[index])

        #We get the corresponding rewards
        cart, rewards1, entrance, nbImpress = simulator.runDay(nbCustomer)
        nbImpress = list(nbImpress.values())
        rewards1 = list(rewards1.values())
        rewards0 = [nbImpress[i] - rewards1[i] for i in range(len(rewards1))]

        #We update the distribution
        for index in range(len(learners)):
            learners[index].update(pulled_arm[index], rewards0[index], rewards1[index])
        l_alphas.update(pulled_arm_alpha, nbCustomer - entrance[pulled_arm_alpha], entrance[pulled_arm_alpha])
        l_nbItem.update(pulled_arm_item, nbItemMax*rewards1[pulled_arm_item]-cart[pulled_arm_item],
                        cart[pulled_arm_item])

    convRates = []
    for learner in learners:
        expected = learner.getExpectedPayoff()
        convRates.append([elem for elem in expected])

    expected = l_alphas.getExpectedPayoff()
    alphas = [elem for elem in expected]

    expected = l_nbItem.getExpectedPayoff()
    nbItemSold = [elem * nbItemMax for elem in expected]

    return convRates, alphas, nbItemSold


if __name__ == "__main__":
    #0 - We recupere our environment
    simulator, products, nbItemMax = environment()

    #1 - We learn the conversion rates
    conversionRates, alphas, nbItemSold = getRates(simulator, products, nbItemMax)

    #2 - We fix the others parameters
    margin = [[1, 2, 4, 8], [2, 3, 5, 13],
              [2, 5, 8, 10], [3, 5, 6, 9], [4, 7, 9, 13]]
    nbUsers = 150
    graphWeights = [0.2,0.3,0.2,0.3]

    #3 - We play the algorithm
    bestPrices, bestTotalmargin, _ = optimization(margin, conversionRates, alphas, nbItemSold, nbUsers, graphWeights)
    for idx in range(len(bestPrices)):
        print("For the product ", idx, " the best price is ", margin[idx][bestPrices[idx]])
    print("The total margin with this configuration is ", bestTotalmargin)
