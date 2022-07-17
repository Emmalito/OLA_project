"""
    File that generate the simulation of the environment
    thanks to a simulator object
"""

from User import User
from Graph import Graph
from Product import Product
from Simulator import Simulator
from test import TS_Learner



def main():
    """Simulation of a environment"""
    user1 = User([0.2,0.3,0.2,0.3], 100, 5, 15)
    #user2 = User([0.4,0.1,0.3,0.2], 200, 2, 23)
    #user3 = User([0.1,0.1,0.3,0.5], 60, 4, 8)

    prod1 = Product(0, [1, 2], [1, 4, 7, 10])
    prod2 = Product(1, [0, 2], [3, 3, 7, 13])
    prod3 = Product(2, [0, 1], [2, 5, 8, 10])

    weights1 = [[0.7, 0.4], [0.6, 0.2], [0.9, 0.1]]
    #weights2 = [[0.9, 0.1], [0.8, 0.5], [0.6, 0.2]]
    #weights3 = [[0.6, 0.2], [0.7, 0.4], [0.7, 0.5]]

    graph1 = Graph(0.9, [prod1, prod2, prod3], weights1)
    #graph2 = Graph(0.2, [prod1, prod2, prod3], weights2)
    #graph3 = Graph(0.5, [prod1, prod2, prod3], weights3)

    #simulator = Simulator([graph1, graph2, graph3], [user1, user2, user3])
    simulator = Simulator([graph1], [user1])

    l1 = TS_Learner(4)  #4 = Number of prices
    #l2 = TS_Learner(4)
    #l3 = TS_Learner(4)

    # Accessor
    print(simulator.getGraph(0))

    #for _ in range(100):
    #    cart, re, rewards, visited = simulator.runDay(100)

    cart, re, rewards, visited = simulator.runDay(1000)
    print("Cart : ", cart)
    print("Nb visitor = ", visited)
    print("Rewards: ", re)
    print("Rewards bernouilli: ", rewards)

    rew, vis = [0,0,0], [0,0,0]
    for _ in range(100):
        cart, rewards, re, visited = simulator.runDay(1000)
        rew = [sum(i) for i in zip(rew, list(rewards.values()))]
        vis = [sum(i) for i in zip(vis, list(visited.values()))]
    print("Rates = ", [rew[i] / vis[i] for i in range(len(rew))])


    print(prod1.getCurrentPrice())
    """print(prod2.getCurrentPrice())
    print(prod3.getCurrentPrice())

    for _ in range(100):
        pulled_arm1 = l1.pull_arm()
        pulled_arm2 = l2.pull_arm()
        pulled_arm3 = l3.pull_arm()

        prod1.changePrice(pulled_arm1)
        prod2.changePrice(pulled_arm2)
        prod3.changePrice(pulled_arm3)

        cart, re, rewards = simulator.runDay(1000)
        #print("Cart : ", cart)
        #print("Rewards: ", re)
        #print("Rewards bernouilli: ", rewards)

        l1.update(pulled_arm1, rewards[0])
        l2.update(pulled_arm2, rewards[1])
        l3.update(pulled_arm3, rewards[2])
    
    print(prod1.getCurrentPrice())
    print(prod2.getCurrentPrice())
    print(prod3.getCurrentPrice())"""

    #cart, re, rewards = simulator.runDay(1000000)
    #print(re)


if __name__ == "__main__":
    main()