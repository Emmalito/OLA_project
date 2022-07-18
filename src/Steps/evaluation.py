"""
    sdds
"""

import numpy as np

def getRegrets(rewards):
    """Return the regrets of a given set of rewards"""

    regrets = np.array([])
    reward_opt = 5
    regrets = np.append(regrets, reward_opt - rewards)
    return regrets

