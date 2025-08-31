import unittest
from circle import *

class test_circle(unittest.TestCase):
    def test_getRadius(self):
        circle = Circle(10)
        self.assertEqual(circle.getRadius(), 10)

    def test_getRadius_neg(self):
        circle = Circle(-9)
        self.assertEqual(circle.getRadius(), -9)

    def test_setRadius(self):
        circle = Circle(10)
        circle.setRadius(100)
        self.assertEqual(circle.getRadius(), 100)

    def test_setRadius_neg(self):
        circle = Circle(10)
        circle.setRadius(-9)
        self.assertEqual(circle.getRadius(), 10)

    def test_getArea_zed(self):
        circle = Circle(2)
        self.assertEqual(circle.getArea(), 0)

    def test_getArea(self):
        circle = Circle(10)
        self.assertEqual(circle.getArea(), 314.1592653589793)

    def test_getCircumference(self):
        circle = Circle(10)
        self.assertEqual(circle.getCircumference(), 62.83185307179586)


if __name__ == "__main__":
    unittest.main()
