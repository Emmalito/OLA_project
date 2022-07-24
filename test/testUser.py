# Test the User class

import sys
import unittest
sys.path.append("./src/Simulator")
from User import User


class TestUserMethods(unittest.TestCase):

    def setUp(self):
        self.user1 = User([0.2,0.3,0.2,0.3], 100, 5, 15)
        self.user2 = User([0.4,0.1,0.3,0.2], 200, 12, 23)
        self.user3 = User([0.1,0.1,0.3,0.5], 6, 9, 8)

    def test_dayli(self):
        for _ in range(100):
            self.assertTrue(self.user3.dayliUsers() > 1)

    def test_alpha(self):
        for _ in range(100):
            tmp = self.user2.generateAlpha()
            self.assertTrue(tmp != [])

    def test_buy(self):
        self.assertTrue(0 < self.user3.buyOrNot(3) <= 1)
        self.assertEqual(self.user3.buyOrNot(9), 0)
        self.assertEqual(self.user3.buyOrNot(11), 0)

    def test_item(self):
        tmp = []
        for _ in range(1000):
            tmp.append(self.user2.nmbItemToBuy())
            self.assertNotEqual(tmp[-1], 0)
        self.assertTrue(round(sum(tmp)/len(tmp)) - 200 < 30)


if __name__ == "__main__":
    unittest.main(verbosity=2)
