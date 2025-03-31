import unittest
from my_package.main import greet, add

class TestMyPackage(unittest.TestCase):
    def test_greet(self):
        self.assertEqual(greet(), "Hello, World!")
        self.assertEqual(greet("PyPI"), "Hello, PyPI!")
        
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertAlmostEqual(add(0.1, 0.2), 0.3)
        
if __name__ == "__main__":
    unittest.main()