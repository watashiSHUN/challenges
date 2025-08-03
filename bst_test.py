import unittest

from bst import findfirst, findfirstafter, findfirstbefore, findlast


class TestBinarySearchFunctions(unittest.TestCase):

    def setUp(self):
        self.test_array = [1, 2, 3, 5, 5, 5, 8, 9, 10]
        self.empty_array = []
        self.single_element = [5]
        self.all_same = [5, 5, 5, 5]

    def test_findfirst(self):
        """Test finding first occurrence of target"""
        # Target exists with duplicates
        self.assertEqual(findfirst(self.test_array, 5), 3)

        # Target exists, single occurrence
        self.assertEqual(findfirst(self.test_array, 1), 0)
        self.assertEqual(findfirst(self.test_array, 10), 8)

        # Target doesn't exist
        self.assertEqual(findfirst(self.test_array, 4), -1)
        self.assertEqual(findfirst(self.test_array, 11), -1)

        # Empty array
        self.assertEqual(findfirst(self.empty_array, 5), -1)

        # Single element
        self.assertEqual(findfirst(self.single_element, 5), 0)
        self.assertEqual(findfirst(self.single_element, 3), -1)

    def test_findlast(self):
        """Test finding last occurrence of target"""
        # Target exists with duplicates
        self.assertEqual(findlast(self.test_array, 5), 5)

        # Target exists, single occurrence
        self.assertEqual(findlast(self.test_array, 1), 0)
        self.assertEqual(findlast(self.test_array, 10), 8)

        # Target doesn't exist
        self.assertEqual(findlast(self.test_array, 4), -1)
        self.assertEqual(findlast(self.test_array, 11), -1)

        # Empty array
        self.assertEqual(findlast(self.empty_array, 5), -1)

        # Single element
        self.assertEqual(findlast(self.single_element, 5), 0)
        self.assertEqual(findlast(self.single_element, 3), -1)

        # All same elements
        self.assertEqual(findlast(self.all_same, 5), 3)

    def test_findfirstbefore(self):
        """Test finding first element before target"""
        # Target exists in array
        self.assertEqual(
            findfirstbefore(self.test_array, 5), 2
        )  # Should return index of 3

        # Target doesn't exist but has elements before it
        self.assertEqual(
            findfirstbefore(self.test_array, 6), 5
        )  # Should return index of last 5
        self.assertEqual(
            findfirstbefore(self.test_array, 4), 2
        )  # Should return index of 3

        # Target smaller than first element
        self.assertEqual(findfirstbefore(self.test_array, 0), -1)
        self.assertEqual(findfirstbefore(self.test_array, 1), -1)

        # Empty array
        self.assertEqual(findfirstbefore(self.empty_array, 5), -1)

        # Single element
        self.assertEqual(findfirstbefore(self.single_element, 6), 0)
        self.assertEqual(findfirstbefore(self.single_element, 3), -1)

    def test_findfirstafter(self):
        """Test finding first element after target"""
        # Target exists in array
        self.assertEqual(
            findfirstafter(self.test_array, 5), 6
        )  # Should return index of 8

        # Target doesn't exist but has elements after it
        self.assertEqual(
            findfirstafter(self.test_array, 4), 3
        )  # Should return index of first 5
        self.assertEqual(
            findfirstafter(self.test_array, 6), 6
        )  # Should return index of 8

        # Target larger than last element
        self.assertEqual(findfirstafter(self.test_array, 11), -1)
        self.assertEqual(findfirstafter(self.test_array, 10), -1)

        # Empty array
        self.assertEqual(findfirstafter(self.empty_array, 5), -1)

        # Single element
        self.assertEqual(findfirstafter(self.single_element, 3), 0)
        self.assertEqual(findfirstafter(self.single_element, 6), -1)

    def test_edge_cases(self):
        """Test edge cases with two-element arrays"""
        two_elements = [3, 7]

        # Test findfirst
        self.assertEqual(findfirst(two_elements, 3), 0)
        self.assertEqual(findfirst(two_elements, 7), 1)
        self.assertEqual(findfirst(two_elements, 5), -1)

        # Test findlast
        self.assertEqual(findlast(two_elements, 3), 0)
        self.assertEqual(findlast(two_elements, 7), 1)
        self.assertEqual(findlast(two_elements, 5), -1)

        # Test findfirstbefore
        self.assertEqual(
            findfirstbefore(two_elements, 5), 0
        )  # Should return index of 3
        self.assertEqual(
            findfirstbefore(two_elements, 8), 1
        )  # Should return index of 7

        # Test findfirstafter
        self.assertEqual(findfirstafter(two_elements, 5), 1)  # Should return index of 7
        self.assertEqual(findfirstafter(two_elements, 2), 0)  # Should return index of 3


if __name__ == "__main__":
    unittest.main()
