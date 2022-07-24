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

    rewards_per_experiment_CV = [[] for _ in range(len(opt_CV))]
    rewards_per_experiment_Alpha = []
    rewards_per_experiment_Item = []

    for exp in range(n_experiment):

        # setting for one experiment
        simulator, prod = environment() #The simulator
        array_CV = [[] for _ in range(len(prod))]
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
                array_CV[index].append(rewards1[index]/(rewards1[index]+rewards0[index])) # to plot the reward
            #We update the distribution for Alpha ratios
            r0_alpha, r1_alpha = nbCustomer - entrance[pulled_arm_alpha], entrance[pulled_arm_alpha]
            l_alphas.update(pulled_arm_alpha,r0_alpha , r1_alpha)
            # and we compute the "regret" for this day
            array_Alpha.append(r1_alpha/((r0_alpha+r1_alpha)))

            #We update the distribution for nb item sold
            r0_item, r1_item = nbItemMax*rewards1[pulled_arm_item]-cart[pulled_arm_item], cart[pulled_arm_item]
            l_nbItem.update(pulled_arm_item, r0_item, r1_item )
            # and we compute the "regret" for this day
            array_nbItem.append(r1_item/((r0_item+r1_item))) if ((r0_item+r1_item)!=0) else array_nbItem.append(0)
            

        # we store the result of the experiment
        for i in range(len(learners)):
            rewards_per_experiment_CV[i].append(np.array(array_CV[i]))
        rewards_per_experiment_Alpha.append(np.array(array_Alpha))
        rewards_per_experiment_Item.append(np.array(array_nbItem))

    reward_CV = []
    std_reward_CV = []
    # add  np.cumsum in front of each to have cummulated one
    for i in range(len(prod)):
        reward_CV.append((np.mean(rewards_per_experiment_CV[i], axis=0)))
        std_reward_CV.append((np.std(rewards_per_experiment_CV[i], axis=0)))
    
    reward_Alpha = (np.mean(rewards_per_experiment_Alpha,axis=0))
    std_Alpha = (np.std(rewards_per_experiment_Alpha,axis=0))

    reward_Item = (np.mean(rewards_per_experiment_Item,axis=0))
    std_Item = (np.std(rewards_per_experiment_Item,axis=0))

    return reward_CV,std_reward_CV, reward_Alpha, std_Alpha, reward_Item, std_Item



def main():
    # setting of the parameter 
    simulator, prod = environment() #The simulator
    n_experiment = 10
    Time = 10

    # setting for the opt_CVimal reward for each features to learn
    opt_CV = np.array([0.8, 0.6, 0.6, 0.4, 0.6])
    opt_alpha, opt_item = 0.2,0.7
    test = [[0.8,0.6,0.2,0],[0.6,0.4,0,0],[0.6,0,0,0],[0.4,0,0,0],[0.6,0.2,0,0]]
    deltas = [opt_CV[i] - np.array(test[i]) for i in range(len(prod))]
    deltas_i = []
    for i in range(len(prod)):
        deltas_i.append(np.array([delta for delta in deltas[i] if delta > 0]))

    # we compute the corresponding regret, upperbound and std
    reward_CV,std_reward_CV, reward_Alpha, std_Alpha, reward_Item, std_Item = regret(n_experiment, Time, opt_CV,opt_alpha, opt_item )
    TS_Learner_upper_bound_CV = []
    for i in range(len(prod)):
        TS_Learner_upper_bound_CV.append(np.array([10*8*np.log(t)*sum(1/deltas_i[i]) + (1 + np.pi**2/3)*sum(deltas_i[i])
                             for t in range(1,Time+1)]))

    # we plot them
    for i in range(len(reward_CV)):
        plt.figure(i)
        plt.xlabel("t")
        plt.ylabel("expected reward")
        plt.plot((reward_CV[i]), 'r', label="expected reward")
        plt.plot(np.linspace(0,Time, Time),[opt_CV[i] for _ in range(Time)], 'b')
        plt.plot((reward_CV[i] + 1.96 *std_reward_CV[i]/ np.sqrt(n_experiment)),linestyle='--', color='g', label="std up")
        plt.plot((reward_CV[i] - 1.96 *std_reward_CV[i]/ np.sqrt(n_experiment)),linestyle='--', color='g', label="std down")
        #plt.plot(TS_Learner_upper_bound_CV[i], color='b', label='Upper bound')
        plt.legend(["TS", "best","std up","std down"])
    plt.show()
    
    plt.figure(len(reward_CV)+1)
    plt.xlabel("t")
    plt.ylabel("expected reward")
    plt.plot((reward_Alpha), 'r', label="expected reward")
    plt.plot(np.linspace(0,Time, Time),[opt_alpha for _ in range(Time)], 'b')
    plt.plot((reward_Alpha + 1.96 *std_Alpha/ np.sqrt(n_experiment)),linestyle='--', color='g', label="std up")
    plt.plot((reward_Alpha - 1.96 *std_Alpha/ np.sqrt(n_experiment)),linestyle='--', color='g', label="std down")
    #plt.plot(TS_Learner_upper_bound[i], color='b', label='Upper bound')
    plt.legend(["TS", "best","std up","std down"])
    plt.show()

    plt.figure(len(reward_CV)+2)
    plt.xlabel("t")
    plt.ylabel("expected reward")
    plt.plot((reward_Item), 'r', label="expected reward")
    plt.plot(np.linspace(0,Time, Time),[opt_item for _ in range(Time)], 'b')
    plt.plot((reward_Item + 1.96 *std_Item/ np.sqrt(n_experiment)),linestyle='--', color='g', label="std up")
    plt.plot((reward_Item - 1.96 *std_Item/ np.sqrt(n_experiment)),linestyle='--', color='g', label="std down")
    #plt.plot(TS_Learner_upper_bound[i], color='b', label='Upper bound')
    plt.legend(["TS", "best","std up","std down"])
    plt.show()



if __name__ == "__main__":
    main()

