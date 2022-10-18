import unittest
from substitutes import User, is_valid_sub


class TestValidSubs(unittest.TestCase):
    def setUp(self):
        self.christa = User()
        self.parker = User()
        self.malcolm = User()

    def test_inactivesub(self):
        self.parker.active = False
        self.assertFalse(is_valid_sub(self.christa, self.parker))

    def test_noSub(self):
        self.assertTrue(is_valid_sub(self.christa, self.parker))

    def test_circularReference(self):
        self.parker.sub = self.christa
        self.assertFalse(is_valid_sub(self.christa, self.parker))

        self.malcolm.sub = self.parker
        self.assertFalse(is_valid_sub(self.christa, self.malcolm))

        self.kenery = User(sub=self.malcolm)
        self.assertFalse(is_valid_sub(self.christa, self.kenery))

    def test_activeChain(self):
        self.parker.sub = self.malcolm
        self.assertTrue(is_valid_sub(self.christa, self.parker))

    def test_inactiveInChain(self):
        self.malcolm.sub = self.parker
        self.parker.active = False
        self.assertFalse(is_valid_sub(self.christa, self.malcolm))


if __name__ == "__main__":
    unittest.main()
