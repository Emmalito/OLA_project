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

    def update(self, pulled_arm, rewards0, rewards1):
        #updtate his parameters
        self.t+=1
        for _ in range(rewards0):
            self.update_observations(pulled_arm,0)
            self.beta_parameters[pulled_arm,1] = self.beta_parameters[pulled_arm,1]+1 # count the failure
        for _ in range(rewards1):
            self.update_observations(pulled_arm,0)
            self.beta_parameters[pulled_arm,0] = self.beta_parameters[pulled_arm,0]+1 # count how many succes we have

    def getBetaParameters(self):
        return self.beta_parameters


class UCB1(learner):
    def __init__(self, n_arms):
        super().__init__(n_arms)
        self.ucb1_criterion = np.zeros(n_arms)
        self.expected_payoffs = np.zeros(n_arms)
        self.number_of_pulls = np.zeros(n_arms)
        

    def pull_arm(self):
        #Select an arm
        if self.t < self.n_arms:
          pulled_arm = self.t  # round robin for the first n steps 
        else:
          idxs = np.argwhere(self.ucb1_criterion == self.ucb1_criterion.max()).reshape(-1)  # there can be more arms with max value
          pulled_arm = np.random.choice(idxs)
        return pulled_arm
      

    def update(self, pulled_arm, rewards0, rewards1):
        #Update UCB1
        self.t+=1
        for _ in range(rewards0):
            self.number_of_pulls[pulled_arm] +=1
            self.expected_payoffs[pulled_arm] = ((self.expected_payoffs[pulled_arm] * (self.number_of_pulls[pulled_arm] - 1.0) + 0) / 
                                            self.number_of_pulls[pulled_arm]) # update sample mean for the selected arm
        for _ in range(rewards1):
            self.number_of_pulls[pulled_arm] += 1
            self.expected_payoffs[pulled_arm] = ((self.expected_payoffs[pulled_arm] * (self.number_of_pulls[pulled_arm] - 1.0) + 1) / 
                                            self.number_of_pulls[pulled_arm]) # update sample mean for the selected arm
        for k in range(0, self.n_arms):
          self.ucb1_criterion[k] = self.expected_payoffs[k] + np.sqrt(2 * np.log(self.t) / self.number_of_pulls[k])

    def getExpectedPayoff(self):
        return self.expected_payoffs