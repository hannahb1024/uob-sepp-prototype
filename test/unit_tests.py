import unittest
import src.app
class TestUI(unittest.TestCase):
    def test_exampleTestingFunctionShouldReturnHelloWorld(self):
        self.assertEqual(src.app.exampleTestingFunction(), "Hello, world!", "The basic example testing function has failed. Likely the whole test suite is broken.")

