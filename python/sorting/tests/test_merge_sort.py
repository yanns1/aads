import unittest

import sorting


class TestMergeSort(unittest.TestCase):
    def test_merge_sort_on_integers(self):
        test_cases = [
            # empty input
            ([], []),
            # one element, thus already sorted
            ([0], [0]),
            # already sorted
            ([0, 1, 2, 3], [0, 1, 2, 3]),
            # sorted but in reverse order
            ([3, 2, 1, 0], [0, 1, 2, 3]),
            # randomly unsorted, even number of elements
            ([16, 0, 4, 2, 8, 5, 3, 1], [0, 1, 2, 3, 4, 5, 8, 16]),
            # randomly unsorted, odd number of elements
            ([16, 0, 4, 2, 8, 5, 3], [0, 2, 3, 4, 5, 8, 16]),
        ]

        for input, expected_output in test_cases:
            self.assertListEqual(sorting.merge_sort_rec(input), expected_output)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
