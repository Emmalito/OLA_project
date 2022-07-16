# Test the User class

import sys

from matplotlib import use
sys.path.append("./src/Simulator")
from User import User


def main():
    """Simulation of a environment"""
    user1 = User([0.2,0.3,0.2,0.3], 100, 5, 15)
    user2 = User([0.4,0.1,0.3,0.2], 200, 12, 23)
    user3 = User([0.1,0.1,0.3,0.5], 60, 9, 8)

    for _ in range(10):
        print(user1.dayliUsers(), sep=" ; ")
    
    for _ in range(10):
        print(user2.generateAlpha(), sep=" ; ")

    print("True = ", user3.buyOrNot(3))
    print("True = ", user3.buyOrNot(9))
    print("False = ", user3.buyOrNot(11))

if __name__ == "__main__":
	main()
