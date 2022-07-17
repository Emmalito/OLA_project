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



def main():
    """Simulation of the step3 environment """

    #Create the simulation environment
    # We use only 1 user that reflects the agregated data
    user = User([0.2,0.3,0.2,0.3], 100, 5, 15)
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

    for _ in range(100):
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
        prod4.changePrice(pulled_arm5)
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

    #Let's verify if the function is correct
    #By computing the empirical conversion rates
    conversionRates = {}
    for idx in range(4):
        rew, vis = [0,0,0,0,0], [0,0,0,0,0]
        prod1.changePrice(idx)
        prod2.changePrice(idx)
        prod3.changePrice(idx)
        prod4.changePrice(idx)
        prod5.changePrice(idx)
        for _ in range(5):
            _, rewards, _, visited = simulator.runDay(100)
            rew = [sum(i) for i in zip(rew, list(rewards.values()))]
            vis = [sum(i) for i in zip(vis, list(visited.values()))]
        empirical = []
        for i in range(len(rew)):
            if vis[i] != 0:
                empirical.append(rew[i] / vis[i])
            else:
                empirical.append(0)
        #print("Rates price", idx, " = ", empirical)
        conversionRates[idx] = empirical
    #print(conversionRates)

    betaL1 = l1.getBetaParameters()
    expected = [0.8, 0.6, 0.2, 0]
    print("Conversion rate for product 1")
    for elem in range(len(betaL1)):
        print("TS algorithm = ", betaL1[elem][0]/(betaL1[elem][0]+betaL1[elem][1]), "; Empirical mean = ",
              conversionRates[elem][0], "; Expected mean = ", expected[elem])


if __name__ == "__main__":
    main()
