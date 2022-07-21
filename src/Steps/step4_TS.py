"""
    Implementation of the fourth step
"""


import sys
sys.path.append("./src")
from Simulator.Environment import environment
from Learner.learner import TS_Learner
from Algorithme import optimization


#Global variable for the simulation
nbCustomer = 1000
nbDays = 20


def getRates(simulator, products, nbItemMax):
    """TS learner for step 4 """
    #Learners for conversions rates
    learners = [TS_Learner(4) for _ in range(5)]

    #Learner for the alpha ratios
    l_alphas = TS_Learner(6)

    #Learner for the nb Item sold per product per price
    l_nbItem = TS_Learner(5)

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
        beta = learner.getBetaParameters()
        convRates.append([beta[elem][0]/(beta[elem][0]+beta[elem][1]) for elem in range(len(beta))])

    beta = l_alphas.getBetaParameters()
    alphas = [alpha[0]/(alpha[0]+alpha[1]) for alpha in beta]

    beta = l_nbItem.getBetaParameters()
    nbItemSold = [item[0]/(item[0]+item[1]) * nbItemMax for item in beta]

    return convRates, alphas, nbItemSold


if __name__ == "__main__":
    #0 - We recupere our environment
    simulator, products = environment()
    nbItemMax = simulator.getUsers()[0].get_nbItemMax()

    #1 - We learn the conversion rates
    conversionRates, alphas, nbItemSold = getRates(simulator, products, nbItemMax)

    #2 - We fix the others parameters
    margin = [product.getPrices() for product in products] #We fix the price as the margin
    totalUsers = nbCustomer * nbDays
    graphWeights = [0.2,0.3,0.2,0.3]

    #3 - We play the algorithm
    bestPrices, bestTotalmargin, _ = optimization(margin, conversionRates, alphas,
                                                nbItemSold, totalUsers, graphWeights)
    for idx in range(len(bestPrices)):
        print("For the product ", idx, " the best price is ",
              margin[idx][bestPrices[idx]])
    print("The total margin with this configuration is ", bestTotalmargin)
