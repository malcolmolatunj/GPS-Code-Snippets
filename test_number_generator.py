import unittest

from number_generator import NumberGenerator


class TestNumberGenerator(unittest.TestCase):
    def setUp(self):
        self.basic_NG = NumberGenerator(letters="AB", digits="012", length=3)

    def test_max_combinations(self):
        self.assertEqual(self.basic_NG.max_combinations, 38)

    def test_index_error(self):
        with self.assertRaises(IndexError):
            self.basic_NG.format(-1)

        with self.assertRaises(IndexError):
            self.basic_NG.format(38)

        with self.assertRaises(IndexError):
            self.basic_NG.format(39)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            self.basic_NG.format(0.5)

        with self.assertRaises(TypeError):
            self.basic_NG.format([])

        with self.assertRaises(TypeError):
            self.basic_NG.format({})

        with self.assertRaises(TypeError):
            self.basic_NG.format(1 + 5j)

        with self.assertRaises(TypeError):
            self.basic_NG.format("one")

    def test_endpoints(self):
        self.assertEqual(self.basic_NG.format(0), "A00")
        self.assertEqual(self.basic_NG.format(17), "B22")
        self.assertEqual(self.basic_NG.format(18), "AA0")
        self.assertEqual(self.basic_NG.format(29), "BB2")
        self.assertEqual(self.basic_NG.format(30), "AAA")
        self.assertEqual(self.basic_NG.format(37), "BBB")

    def test_between_endpoints(self):
        self.assertEqual(self.basic_NG.format(1), "A01")
        self.assertEqual(self.basic_NG.format(16), "B21")
        self.assertEqual(self.basic_NG.format(9), "B00")
        self.assertEqual(self.basic_NG.format(21), "AB0")
        self.assertEqual(self.basic_NG.format(24), "BA0")
        self.assertEqual(self.basic_NG.format(33), "ABB")


if __name__ == "__main__":
    unittest.main()
