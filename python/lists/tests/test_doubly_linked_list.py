import unittest

from option import Option

from lists import DoublyLinkedList


class TestDoublyLinkedList(unittest.TestCase):
    def test_init(self):
        lst = DoublyLinkedList()
        self.assertEqual(len(lst), 0)
        self.assertEqual(lst.is_empty, True)
        self.assertFalse(lst)

    def test_repr(self):
        test_cases = [
            (DoublyLinkedList(), "[]"),
            (DoublyLinkedList([0]), "[0]"),
            (DoublyLinkedList([0, 1, 2, 3, 4]), "[0 >< 1 >< 2 >< 3 >< 4]"),
        ]

        for lst, expected_repr in test_cases:
            self.assertEqual(str(lst), expected_repr)

    def test_len(self):
        test_cases = [
            (DoublyLinkedList(), 0),
            (DoublyLinkedList([0]), 1),
            (DoublyLinkedList([0, 1, 2, 3, 4]), 5),
            (DoublyLinkedList(list(range(100))), 100),
        ]

        for lst, expected_len in test_cases:
            self.assertEqual(len(lst), expected_len)

    def test_iter(self):
        lst = DoublyLinkedList(list(range(5)))

        els = list(lst)
        self.assertListEqual(els, list(range(5)))

        els = []
        for el in lst:
            els.append(el)
        self.assertListEqual(els, list(range(5)))

        els = []
        it = iter(lst)
        els.append(next(it))
        els.append(next(it))
        els.append(next(it))
        els.append(next(it))
        els.append(next(it))
        self.assertRaises(StopIteration, lambda: els.append(next(it)))
        self.assertListEqual(els, list(range(5)))

    def test_get_at_idx(self):
        lst = DoublyLinkedList(list(range(5)))
        for n in range(5):
            output_node = lst.get_at_idx(n)
            self.assertFalse(output_node.is_none)
            self.assertEqual(output_node.unwrap().v, n)
        self.assertTrue(lst.get_at_idx(-2).is_none)
        last_node = lst.get_at_idx(-1)
        self.assertTrue(last_node.is_some and last_node.unwrap().v == 4)
        self.assertTrue(lst.get_at_idx(5).is_none)

    def test_get_by_val(self):
        lst = DoublyLinkedList(list(range(5)))
        for n in range(5):
            output_node = lst.get_by_val(n)
            self.assertFalse(output_node.is_none)
            self.assertEqual(output_node.unwrap().v, n)
        self.assertTrue(lst.get_at_idx(-2).is_none)
        last_node = lst.get_at_idx(-1)
        self.assertTrue(last_node.is_some and last_node.unwrap().v == 4)
        self.assertTrue(lst.get_at_idx(5).is_none)

    def test_getitem(self):
        lst = DoublyLinkedList(list(range(5)))
        for n in range(5):
            self.assertEqual(lst[n], n)
        self.assertEqual(lst[-1], 4)
        self.assertRaises(TypeError, lambda: lst["wrong key type"])
        self.assertRaises(IndexError, lambda: lst[-2])
        self.assertRaises(IndexError, lambda: lst[5])

    def test_set_at_idx(self):
        lst = DoublyLinkedList()
        set_node = lst.set_at_idx(0, 0)
        self.assertTrue(set_node.is_none)
        self.assertEqual(lst, DoublyLinkedList())

        lst = DoublyLinkedList([0])
        set_node = lst.set_at_idx(1, 1)
        self.assertTrue(set_node.is_none)
        self.assertEqual(lst, DoublyLinkedList([0]))
        set_node = lst.set_at_idx(-2, 1)
        self.assertTrue(set_node.is_none)
        self.assertEqual(lst, DoublyLinkedList([0]))
        set_node = lst.set_at_idx(-1, 1)
        self.assertTrue(set_node.is_some and set_node.unwrap().v == 1)
        self.assertEqual(lst, DoublyLinkedList([1]))
        set_node = lst.set_at_idx(0, 2)
        self.assertTrue(set_node.is_some and set_node.unwrap().v == 2)
        self.assertEqual(lst, DoublyLinkedList([2]))

        lst = DoublyLinkedList([0, 1, 2])
        set_node = lst.set_at_idx(3, 3)
        self.assertTrue(set_node.is_none)
        self.assertEqual(lst, DoublyLinkedList([0, 1, 2]))
        set_node = lst.set_at_idx(-2, -2)
        self.assertTrue(set_node.is_none)
        self.assertEqual(lst, DoublyLinkedList([0, 1, 2]))
        set_node = lst.set_at_idx(0, 3)
        self.assertTrue(set_node.is_some and set_node.unwrap().v == 3)
        self.assertEqual(lst, DoublyLinkedList([3, 1, 2]))
        set_node = lst.set_at_idx(1, 4)
        self.assertTrue(set_node.is_some and set_node.unwrap().v == 4)
        self.assertEqual(lst, DoublyLinkedList([3, 4, 2]))
        set_node = lst.set_at_idx(2, 5)
        self.assertTrue(set_node.is_some and set_node.unwrap().v == 5)
        self.assertEqual(lst, DoublyLinkedList([3, 4, 5]))
        set_node = lst.set_at_idx(-1, 6)
        self.assertTrue(set_node.is_some and set_node.unwrap().v == 6)
        self.assertEqual(lst, DoublyLinkedList([3, 4, 6]))

    def test_set_by_val(self):
        lst = DoublyLinkedList()
        set_node = lst.set_by_val(0, 1)
        self.assertTrue(set_node.is_none)
        self.assertEqual(lst, DoublyLinkedList())

        lst = DoublyLinkedList([0])
        set_node = lst.set_by_val(1, 2)
        self.assertTrue(set_node.is_none)
        self.assertEqual(lst, DoublyLinkedList([0]))
        set_node = lst.set_by_val(-1, -2)
        self.assertTrue(set_node.is_none)
        self.assertEqual(lst, DoublyLinkedList([0]))
        set_node = lst.set_by_val(0, 1)
        self.assertTrue(set_node.is_some and set_node.unwrap().v == 1)
        self.assertEqual(lst, DoublyLinkedList([1]))
        set_node = lst.set_by_val(1, 2)
        self.assertTrue(set_node.is_some and set_node.unwrap().v == 2)
        self.assertEqual(lst, DoublyLinkedList([2]))

        lst = DoublyLinkedList([0, 1, 2])
        set_node = lst.set_by_val(3, 4)
        self.assertTrue(set_node.is_none)
        self.assertEqual(lst, DoublyLinkedList([0, 1, 2]))
        set_node = lst.set_by_val(-2, -3)
        self.assertTrue(set_node.is_none)
        self.assertEqual(lst, DoublyLinkedList([0, 1, 2]))
        set_node = lst.set_by_val(0, 3)
        self.assertTrue(set_node.is_some and set_node.unwrap().v == 3)
        self.assertEqual(lst, DoublyLinkedList([3, 1, 2]))
        set_node = lst.set_by_val(1, 4)
        self.assertTrue(set_node.is_some and set_node.unwrap().v == 4)
        self.assertEqual(lst, DoublyLinkedList([3, 4, 2]))
        set_node = lst.set_by_val(2, 5)
        self.assertTrue(set_node.is_some and set_node.unwrap().v == 5)
        self.assertEqual(lst, DoublyLinkedList([3, 4, 5]))

    def test_setitem(self):
        lst = DoublyLinkedList()

        def f1():
            lst[0] = 0

        self.assertRaises(IndexError, f1)
        self.assertEqual(lst, DoublyLinkedList())

        lst = DoublyLinkedList([0])

        def f2():
            lst[1] = 1

        self.assertRaises(IndexError, f2)
        self.assertEqual(lst, DoublyLinkedList([0]))

        def f3():
            lst[-2] = -2

        self.assertRaises(IndexError, f3)
        self.assertEqual(lst, DoublyLinkedList([0]))
        lst[-1] = 1
        self.assertEqual(lst, DoublyLinkedList([1]))
        lst[0] = 2
        self.assertEqual(lst, DoublyLinkedList([2]))

        lst = DoublyLinkedList([0, 1, 2])

        def f4():
            lst[3] = 3

        self.assertRaises(IndexError, f4)
        self.assertEqual(lst, DoublyLinkedList([0, 1, 2]))

        def f5():
            lst[-2] = 2

        self.assertRaises(IndexError, f5)
        self.assertEqual(lst, DoublyLinkedList([0, 1, 2]))
        lst[0] = 3
        self.assertEqual(lst, DoublyLinkedList([3, 1, 2]))
        lst[1] = 4
        self.assertEqual(lst, DoublyLinkedList([3, 4, 2]))
        lst[2] = 5
        self.assertEqual(lst, DoublyLinkedList([3, 4, 5]))
        lst[-1] = 6
        self.assertEqual(lst, DoublyLinkedList([3, 4, 6]))

    def test_insert(self):
        lst = DoublyLinkedList([0])
        node = lst.get_at_idx(0).unwrap()
        new_node = lst.insert(-1, Option.Some(node), False)
        self.assertEqual(new_node.v, -1)
        self.assertEqual(str(lst), "[-1 >< 0]")
        new_node = lst.insert(1, Option.Some(node), True)
        self.assertEqual(new_node.v, 1)
        self.assertEqual(str(lst), "[-1 >< 0 >< 1]")
        new_node = lst.insert(2, Option.NONE())
        self.assertEqual(new_node.v, 2)
        self.assertEqual(str(lst), "[-1 >< 0 >< 1 >< 2]")

        lst = DoublyLinkedList([0, 3, 6])
        node0 = lst.get_at_idx(0).unwrap()
        node1 = lst.get_at_idx(1).unwrap()
        node2 = lst.get_at_idx(2).unwrap()
        new_node = lst.insert(-1, Option.Some(node0), False)
        self.assertEqual(new_node.v, -1)
        self.assertEqual(str(lst), "[-1 >< 0 >< 3 >< 6]")
        new_node = lst.insert(1, Option.Some(node0), True)
        self.assertEqual(new_node.v, 1)
        self.assertEqual(str(lst), "[-1 >< 0 >< 1 >< 3 >< 6]")
        new_node = lst.insert(2, Option.Some(node1), False)
        self.assertEqual(new_node.v, 2)
        self.assertEqual(str(lst), "[-1 >< 0 >< 1 >< 2 >< 3 >< 6]")
        new_node = lst.insert(4, Option.Some(node1), True)
        self.assertEqual(new_node.v, 4)
        self.assertEqual(str(lst), "[-1 >< 0 >< 1 >< 2 >< 3 >< 4 >< 6]")
        new_node = lst.insert(5, Option.Some(node2), False)
        self.assertEqual(new_node.v, 5)
        self.assertEqual(str(lst), "[-1 >< 0 >< 1 >< 2 >< 3 >< 4 >< 5 >< 6]")
        new_node = lst.insert(7, Option.Some(node2), True)
        self.assertEqual(new_node.v, 7)
        self.assertEqual(str(lst), "[-1 >< 0 >< 1 >< 2 >< 3 >< 4 >< 5 >< 6 >< 7]")

    def test_insert_at_idx(self):
        lst = DoublyLinkedList()
        for n in range(1, 4):
            new_node = lst.insert_at_idx(0, -n)
            self.assertTrue(new_node.is_some)
            self.assertEqual(new_node.unwrap().v, -n)

        for n in range(1, 4):
            new_node = lst.insert_at_idx(len(lst), n)
            self.assertTrue(new_node.is_some)
            self.assertEqual(new_node.unwrap().v, n)

        new_node = lst.insert_at_idx(3, 0)
        self.assertTrue(new_node.is_some)
        self.assertEqual(new_node.unwrap().v, 0)

        new_node = lst.insert_at_idx(1, -10)
        self.assertTrue(new_node.is_some)
        self.assertEqual(new_node.unwrap().v, -10)

        new_node = lst.insert_at_idx(len(lst) - 1, 10)
        self.assertTrue(new_node.is_some)
        self.assertEqual(new_node.unwrap().v, 10)

        new_node = lst.insert_at_idx(-2, -100)
        self.assertTrue(new_node.is_none)

        new_node = lst.insert_at_idx(len(lst) + 1, 100)
        self.assertTrue(new_node.is_none)

        self.assertEqual(lst.is_empty, False)
        self.assertEqual(len(lst), 9)
        self.assertEqual(str(lst), "[-3 >< -10 >< -2 >< -1 >< 0 >< 1 >< 2 >< 10 >< 3]")

    def test_append(self):
        lst = DoublyLinkedList()
        for n in range(5):
            new_node = lst.append(n)
            self.assertEqual(new_node._v, n)

        self.assertTrue(bool(lst))
        self.assertFalse(lst.is_empty, False)
        self.assertEqual(len(lst), 5)
        self.assertEqual(str(lst), "[0 >< 1 >< 2 >< 3 >< 4]")

    def test_prepend(self):
        lst = DoublyLinkedList()
        for n in range(5):
            new_node = lst.prepend(n)
            self.assertEqual(new_node._v, n)

        self.assertTrue(bool(lst))
        self.assertEqual(lst.is_empty, False)
        self.assertEqual(len(lst), 5)
        self.assertEqual(str(lst), "[4 >< 3 >< 2 >< 1 >< 0]")

    def test_delete(self):
        # One-element list.
        lst = DoublyLinkedList()
        lst.append(0)
        node = lst.get_at_idx(0).unwrap()
        lst.delete(node)
        self.assertIsNone(node.prv)
        self.assertIsNone(node.nxt)
        self.assertEqual(len(lst), 0)
        self.assertEqual(str(lst), "[]")

        # N-elements list...
        # ... delete at the beginning
        lst = DoublyLinkedList(list(range(5)))
        node = lst.get_at_idx(0).unwrap()
        lst.delete(node)
        self.assertIsNone(node.prv)
        self.assertIsNone(node.nxt)
        self.assertEqual(len(lst), 4)
        self.assertEqual(str(lst), "[1 >< 2 >< 3 >< 4]")

        # ... delete at the end
        lst = DoublyLinkedList(list(range(5)))
        node = lst.get_at_idx(4).unwrap()
        lst.delete(node)
        self.assertIsNone(node.prv)
        self.assertIsNone(node.nxt)
        self.assertEqual(len(lst), 4)
        self.assertEqual(str(lst), "[0 >< 1 >< 2 >< 3]")

        # ... delete in the middle
        lst = DoublyLinkedList(list(range(5)))
        node = lst.get_at_idx(2).unwrap()
        lst.delete(node)
        self.assertIsNone(node.prv)
        self.assertIsNone(node.nxt)
        self.assertEqual(len(lst), 4)
        self.assertEqual(str(lst), "[0 >< 1 >< 3 >< 4]")

    def test_delete_at_idx(self):
        lst = DoublyLinkedList(list(range(5)))

        deleted_node = lst.delete_at_idx(-2)
        self.assertTrue(deleted_node.is_none)

        deleted_node = lst.delete_at_idx(len(lst))
        self.assertTrue(deleted_node.is_none)

        deleted_node = lst.delete_at_idx(0)
        self.assertTrue(deleted_node.is_some)
        self.assertEqual(deleted_node.unwrap().v, 0)

        deleted_node = lst.delete_at_idx(-1)
        self.assertTrue(deleted_node.is_some)
        self.assertEqual(deleted_node.unwrap().v, 4)

        deleted_node = lst.delete_at_idx(1)
        self.assertTrue(deleted_node.is_some)
        self.assertEqual(deleted_node.unwrap().v, 2)

        self.assertEqual(str(lst), "[1 >< 3]")

    def test_delete_by_val(self):
        lst = DoublyLinkedList()

        # Test on empty list.
        deleted_node = lst.delete_by_val(0)
        self.assertTrue(deleted_node.is_none)

        # Test on one element list.
        lst.append(0)
        deleted_node = lst.delete_by_val(0)
        self.assertTrue(deleted_node.is_some)
        self.assertEqual(deleted_node.unwrap().v, 0)
        self.assertEqual(str(lst), "[]")

        for n in range(5):
            lst.append(n)

        deleted_node = lst.delete_by_val(-1)
        self.assertTrue(deleted_node.is_none)

        deleted_node = lst.delete_by_val(len(lst))
        self.assertTrue(deleted_node.is_none)

        deleted_node = lst.delete_by_val(0)
        self.assertTrue(deleted_node.is_some)
        self.assertEqual(deleted_node.unwrap().v, 0)

        deleted_node = lst.delete_by_val(4)
        self.assertTrue(deleted_node.is_some)
        self.assertEqual(deleted_node.unwrap().v, 4)

        deleted_node = lst.delete_by_val(2)
        self.assertTrue(deleted_node.is_some)
        self.assertEqual(deleted_node.unwrap().v, 2)

        self.assertEqual(str(lst), "[1 >< 3]")

    def test_delitem(self):
        lst = DoublyLinkedList(list(range(5)))

        def f1():
            del lst[-2]

        self.assertRaises(IndexError, f1)

        def f2():
            del lst[len(lst)]

        self.assertRaises(IndexError, f2)

        del lst[0]
        self.assertEqual(str(lst), "[1 >< 2 >< 3 >< 4]")

        del lst[-1]
        self.assertEqual(str(lst), "[1 >< 2 >< 3]")

        del lst[1]
        self.assertEqual(str(lst), "[1 >< 3]")

    def test_rotate(self):
        # Rotate empty list.
        lst = DoublyLinkedList()
        lst.rotate(1)
        # Nothing happened, but doesn't throw.
        self.assertEqual(str(lst), "[]")

        # Rotate one-element list.
        lst = DoublyLinkedList([0])
        lst.rotate(1)
        # Nothing happened, but doesn't throw.
        self.assertEqual(str(lst), "[0]")

        # Rotate two-elements list.
        lst = DoublyLinkedList([0, 1])
        lst.rotate(1)
        self.assertEqual(str(lst), "[1 >< 0]")

        # Rotate with offset equivalent to 0.
        lst = DoublyLinkedList(list(range(5)))
        lst.rotate(0)
        lst.rotate(5)
        lst.rotate(10)
        lst.rotate(100)
        # Nothing should have happened.
        self.assertEqual(str(lst), "[0 >< 1 >< 2 >< 3 >< 4]")

        # Rotate n-elements list.
        lst = DoublyLinkedList(list(range(5)))
        lst.rotate(1)
        self.assertEqual(str(lst), "[4 >< 0 >< 1 >< 2 >< 3]")
        lst.rotate(-1)
        self.assertEqual(str(lst), "[0 >< 1 >< 2 >< 3 >< 4]")
        lst.rotate(2)
        self.assertEqual(str(lst), "[3 >< 4 >< 0 >< 1 >< 2]")
        lst.rotate(-2)
        self.assertEqual(str(lst), "[0 >< 1 >< 2 >< 3 >< 4]")
        lst.rotate(3)
        self.assertEqual(str(lst), "[2 >< 3 >< 4 >< 0 >< 1]")
        lst.rotate(-3)
        self.assertEqual(str(lst), "[0 >< 1 >< 2 >< 3 >< 4]")
        lst.rotate(4)
        self.assertEqual(str(lst), "[1 >< 2 >< 3 >< 4 >< 0]")
        lst.rotate(-4)
        self.assertEqual(str(lst), "[0 >< 1 >< 2 >< 3 >< 4]")

    def test_reverse(self):
        # Reverse empty list.
        lst = DoublyLinkedList()
        lst.reverse()
        # Nothing hapened, but doesn't throw.
        self.assertEqual(str(lst), "[]")

        # Reverse one-element list.
        lst = DoublyLinkedList([0])
        lst.reverse()
        # Nothing happened, but doesn't throw.
        self.assertEqual(str(lst), "[0]")

        # Reverse two-elements list.
        lst = DoublyLinkedList([0, 1])
        lst.reverse()
        self.assertEqual(str(lst), "[1 >< 0]")

        # Reverse n-elements list.
        lst = DoublyLinkedList(list(range(5)))
        lst.reverse()
        self.assertEqual(str(lst), "[4 >< 3 >< 2 >< 1 >< 0]")

    def test_extend(self):
        test_cases = [
            (DoublyLinkedList(), DoublyLinkedList(), DoublyLinkedList()),
            (
                DoublyLinkedList(),
                DoublyLinkedList([0, 1, 2]),
                DoublyLinkedList([0, 1, 2]),
            ),
            (
                DoublyLinkedList([0, 1, 2]),
                DoublyLinkedList(),
                DoublyLinkedList([0, 1, 2]),
            ),
            (
                DoublyLinkedList([0, 1, 2]),
                DoublyLinkedList([3]),
                DoublyLinkedList([0, 1, 2, 3]),
            ),
            (
                DoublyLinkedList([0]),
                DoublyLinkedList([1, 2, 3]),
                DoublyLinkedList([0, 1, 2, 3]),
            ),
            (
                DoublyLinkedList([0, 1, 2]),
                DoublyLinkedList([3, 4, 5]),
                DoublyLinkedList([0, 1, 2, 3, 4, 5]),
            ),
        ]

        for lst1, lst2, expected_lst in test_cases:
            self.assertEqual(lst1.extend(lst2), expected_lst)

    def test_add(self):
        test_cases = [
            (DoublyLinkedList(), DoublyLinkedList(), DoublyLinkedList()),
            (
                DoublyLinkedList(),
                DoublyLinkedList([0, 1, 2]),
                DoublyLinkedList([0, 1, 2]),
            ),
            (
                DoublyLinkedList([0, 1, 2]),
                DoublyLinkedList(),
                DoublyLinkedList([0, 1, 2]),
            ),
            (
                DoublyLinkedList([0, 1, 2]),
                DoublyLinkedList([3]),
                DoublyLinkedList([0, 1, 2, 3]),
            ),
            (
                DoublyLinkedList([0]),
                DoublyLinkedList([1, 2, 3]),
                DoublyLinkedList([0, 1, 2, 3]),
            ),
            (
                DoublyLinkedList([0, 1, 2]),
                DoublyLinkedList([3, 4, 5]),
                DoublyLinkedList([0, 1, 2, 3, 4, 5]),
            ),
        ]

        for lst1, lst2, expected_lst in test_cases:
            self.assertEqual(lst1 + lst2, expected_lst)

    def test_selection_sort(self):
        test_cases = [
            (DoublyLinkedList(), "[]"),
            (DoublyLinkedList([1]), "[1]"),
            (DoublyLinkedList([1, 2, 3, 4, 5]), "[1 >< 2 >< 3 >< 4 >< 5]"),
            (DoublyLinkedList([5, 4, 3, 2, 1]), "[1 >< 2 >< 3 >< 4 >< 5]"),
            (DoublyLinkedList([2, 5, 3, 1, 4]), "[1 >< 2 >< 3 >< 4 >< 5]"),
            (
                DoublyLinkedList([1, 10, 100, -100, -10, -1]),
                "[-100 >< -10 >< -1 >< 1 >< 10 >< 100]",
            ),
        ]

        for lst, expected_output in test_cases:
            lst.selection_sort()
            self.check_doubly_linked_list_is_sorted(lst)
            self.assertEqual(str(lst), expected_output)

    def test_insertion_sort(self):
        test_cases = [
            (DoublyLinkedList(), "[]"),
            (DoublyLinkedList([1]), "[1]"),
            (DoublyLinkedList([1, 2, 3, 4, 5]), "[1 >< 2 >< 3 >< 4 >< 5]"),
            (DoublyLinkedList([5, 4, 3, 2, 1]), "[1 >< 2 >< 3 >< 4 >< 5]"),
            (DoublyLinkedList([2, 5, 3, 1, 4]), "[1 >< 2 >< 3 >< 4 >< 5]"),
            (
                DoublyLinkedList([1, 10, 100, -100, -10, -1]),
                "[-100 >< -10 >< -1 >< 1 >< 10 >< 100]",
            ),
        ]

        for lst, expected_output in test_cases:
            lst.insertion_sort()
            self.check_doubly_linked_list_is_sorted(lst)
            self.assertEqual(str(lst), expected_output)

    def test_quicksort(self):
        test_cases = [
            (DoublyLinkedList(), "[]"),
            (DoublyLinkedList([1]), "[1]"),
            (DoublyLinkedList([1, 2, 3, 4, 5]), "[1 >< 2 >< 3 >< 4 >< 5]"),
            (DoublyLinkedList([5, 4, 3, 2, 1]), "[1 >< 2 >< 3 >< 4 >< 5]"),
            (DoublyLinkedList([2, 5, 3, 1, 4]), "[1 >< 2 >< 3 >< 4 >< 5]"),
            (
                DoublyLinkedList([1, 10, 100, -100, -10, -1]),
                "[-100 >< -10 >< -1 >< 1 >< 10 >< 100]",
            ),
        ]

        for lst, expected_output in test_cases:
            lst.quicksort()
            self.check_doubly_linked_list_is_sorted(lst)
            self.assertEqual(str(lst), expected_output)

    def check_doubly_linked_list_is_sorted(self, lst: DoublyLinkedList):
        n = lst._hd
        while n is not None:
            self.assertTrue(n._nxt is None or n._v <= n._nxt._v)
            n = n._nxt


def main():
    unittest.main()


if __name__ == "__main__":
    main()
