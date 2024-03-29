from cgi import test
import sys
sys.path.append("./src")
from Simulator.Environment import environment
from Learner.learner import TS_Learner
from Simulator.Environment import environment
import matplotlib.pyplot as plt

import numpy as np



def regret(n_experiment, Time,opt_CV, opt_Alpha,opt_Item):
    # setting for each experiment
    nbCustomer = 1000

    regret_per_experiment_CV = [[] for _ in range(len(opt_CV))]
    regret_per_experiment_Alpha = []
    regret_per_experiment_Item = []

    for exp in range(n_experiment):

        # setting for one experiment
        simulator, prod = environment() #The simulator
        array_CV = [[] for _ in range(len(prod))]
        reward_CV = [[] for _ in range(len(prod))]
        array_Alpha = []
        array_nbItem = []
        nbItemMax = simulator.getUsers()[0].get_nbItemMax()

        #Learners for conversions rates
        learners = [TS_Learner(4) for _ in range(5)]

        #Learner for the alpha ratios
        l_alphas = TS_Learner(6)

        #Learner for the nb Item sold per product
        l_nbItem = TS_Learner(5)

        for _ in range(Time):
            #We choose the arm to pull
            pulled_arm = [learner.pull_arm() for learner in learners]
            pulled_arm_alpha = l_alphas.pull_arm()
            pulled_arm_item = l_nbItem.pull_arm()

            #We change the price in function
            for index in range(len(prod)):
                prod[index].changePrice(pulled_arm[index])

            #We get the corresponding rewards
            cart, rewards1, entrance, nbImpress = simulator.runDay(nbCustomer)
            nbImpress = list(nbImpress.values())
            rewards1 = list(rewards1.values())
            rewards0 = [nbImpress[i] - rewards1[i] for i in range(len(rewards1))]

            #We update the distribution for Conversion Rate
            for index in range(len(learners)):
                learners[index].update(pulled_arm[index], rewards0[index], rewards1[index])
                # and we compute the "regret" for this day
                array_CV[index].append(((rewards0[index]+rewards1[index])*opt_CV[index]-(rewards1[index]))/(rewards0[index]+rewards1[index]))
            #We update the distribution for Alpha ratios
            r0_alpha, r1_alpha = nbCustomer - entrance[pulled_arm_alpha], entrance[pulled_arm_alpha]
            l_alphas.update(pulled_arm_alpha,r0_alpha , r1_alpha)
            # and we compute the "regret" for this day
            array_Alpha.append(((r0_alpha+r1_alpha)*opt_Alpha - r1_alpha)/(r0_alpha+r1_alpha))

            #We update the distribution for nb item sold
            r0_item, r1_item = nbItemMax*rewards1[pulled_arm_item]-cart[pulled_arm_item], cart[pulled_arm_item]
            l_nbItem.update(pulled_arm_item, r0_item, r1_item )
            # and we compute the "regret" for this day
            array_nbItem.append(((r0_item+r1_item)*opt_Item - r1_item)/(r0_item+r1_item)) if ((r0_item+r1_item)!=0) else array_nbItem.append(0)
            

        # we store the result of the experiment
        for i in range(len(learners)):
            regret_per_experiment_CV[i].append(np.array(array_CV[i]))
        regret_per_experiment_Alpha.append(np.array(array_Alpha))
        regret_per_experiment_Item.append(np.array(array_nbItem))

    regret_CV = []
    std_regret_CV = []
    # add np.cumsum in front of each to have the cumulated one
    for i in range(len(prod)):
        regret_CV.append(np.cumsum(np.mean(regret_per_experiment_CV[i], axis=0)))
        std_regret_CV.append(np.cumsum(np.std(regret_per_experiment_CV[i], axis=0)))
    
    regret_Alpha = np.cumsum(np.mean(regret_per_experiment_Alpha,axis=0))
    std_Alpha = np.cumsum(np.std(regret_per_experiment_Alpha,axis=0))

    regret_Item = np.cumsum(np.mean(regret_per_experiment_Item,axis=0))
    std_Item = np.cumsum(np.std(regret_per_experiment_Item,axis=0))

    return regret_CV,std_regret_CV, regret_Alpha, std_Alpha, regret_Item, std_Item



def main():
    # setting of the parameter 
    simulator, prod = environment() #The simulator
    n_experiment = 10
    Time = 10

    # setting for the opt_CVimal reward for each features to learn
    opt_CV = np.array([0.8, 0.6, 0.6, 0.4, 0.6])
    test = [[0.8,0.6,0.2,0],[0.6,0.4,0,0],[0.6,0,0,0],[0.4,0,0,0],[0.6,0.2,0,0]]
    deltas = [opt_CV[i] - np.array(test[i]) for i in range(len(prod))]
    deltas_i = []
    for i in range(len(prod)):
        deltas_i.append(np.array([delta for delta in deltas[i] if delta > 0]))

    opt_alpha, opt_item = 0.2,0.7

    # we compute the corresponding regret, upperbound and std
    regret_CV,std_regret_CV, regret_Alpha, std_Alpha, regret_Item, std_Item = regret(n_experiment, Time, opt_CV, opt_alpha, opt_item)


    # we plot them
    for i in range(len(regret_CV)):
        plt.figure(i)
        plt.xlabel("t")
        plt.ylabel("regrets")
        plt.plot((regret_CV[i]), 'r', label="regret")
        plt.plot((regret_CV[i] + std_regret_CV[i]),linestyle='--', color='g', label="std up")
        plt.plot((regret_CV[i] - std_regret_CV[i]),linestyle='--', color='g', label="std down")
        plt.legend(["TS", "std up","std down"])
    plt.show()
    
    plt.figure(len(regret_CV)+1)
    plt.xlabel("t")
    plt.ylabel("regrets")
    plt.plot((regret_Alpha), 'r', label="regret")
    plt.plot((regret_Alpha + std_Alpha),linestyle='--', color='g', label="std up")
    plt.plot((regret_Alpha - std_Alpha),linestyle='--', color='g', label="std down")
    plt.legend(["TS", "std up","std down"])
    plt.show()

    plt.figure(len(regret_CV)+2)
    plt.xlabel("t")
    plt.ylabel("regrets")
    plt.plot((regret_Item), 'r', label="regret")
    plt.plot((regret_Item + std_Item),linestyle='--', color='g', label="std up")
    plt.plot((regret_Item - std_Item),linestyle='--', color='g', label="std down")
    plt.legend(["TS", "std up","std down"])
    plt.show()



if __name__ == "__main__":
    main()

