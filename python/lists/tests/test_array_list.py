import unittest

from option import Option

from lists import ArrayList


class TestDoublyLinkedList(unittest.TestCase):
    def test_init(self):
        lst = ArrayList()
        self.assertEqual(len(lst), 0)
        self.assertEqual(lst.is_empty, True)

    def test_is_empty(self):
        test_cases = [
            (ArrayList(), True),
            (ArrayList([0]).append(0), False),
            (ArrayList([0, 1, 2]), False),
        ]

        for lst, expected_res in test_cases:
            self.assertEqual(lst.is_empty, expected_res)

    def test_repr(self):
        test_cases = [
            (ArrayList(), "[]"),
            (ArrayList([0]), "[0]"),
            (ArrayList([0, 1, 2]), "[0, 1, 2]"),
        ]

        for lst, expected_string in test_cases:
            self.assertEqual(str(lst), expected_string)

    def test_iter(self):
        test_cases = [
            (ArrayList(), []),
            (ArrayList([0]), [0]),
            (
                ArrayList(["hello", " ", "world"]),
                ["hello", " ", "world"],
            ),
            (ArrayList([0]), [0]),
            (ArrayList([[3], [2], [1]]), [[3], [2], [1]]),
        ]

        for lst, expected_els in test_cases:
            els = []
            for el in lst:
                els.append(el)
            self.assertListEqual(els, expected_els)

    def test_eq(self):
        test_cases = [
            (ArrayList(), ArrayList(), True),
            (ArrayList().append(0), ArrayList().prepend(0), True),
            (
                ArrayList().append(0).append(1).append(2),
                ArrayList().prepend(2).prepend(1).prepend(0),
                True,
            ),
            (ArrayList(), 1, False),
            (ArrayList().append(0), ArrayList().prepend(1), False),
            (
                ArrayList().append(0).append(1).append(2),
                ArrayList().prepend(3).prepend(2).prepend(1).prepend(0),
                False,
            ),
        ]

        for lst1, lst2, expected_equal in test_cases:
            self.assertEqual(lst1 == lst2, expected_equal)

    def test_to_python_list(self):
        test_cases = [
            (ArrayList(), []),
            (ArrayList().append(0), [0]),
            (
                ArrayList().append("hello").append(" ").append("world"),
                ["hello", " ", "world"],
            ),
            (ArrayList().prepend(0), [0]),
            (ArrayList().prepend([1]).prepend([2]).prepend([3]), [[3], [2], [1]]),
        ]

        for lst, expected_py_lst in test_cases:
            self.assertListEqual(lst.to_python_list(), expected_py_lst)

    def test_get_at_idx(self):
        test_cases = [
            (ArrayList([]), 0, Option.NONE()),
            (ArrayList([0]), -2, Option.NONE()),
            (ArrayList([0]), -1, Option.Some(0)),
            (ArrayList([0]), 0, Option.Some(0)),
            (ArrayList([0]), 1, Option.NONE()),
            (ArrayList([0, 1, 2]), -2, Option.NONE()),
            (ArrayList([0, 1, 2]), -1, Option.Some(2)),
            (ArrayList([0, 1, 2]), 0, Option.Some(0)),
            (ArrayList([0, 1, 2]), 1, Option.Some(1)),
            (ArrayList([0, 1, 2]), 2, Option.Some(2)),
            (ArrayList([0, 1, 2]), 3, Option.NONE()),
        ]

        for lst, i, expected_res in test_cases:
            self.assertEqual(lst.get_at_idx(i), expected_res)

    def test_get_by_val(self):
        test_cases = [
            (ArrayList(), 0, Option.NONE()),
            (ArrayList([0]), 0, Option.Some(0)),
            (ArrayList([0]), 1, Option.NONE()),
            (ArrayList([0, 1, 2]), 0, Option.Some(0)),
            (ArrayList([0, 1, 2]), 1, Option.Some(1)),
            (ArrayList([0, 1, 2]), 2, Option.Some(2)),
            (ArrayList([0, 1, 2]), 3, Option.NONE()),
        ]

        for lst, v, expected_res in test_cases:
            self.assertEqual(lst.get_by_val(v), expected_res)

    def test_insert_at_idx(self):
        test_cases = [
            (ArrayList(), -1, 0, ArrayList([0])),
            (ArrayList(), 0, 0, ArrayList([0])),
            (ArrayList(), 1, 0, ArrayList()),
            (ArrayList([0]), -1, 1, ArrayList([0, 1])),
            (ArrayList([0]), 0, 1, ArrayList([1, 0])),
            (ArrayList([0]), 1, 1, ArrayList([0, 1])),
            (ArrayList([0]), 2, 1, ArrayList([0])),
            (ArrayList([0, 1, 2]), -1, 3, ArrayList([0, 1, 2, 3])),
            (ArrayList([0, 1, 2]), 0, 3, ArrayList([3, 0, 1, 2])),
            (ArrayList([0, 1, 2]), 1, 3, ArrayList([0, 3, 1, 2])),
            (ArrayList([0, 1, 2]), 2, 3, ArrayList([0, 1, 3, 2])),
            (ArrayList([0, 1, 2]), 3, 3, ArrayList([0, 1, 2, 3])),
            (ArrayList([0, 1, 2]), 4, 3, ArrayList([0, 1, 2])),
        ]

        for lst, i, v, expected_lst in test_cases:
            self.assertEqual(lst.insert_at_idx(i, v), expected_lst)

    def test_prepend(self):
        test_cases = [
            (ArrayList(), 0, ArrayList([0])),
            (ArrayList([0]), 1, ArrayList([1, 0])),
            (ArrayList([0, 1, 2]), 3, ArrayList([3, 0, 1, 2])),
        ]

        for lst, v, expected_lst in test_cases:
            self.assertEqual(lst.prepend(v), expected_lst)

    def test_append(self):
        test_cases = [
            (ArrayList(), 0, ArrayList([0])),
            (ArrayList([0]), 1, ArrayList([0, 1])),
            (ArrayList([0, 1, 2]), 3, ArrayList([0, 1, 2, 3])),
        ]

        for lst, v, expected_lst in test_cases:
            self.assertEqual(lst.append(v), expected_lst)

    def test_set_at_idx(self):
        test_cases = [
            (ArrayList([]), 0, 0, ArrayList([])),
            (ArrayList([0]), -1, 10, ArrayList([10])),
            (ArrayList([0]), 0, 10, ArrayList([10])),
            (ArrayList([0]), 1, 10, ArrayList([0])),
            (ArrayList([0, 1, 2]), -1, 10, ArrayList([0, 1, 10])),
            (ArrayList([0, 1, 2]), 0, 10, ArrayList([10, 1, 2])),
            (ArrayList([0, 1, 2]), 1, 10, ArrayList([0, 10, 2])),
            (ArrayList([0, 1, 2]), 2, 10, ArrayList([0, 1, 10])),
            (ArrayList([0, 1, 2]), 3, 10, ArrayList([0, 1, 2])),
        ]

        for lst, i, v, expected_lst in test_cases:
            self.assertEqual(lst.set_at_idx(i, v), expected_lst)

    def test_extend(self):
        test_cases = [
            (ArrayList(), ArrayList(), ArrayList()),
            (ArrayList(), ArrayList([0, 1, 2]), ArrayList([0, 1, 2])),
            (ArrayList([0, 1, 2]), ArrayList(), ArrayList([0, 1, 2])),
            (ArrayList([0, 1, 2]), ArrayList([3]), ArrayList([0, 1, 2, 3])),
            (ArrayList([0]), ArrayList([1, 2, 3]), ArrayList([0, 1, 2, 3])),
            (ArrayList([0, 1, 2]), ArrayList([3, 4, 5]), ArrayList([0, 1, 2, 3, 4, 5])),
        ]

        for lst1, lst2, expected_lst in test_cases:
            self.assertEqual(lst1.extend(lst2), expected_lst)

    def test_add(self):
        test_cases = [
            (ArrayList(), ArrayList(), ArrayList()),
            (ArrayList(), ArrayList([0, 1, 2]), ArrayList([0, 1, 2])),
            (ArrayList([0, 1, 2]), ArrayList(), ArrayList([0, 1, 2])),
            (ArrayList([0, 1, 2]), ArrayList([3]), ArrayList([0, 1, 2, 3])),
            (ArrayList([0]), ArrayList([1, 2, 3]), ArrayList([0, 1, 2, 3])),
            (ArrayList([0, 1, 2]), ArrayList([3, 4, 5]), ArrayList([0, 1, 2, 3, 4, 5])),
        ]

        for lst1, lst2, expected_lst in test_cases:
            self.assertEqual(lst1 + lst2, expected_lst)

    def test_bool(self):
        test_cases = [
            (ArrayList(), False),
            (ArrayList([]), False),
            (ArrayList([0]), True),
            (ArrayList([0, 1, 2]), True),
        ]

        for lst, expected_bool in test_cases:
            self.assertEqual(bool(lst), expected_bool)

    def test_clone(self):
        lst = ArrayList()
        clone = lst.clone()
        lst.append(0)
        self.assertEqual(clone, ArrayList())
        self.assertNotEqual(lst, clone)

        lst = ArrayList([1, 2, 3])
        clone = lst.clone()
        lst.append(4)
        self.assertEqual(clone, ArrayList([1, 2, 3]))
        self.assertNotEqual(lst, clone)

        lst = ArrayList(["a", "b", "c"])
        clone = lst.clone()
        lst.append("d")
        self.assertEqual(clone, ArrayList(["a", "b", "c"]))
        self.assertNotEqual(lst, clone)

        lst = ArrayList([[1], [2], [3]])
        clone = lst.clone()
        py_lst = lst.get_at_idx(0).unwrap()
        py_lst.append(2)
        self.assertEqual(clone, ArrayList([[1], [2], [3]]))
        self.assertNotEqual(lst, clone)

    def test_selection_sort(self):
        test_cases = [
            (ArrayList(), ArrayList()),
            (ArrayList([0]), ArrayList([0])),
            (ArrayList([0, 1]), ArrayList([0, 1])),
            (ArrayList([1, 0]), ArrayList([0, 1])),
            (ArrayList([0, 1, 2]), ArrayList([0, 1, 2])),
            (ArrayList([2, 1, 0]), ArrayList([0, 1, 2])),
            (ArrayList([2, 1, 5, 4, 7]), ArrayList([1, 2, 4, 5, 7])),
        ]

        for lst, expected_lst in test_cases:
            lst.selection_sort()
            self._check_is_sorted(lst)
            self.assertEqual(lst, expected_lst)

    def test_quicksort(self):
        test_cases = [
            (ArrayList(), ArrayList()),
            (ArrayList([0]), ArrayList([0])),
            (ArrayList([0, 1]), ArrayList([0, 1])),
            (ArrayList([1, 0]), ArrayList([0, 1])),
            (ArrayList([0, 1, 2]), ArrayList([0, 1, 2])),
            (ArrayList([2, 1, 0]), ArrayList([0, 1, 2])),
            (ArrayList([2, 1, 5, 4, 7]), ArrayList([1, 2, 4, 5, 7])),
        ]

        for lst, expected_lst in test_cases:
            lst.quicksort()
            self._check_is_sorted(lst)
            self.assertEqual(lst, expected_lst)

    def test_insertion_sort(self):
        test_cases = [
            (ArrayList(), ArrayList()),
            (ArrayList([0]), ArrayList([0])),
            (ArrayList([0, 1]), ArrayList([0, 1])),
            (ArrayList([1, 0]), ArrayList([0, 1])),
            (ArrayList([0, 1, 2]), ArrayList([0, 1, 2])),
            (ArrayList([2, 1, 0]), ArrayList([0, 1, 2])),
            (ArrayList([2, 1, 5, 4, 7]), ArrayList([1, 2, 4, 5, 7])),
        ]

        for lst, expected_lst in test_cases:
            lst.insertion_sort()
            self._check_is_sorted(lst)
            self.assertEqual(lst, expected_lst)

    def test_bubble_sort(self):
        test_cases = [
            (ArrayList(), ArrayList()),
            (ArrayList([0]), ArrayList([0])),
            (ArrayList([0, 1]), ArrayList([0, 1])),
            (ArrayList([1, 0]), ArrayList([0, 1])),
            (ArrayList([0, 1, 2]), ArrayList([0, 1, 2])),
            (ArrayList([2, 1, 0]), ArrayList([0, 1, 2])),
            (ArrayList([2, 1, 5, 4, 7]), ArrayList([1, 2, 4, 5, 7])),
        ]

        for lst, expected_lst in test_cases:
            lst.bubble_sort()
            self._check_is_sorted(lst)
            self.assertEqual(lst, expected_lst)

    def _check_is_sorted[T](self, lst: ArrayList[T]):
        prev = None
        for el in lst:
            self.assertTrue(prev is None or el >= prev)
            prev = el


def main():
    unittest.main()


if __name__ == "__main__":
    main()
