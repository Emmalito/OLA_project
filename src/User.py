"""
    Implementation of the User's class
    which will use the simulator
"""

import numpy as np


class User:
    """"""

    def __init__(self, alphas, dailyUsers, index) -> None:
        self.expectedAlphas = alphas
        self.dailyUsers = dailyUsers
        self.index = index

    #Methods
    def generateAlpha(self):
        """Generate the noisy alphas"""
        noisyAlphas = []
        alpha_ratio = np.random.multinomial(self.dailyUsers, self.expectedAlphas)
        noisyAlphas = np.random.dirichlet(alpha_ratio)
        return noisyAlphas
    
    def buyOrNot(price):
        """Return true if the user buy the product, otherwhise False"""
