import numpy as np


class learner:
    #interact with environement by selecting the arm to pull
    # and observe reward given by the environement
    def __init__(self, n_arms):
        # defined by nb arms, current round and the collected rewards
        self.n_arms = n_arms
        self.t=0
        self.reward_per_arm = x = [[] for _ in range(n_arms)]
        self.collected_rewards = np.array([])

    def update_observations(self, pulled_arm, reward):
        self.reward_per_arm[pulled_arm].append(reward)
        self.collected_rewards = np.append(self.collected_rewards, reward)


class TS_Learner(learner):
    def __init__(self, n_arms):
        super().__init__(n_arms)
        # store beta distribution
        self.beta_parameters = np.ones((n_arms,2))

    def pull_arm(self):
        #select the best arm
        idx = np.argmax(np.random.beta(self.beta_parameters[:,0],self.beta_parameters[:,1]))
        return idx

    def update(self, pulled_arm, reward):
        #updtate his parameters
        self.t+=1
        self.update_observations(pulled_arm,reward)
        self.beta_parameters[pulled_arm,0] = self.beta_parameters[pulled_arm,0]+reward # count how many succes we have
        self.beta_parameters[pulled_arm,1] = self.beta_parameters[pulled_arm,1]+1-reward # count the opposit