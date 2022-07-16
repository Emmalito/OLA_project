"""
    Implementation of the User's class
    which will use the simulator
"""

import numpy as np


class User:
    """User class that defines the user behaviour"""

    def __init__(self, alphas, dayliUsers, price, nbItemMax) -> None:
        self.expectedAlphas = alphas
        self.dayli = dayliUsers
        self.resevationPrice = price
        self.nbItemMax = nbItemMax

    #Methods
    def dayliUsers(self):
        """Return a r.v. of dayli Users"""
        var = int(self.dayli/3)  #Variance of the noise distribution
        visitor = self.dayli + int(np.random.normal(0,var,1)[0]) #We add a gaussian noise
        if visitor < 1:
            return self.dayliUsers()
        return visitor

    def generateAlpha(self, noisyAlphas=[]):
        """Generate the noisy alphas"""
        alpha_ratio = np.random.multinomial(self.dayliUsers(), self.expectedAlphas)
        try:
            noisyAlphas = np.random.dirichlet(alpha_ratio)
        except ValueError:
            self.generateAlpha()
        return noisyAlphas
    
    def buyOrNot(self, price):
        """Return true if the user buy the product, otherwhise False"""
        return price <= self.resevationPrice
    
    def nmbItemToBuy(self):
        """R.v that defines the number of items to buy"""
        return np.random.randint(1,self.nbItemMax) #Can not buy more than 'nbItemMax' items
