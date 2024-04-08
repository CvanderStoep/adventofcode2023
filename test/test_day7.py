import os
import unittest

from day7 import compute_part_one, compute_part_two


class Day7Test(unittest.TestCase):
    path = os.path.dirname(os.path.abspath(__file__))

    def test_input_part_one(self):
        self.assertEqual(6440, compute_part_one(self.path + '/input/day7.txt'))

    def test_input_part_two(self):
        self.assertEqual(5905, compute_part_two(self.path + '/input/day7.txt'))


if __name__ == '__main__':
    unittest.main()
