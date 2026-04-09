import unittest
from main import *

class TestVectorMath(unittest.TestCase):

    def test_add(self):
        self.assertEqual(add((-1, 2), (-3, 0)), (-4, 2), "Should be <-4, 2>")

    def test_subtract(self):
        self.assertEqual(subtract((-1, 2), (-3, 0)), (2, 2), "Should be <2, 2>")

    def test_dot(self):
        self.assertEqual(dot((-1, 2), (-3, 0)), 3, "Should be 3")

    def test_scale(self):
        self.assertEqual(scaleBy((-1, 2), -5), (5, -10), "Should be <5, -10>")

    def test_magnitude(self):
        self.assertEqual(magnitude((-1, 2)), sqrt(5), "Should be the square root of 5")

    def test_porjection1(self):
        self.assertEqual(projectOnto((-2, 2), (3, 0)), (-2, 0), "Should be <-2, 0>")
    def test_porjection2(self):
        self.assertEqual(projectOnto((4, 3), (2, 8)), (16/17, 64/17), "Should be <16/17, 64/17>")

    def test_vecPointMag(self):
        self.assertEqual(magnitude(normalPoint((-2, 2), (3, 0))), 1, "Should be 1")
        self.assertEqual(magnitude(normalPoint((20, 0), (15, -2))), 1, "Should be 1")
    def test_vecPointFull(self):
        self.assertAlmostEqual(normalPoint((0,0), (-3, 4))[0], ((-3/5), 4/5)[0])
        self.assertAlmostEqual(normalPoint((0,0), (-3, 4))[1], ((-3/5), 4/5)[1])
        self.assertEqual(normalPoint((20, 0), (-20, 0)), (-1, 0), "Should be <-1, 0")

    def test_distance(self):
        self.assertAlmostEqual(distanceBetween((0,4), (-3,0)), 5, msg="Should be 5")
        self.assertAlmostEqual(distanceBetween((0,4), (0,-5)), 9, msg="Should be 9")

if __name__ == "__main_":
    unittest.main()
