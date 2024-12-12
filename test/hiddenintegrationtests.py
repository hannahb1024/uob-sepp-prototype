import sys
import unittest
import src.app
from PyQt5.QtWidgets import *
from qfluentwidgets import *
class TestUI(unittest.TestCase):
    def test_exampleTestingFunctionShouldReturnHelloWorld(self):
        self.assertEqual(src.app.exampleTestingFunction(), "Hello, world!", "The basic example testing function has failed. Likely the whole test suite is broken.")

    def test_UI(self):
        app = QApplication([])
        window = src.app.mainWindow()

        #check it loads the database correctly
        window.loadDatabaseButton.click()
        print(window.windowType())
        print(window.markerCards)
        print(window.markerListPlaceholder.windowType())
        self.assertEqual(len(window.markerCards), 5, "There should be 5 marker cards when loading this dataset.")
        self.assertEqual(window.markerCards[0].marker.firstName, "Stacy","First marker's name should be stacy. Was she loaded?")
        self.assertEqual(window.markerCards[0].marker.chiSquaredAll, 8.243308080808081, "Chi squared against all markers for this marker should be ~8.24")
        self.assertEqual(window.markerCards[0].trustIsChecked, False, "Marker trust should be checked fale by default")
        window.markerCards[0].inspect.click()
        print("here")
        app.quit()