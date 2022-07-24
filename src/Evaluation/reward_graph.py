from cgi import test
import sys
sys.path.append("./src")
from Simulator.Environment import environment
from Learner.learner import TS_Learner, UCB1
from Simulator.Environment import environment
import matplotlib.pyplot as plt

import numpy as np



def regret(n_experiment, Time,opt):
    # setting for each experiment
    nbCustomer = 1000

    reward_per_experiment_ts = [[] for _ in range(2)]
    reward_per_experiment_ucb = [[] for _ in range(2)]

    for exp in range(n_experiment):

        # setting for one experiment
        simulator, prod = environment() #The simulator
        array_ts =  [[] for _ in range(2)]
        array_ucb = [[] for _ in range(2)]

        #Learners for graph probabilities
        learners_TS = [TS_Learner(simulator.getNbProducts()) for _ in range(2)]
        learners_UCB1 = [UCB1(simulator.getNbProducts()) for _ in range(2)]

        for _ in range(Time):
            #We choose the arm to pull
            pulled_arms_ts = [learner.pull_arm() for learner in learners_TS]
            pulled_arms_ucb = [learner.pull_arm() for learner in learners_UCB1]
            #We simulate one day
            _, _, _, _ = simulator.runDay(nbCustomer)
            rewards = simulator.getSecondary()

            #We update the distribution
            for index in range(len(learners_TS)):
                reward_ts = rewards[pulled_arms_ts[index]][index]
                learners_TS[index].update(pulled_arms_ts[index], reward_ts.count(0), reward_ts.count(1))
                array_ts[index].append(reward_ts.count(1) /(reward_ts.count(0) +reward_ts.count(1)))

                reward_ucb = rewards[pulled_arms_ucb[index]][index]
                learners_UCB1[index].update(pulled_arms_ucb[index], reward_ucb.count(0), reward_ucb.count(1))
                array_ucb[index].append(reward_ucb.count(1)/(reward_ucb.count(0) +reward_ucb.count(1)))

        # we store the result of the experiment
        for i in range(len(learners_TS)):
            reward_per_experiment_ts[i].append(np.array(array_ts[i]))
            reward_per_experiment_ucb[i].append(np.array(array_ucb[i]))

        reward_ts,std_reward_ts =   [],[]
        reward_ucb,std_reward_ucb = [],[]
        # add  np.cumsum in front of each to have cummulated one
        for i in range(len(learners_TS)):
            reward_ts.append((np.mean(reward_per_experiment_ts[i], axis=0)))
            std_reward_ts.append((np.std(reward_per_experiment_ts[i], axis=0)))
            reward_ucb.append((np.mean(reward_per_experiment_ucb[i], axis=0)))
            std_reward_ucb.append((np.std(reward_per_experiment_ucb[i], axis=0)))
 
    return reward_ts,std_reward_ts, reward_ucb,std_reward_ucb 



def main():
    # setting of the parameter 
    simulator, prod = environment() #The simulator
    n_experiment = 10
    Time = 20

    # setting for the opt_CVimal reward for each features to learn
    opt = np.array([0.9, 0.5])
    test = [[0.7,0.6,0.9,0.6,0.2],[0.4,0.2,0.1,0.5,0.1]]
    deltas = [opt[i] - np.array(test[i]) for i in range(len(opt))]
    deltas_i = []
    for i in range(len(opt)):
        deltas_i.append(np.array([delta for delta in deltas[i] if delta > 0]))


    # we compute the corresponding regret, upperbound and std
    reward_ts,std_reward_ts, reward_ucb,std_reward_ucb = regret(n_experiment, Time, opt)


    # we plot them
    for i in range(len(reward_ts)):
        plt.figure(i)
        plt.xlabel("t")
        plt.ylabel("expected reward")
        plt.plot((reward_ts[i]), 'r', label="expected reward")
        plt.plot(np.linspace(0,Time, Time),[opt[i] for _ in range(Time)], 'black')
        plt.plot((reward_ts[i] + std_reward_ts[i]),linestyle='--', color='orange', label="std up")
        plt.plot((reward_ts[i] - std_reward_ts[i]),linestyle='--', color='orange', label="std down")
        plt.plot((reward_ucb[i]), 'cyan', label="regret")
        plt.plot((reward_ucb[i] + std_reward_ucb[i]),linestyle='--', color='b', label="std up")
        plt.plot((reward_ucb[i] - std_reward_ucb[i]),linestyle='--', color='b', label="std down")
        plt.legend(["TS", "best", "std up","std down", 'UCB1',"std up","std down"])
    plt.show()




if __name__ == "__main__":
    main()

