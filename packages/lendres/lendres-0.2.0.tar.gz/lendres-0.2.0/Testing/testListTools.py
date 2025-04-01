"""
Created on July 23, 2023
@author: Lance A. Endres
"""
import numpy                                                         as np
import copy

from   lendres.io.ConsoleHelper                                      import ConsoleHelper
from   lendres.datatypes.ListTools                                   import ListTools

import unittest

# More information at:
# https://docs.python.org/3/library/unittest.html

class TestListTools(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        verboseLevel = ConsoleHelper.VERBOSEREQUESTED
        # verboseLevel = ConsoleHelper.VERBOSETESTING
        cls.consoleHelper = ConsoleHelper(verboseLevel=verboseLevel)

        cls.listOfLists     = [[1, 3], [5], [8, 11, 14]]

        # Tuples have to have at least 2 elements.
        cls.listOfTuples    = [(1, 3), (5, 6), (8, 11, 14)]

        cls.mixedList       = [1, [5], [8, 11, 14]]

        cls.deepListOfLists = [[1, 3], 5, [[8, 11], 14]]


    def testIsListOfLists(self):
        result = ListTools.IsListOfLists(self.listOfLists)
        self.assertTrue(result)

        result = ListTools.IsListOfLists(self.listOfTuples)
        self.assertTrue(result)

        result = ListTools.IsListOfLists(self.mixedList)
        self.assertFalse(result)


    def testContainsAtLeastOneList(self):
        result = ListTools.ContainsAtLeastOneList(self.listOfLists)
        self.assertTrue(result)

        result = ListTools.ContainsAtLeastOneList(self.listOfTuples)
        self.assertTrue(result)

        result = ListTools.ContainsAtLeastOneList(self.mixedList)
        self.assertTrue(result)

        result = ListTools.ContainsAtLeastOneList([1, 2, 3])
        self.assertFalse(result)


    def testAreListsOfListsSameSize(self):
        result = ListTools.AreListsOfListsSameSize(self.listOfLists, self.listOfLists)
        self.assertTrue(result)

        newList = copy.deepcopy(self.listOfLists)
        newList[0][0] = 0
        result = ListTools.AreListsOfListsSameSize(self.listOfLists, self.listOfLists)
        self.assertTrue(result)

        self.assertRaises(Exception, ListTools.AreListsOfListsSameSize, self.listOfLists, self.mixedList)


    def testCreateListOfLists(self):
        newListofLists = ListTools.CreateListOfLists(self.listOfLists, 1)
        # self.consoleHelper.Display(newListofLists, verboseLevel=ConsoleHelper.VERBOSEREQUESTED)
        self.assertTrue(ListTools.AreListsOfListsSameSize(self.listOfLists, newListofLists))


    def testFlatten(self):
        solution = [1, 3, 5, 8, 11, 14]
        result   = ListTools.Flatten(self.listOfLists)
        self.assertEqual(result, solution)

        solution = [1, 3, 5, 6, 8, 11, 14]
        result   = ListTools.Flatten(self.listOfTuples)
        self.assertEqual(result, solution)

        solution = [1, 5, 8, 11, 14]
        result   = ListTools.Flatten(self.mixedList)
        self.assertEqual(result, solution)

        solution = [1, 3, 5, 8, 11, 14]
        result   = ListTools.Flatten(self.deepListOfLists)
        self.assertEqual(result, solution)


    def testGetFirstItemInEachListOfLists(self):
        solution = [1, 5, 8]
        result   = ListTools.GetFirstItemInEachListOfLists(self.listOfLists)
        self.assertEqual(result, solution)

        ListTools.GetFirstItemInEachListOfLists(self.listOfTuples)
        self.assertEqual(result, solution)

        ListTools.GetFirstItemInEachListOfLists(self.mixedList)
        self.assertEqual(result, solution)


    def testGetLengthOfNestedObjects(self):
        result = ListTools.GetLengthOfNestedObjects(self.listOfLists)
        self.assertEqual(result, 6)

        result = ListTools.GetLengthOfNestedObjects(self.mixedList)
        self.assertEqual(result, 5)


if __name__ == "__main__":
    unittest.main()