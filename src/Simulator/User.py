"""
    Implementation of the User's class
    which will use the simulator
"""

import numpy.random as npr


class User:
    """User class that defines the user behaviour"""

    def __init__(self, alphas, dayliUsers, price, nbItemMax) -> None:
        self.expectedAlphas = alphas
        self.dayli = dayliUsers
        self.resevationPrice = price
        self.nbItemMax = nbItemMax
    
    #Accessor
    def get_nbItemMax(self):
        return self.nbItemMax


    #Methods
    def dayliUsers(self):
        """Return a r.v. of dayli Users"""
        var = int(self.dayli/5)  #Variance of the noise distribution
        visitor = self.dayli + int(npr.normal(0,var,1)[0]) #We add a gaussian noise
        if visitor < 1:
            return self.dayliUsers()
        else:
            return visitor

    def generateAlpha(self, noisyAlphas=[]):
        """Generate the noisy alphas"""
        alpha_ratio = npr.multinomial(self.dayliUsers(), self.expectedAlphas)
        try:
            noisyAlphas = npr.dirichlet(alpha_ratio)
        except ValueError:
            self.generateAlpha()
        if noisyAlphas == []:
            return self.generateAlpha()
        else:
            return noisyAlphas
    
    def buyOrNot(self, price):
        """Return true if the user buy the product, otherwhise False"""
        proba = 1 - min(1, price/self.resevationPrice)
        return npr.binomial(1,proba)
    
    def nmbItemToBuy(self):
        """Uniform r.v that defines the number of items to buy"""
        proba = 0.7   # We assume to fix this probability
        nbItem = npr.binomial(self.nbItemMax, proba)   #Can not buy more than 'nbItemMax' items
        if nbItem > 0:
            return nbItem
        else:
            return self.nmbItemToBuy()  
