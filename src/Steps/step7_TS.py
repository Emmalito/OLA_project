"""
    Implementation of the seventh step
"""


import sys
sys.path.append("./src")
from Simulator.Environment import bigEnvironment
from Learner.learner import TS_Learner
from Algorithme import optimization


#Global variable for the simulation
nbCustomer = 1000
nbDays = 20



def getRates(simulators, products, nbItemsMax):
    """TS learner for step 7 """
    #Learners for conversions rates
    allLearners = [[TS_Learner(4) for _ in range(5)] for _ in range(len(simulators))]

    #Learner for the alpha ratios
    allL_alphas = [TS_Learner(6) for  _ in range(len(simulators))]

    #Learner for the nb Item sold per product per price
    allL_nbItem = [TS_Learner(5) for  _ in range(len(simulators))]

    for i in range(len(simulators)):
        learners = allLearners[i]
        l_alphas = allL_alphas[i]
        l_nbItem = allL_nbItem[i]
        simulator = simulators[i]
        nbItemMax = nbItemsMax[i]

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
            if cart[pulled_arm_item] != 0:
                l_nbItem.update(pulled_arm_item, nbItemMax*rewards1[pulled_arm_item]-cart[pulled_arm_item],
                                cart[pulled_arm_item])

    convRates = {}
    index, idx = 0, 0
    for learners in allLearners:
        convRates[index] = [[]]*5
        for learner in learners:
            beta = learner.getBetaParameters()
            convRates[index][idx] = ([beta[elem][0]/(beta[elem][0]+beta[elem][1]) for elem in range(len(beta))])
            idx += 1
        index += 1
        idx = 0

    alphas = []
    for l_alphas in allL_alphas:
        beta = l_alphas.getBetaParameters()
        alphas.append([alpha[0]/(alpha[0]+alpha[1]) for alpha in beta])

    index = 0
    nbItemSold = []
    for l_nbItem in allL_nbItem:
        beta = l_nbItem.getBetaParameters()
        nbItemSold.append([item[0]/(item[0]+item[1]) * nbItemsMax[index] for item in beta])
        index += 1

    return convRates, alphas, nbItemSold


if __name__ == "__main__":
    #0 - We recupere our environment
    simulators, products = bigEnvironment()
    nbItemsMax = [simulator.getUsers()[0].get_nbItemMax() for simulator in simulators] 

    #1 - We learn the conversion rates
    conversionRates, alphas, nbItemSold = getRates(simulators, products, nbItemsMax)

    #2 - We fix the others parameters
    margin = [product.getPrices() for product in products] #We fix the price as the margin
    totalUsers = nbCustomer * nbDays
    graphWeights = [[[0.7, 0.6, 0.9, 0.6, 0.2], [0.4, 0.2, 0.1, 0.5, 0.1]],
                    [[0.3, 0.2, 0.6, 0.8, 0.6], [0.4, 0.2, 0.4, 0.7, 0.3]],
                    [[0.5, 0.4, 0.2, 0.6, 0.7],  [0.5, 0.4, 0.1, 0.5, 0.5]]]

   #3 - We play the algorithm
    for index in range(len(conversionRates)):
        bestPrices, bestTotalmargin, _ = optimization(margin, conversionRates[index], alphas[index],
                                                    nbItemSold[index], totalUsers, graphWeights[index])
        print("For the user class ", index, " we have:")
        for idx in range(len(bestPrices)):
            print("For the product ", idx, " the best price is ",
                margin[idx][bestPrices[idx]])
        print("The total margin with this configuration is ", bestTotalmargin, "\n")
