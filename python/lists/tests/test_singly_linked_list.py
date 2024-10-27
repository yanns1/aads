import unittest

from option import Option

from lists import SinglyLinkedList


class TestSinglyLinkedList(unittest.TestCase):
    def test_init(self):
        lst = SinglyLinkedList()
        self.assertEqual(len(lst), 0)
        self.assertTrue(lst.is_empty)
        self.assertFalse(bool(lst))

    def test_repr(self):
        test_cases = [
            (SinglyLinkedList(), "[]"),
            (SinglyLinkedList([0]), "[0]"),
            (SinglyLinkedList([0, 1, 2, 3, 4]), "[0 > 1 > 2 > 3 > 4]"),
        ]

        for lst, expected_repr in test_cases:
            self.assertEqual(str(lst), expected_repr)

    def test_len(self):
        test_cases = [
            (SinglyLinkedList(), 0),
            (SinglyLinkedList([0]), 1),
            (SinglyLinkedList([0, 1, 2, 3, 4]), 5),
            (SinglyLinkedList(list(range(100))), 100),
        ]

        for lst, expected_len in test_cases:
            self.assertEqual(len(lst), expected_len)

    def test_iter(self):
        els = list(range(5))
        lst = SinglyLinkedList(els)
        self.assertListEqual(list(lst), els)

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
        lst = SinglyLinkedList(list(range(5)))
        for n in range(5):
            output_node = lst.get_at_idx(n)
            self.assertFalse(output_node.is_none)
            self.assertEqual(output_node.unwrap().v, n)
        self.assertTrue(lst.get_at_idx(-2).is_none)
        last_node = lst.get_at_idx(-1)
        self.assertTrue(last_node.is_some and last_node.unwrap().v == 4)
        self.assertTrue(lst.get_at_idx(5).is_none)

    def test_get_by_val(self):
        lst = SinglyLinkedList(list(range(5)))
        for n in range(5):
            output_node = lst.get_by_val(n)
            self.assertFalse(output_node.is_none)
            self.assertEqual(output_node.unwrap().v, n)
        self.assertTrue(lst.get_at_idx(-2).is_none)
        last_node = lst.get_at_idx(-1)
        self.assertTrue(last_node.is_some and last_node.unwrap().v == 4)
        self.assertTrue(lst.get_at_idx(5).is_none)

    def test_getitem(self):
        lst = SinglyLinkedList(list(range(5)))
        for n in range(5):
            self.assertEqual(lst[n], n)
        self.assertEqual(lst[-1], 4)
        self.assertRaises(TypeError, lambda: lst["wrong key type"])
        self.assertRaises(IndexError, lambda: lst[-2])
        self.assertRaises(IndexError, lambda: lst[5])

    def test_set_at_idx(self):
        lst = SinglyLinkedList()
        set_node = lst.set_at_idx(0, 0)
        self.assertTrue(set_node.is_none)
        self.assertEqual(lst, SinglyLinkedList())

        lst = SinglyLinkedList([0])
        set_node = lst.set_at_idx(1, 1)
        self.assertTrue(set_node.is_none)
        self.assertEqual(lst, SinglyLinkedList([0]))
        set_node = lst.set_at_idx(-2, 1)
        self.assertTrue(set_node.is_none)
        self.assertEqual(lst, SinglyLinkedList([0]))
        set_node = lst.set_at_idx(-1, 1)
        self.assertTrue(set_node.is_some and set_node.unwrap().v == 1)
        self.assertEqual(lst, SinglyLinkedList([1]))
        set_node = lst.set_at_idx(0, 2)
        self.assertTrue(set_node.is_some and set_node.unwrap().v == 2)
        self.assertEqual(lst, SinglyLinkedList([2]))

        lst = SinglyLinkedList([0, 1, 2])
        set_node = lst.set_at_idx(3, 3)
        self.assertTrue(set_node.is_none)
        self.assertEqual(lst, SinglyLinkedList([0, 1, 2]))
        set_node = lst.set_at_idx(-2, -2)
        self.assertTrue(set_node.is_none)
        self.assertEqual(lst, SinglyLinkedList([0, 1, 2]))
        set_node = lst.set_at_idx(0, 3)
        self.assertTrue(set_node.is_some and set_node.unwrap().v == 3)
        self.assertEqual(lst, SinglyLinkedList([3, 1, 2]))
        set_node = lst.set_at_idx(1, 4)
        self.assertTrue(set_node.is_some and set_node.unwrap().v == 4)
        self.assertEqual(lst, SinglyLinkedList([3, 4, 2]))
        set_node = lst.set_at_idx(2, 5)
        self.assertTrue(set_node.is_some and set_node.unwrap().v == 5)
        self.assertEqual(lst, SinglyLinkedList([3, 4, 5]))
        set_node = lst.set_at_idx(-1, 6)
        self.assertTrue(set_node.is_some and set_node.unwrap().v == 6)
        self.assertEqual(lst, SinglyLinkedList([3, 4, 6]))

    def test_set_by_val(self):
        lst = SinglyLinkedList()
        set_node = lst.set_by_val(0, 1)
        self.assertTrue(set_node.is_none)
        self.assertEqual(lst, SinglyLinkedList())

        lst = SinglyLinkedList([0])
        set_node = lst.set_by_val(1, 2)
        self.assertTrue(set_node.is_none)
        self.assertEqual(lst, SinglyLinkedList([0]))
        set_node = lst.set_by_val(-1, -2)
        self.assertTrue(set_node.is_none)
        self.assertEqual(lst, SinglyLinkedList([0]))
        set_node = lst.set_by_val(0, 1)
        self.assertTrue(set_node.is_some and set_node.unwrap().v == 1)
        self.assertEqual(lst, SinglyLinkedList([1]))
        set_node = lst.set_by_val(1, 2)
        self.assertTrue(set_node.is_some and set_node.unwrap().v == 2)
        self.assertEqual(lst, SinglyLinkedList([2]))

        lst = SinglyLinkedList([0, 1, 2])
        set_node = lst.set_by_val(3, 4)
        self.assertTrue(set_node.is_none)
        self.assertEqual(lst, SinglyLinkedList([0, 1, 2]))
        set_node = lst.set_by_val(-2, -3)
        self.assertTrue(set_node.is_none)
        self.assertEqual(lst, SinglyLinkedList([0, 1, 2]))
        set_node = lst.set_by_val(0, 3)
        self.assertTrue(set_node.is_some and set_node.unwrap().v == 3)
        self.assertEqual(lst, SinglyLinkedList([3, 1, 2]))
        set_node = lst.set_by_val(1, 4)
        self.assertTrue(set_node.is_some and set_node.unwrap().v == 4)
        self.assertEqual(lst, SinglyLinkedList([3, 4, 2]))
        set_node = lst.set_by_val(2, 5)
        self.assertTrue(set_node.is_some and set_node.unwrap().v == 5)
        self.assertEqual(lst, SinglyLinkedList([3, 4, 5]))

    def test_setitem(self):
        lst = SinglyLinkedList()

        def f1():
            lst[0] = 0

        self.assertRaises(IndexError, f1)
        self.assertEqual(lst, SinglyLinkedList())

        lst = SinglyLinkedList([0])

        def f2():
            lst[1] = 1

        self.assertRaises(IndexError, f2)
        self.assertEqual(lst, SinglyLinkedList([0]))

        def f3():
            lst[-2] = -2

        self.assertRaises(IndexError, f3)
        self.assertEqual(lst, SinglyLinkedList([0]))
        lst[-1] = 1
        self.assertEqual(lst, SinglyLinkedList([1]))
        lst[0] = 2
        self.assertEqual(lst, SinglyLinkedList([2]))

        lst = SinglyLinkedList([0, 1, 2])

        def f4():
            lst[3] = 3

        self.assertRaises(IndexError, f4)
        self.assertEqual(lst, SinglyLinkedList([0, 1, 2]))

        def f5():
            lst[-2] = 2

        self.assertRaises(IndexError, f5)
        self.assertEqual(lst, SinglyLinkedList([0, 1, 2]))
        lst[0] = 3
        self.assertEqual(lst, SinglyLinkedList([3, 1, 2]))
        lst[1] = 4
        self.assertEqual(lst, SinglyLinkedList([3, 4, 2]))
        lst[2] = 5
        self.assertEqual(lst, SinglyLinkedList([3, 4, 5]))
        lst[-1] = 6
        self.assertEqual(lst, SinglyLinkedList([3, 4, 6]))

    def test_insert(self):
        # Insert in empty list.
        lst = SinglyLinkedList()
        new_node = lst.insert(0, Option.NONE())
        self.assertEqual(new_node._v, 0)
        self.assertFalse(lst.is_empty)
        self.assertEqual(len(lst), 1)
        self.assertEqual(str(lst), "[0]")

        # Insert in n-elements list...
        lst = SinglyLinkedList(list(range(5)))
        # ... at the beginning
        new_node = lst.insert(-1, Option.NONE())
        self.assertEqual(new_node._v, -1)
        self.assertEqual(len(lst), 6)
        self.assertEqual(str(lst), "[-1 > 0 > 1 > 2 > 3 > 4]")
        # ... in the middle
        neighbor = new_node._nxt._nxt  # type: ignore
        new_node = lst.insert(10, Option.Some(neighbor))
        self.assertEqual(new_node._v, 10)
        self.assertEqual(len(lst), 7)
        self.assertEqual(str(lst), "[-1 > 0 > 1 > 10 > 2 > 3 > 4]")
        # ... at the end
        neighbor = new_node._nxt._nxt._nxt  # type: ignore
        new_node = lst.insert(5, Option.Some(neighbor))
        self.assertEqual(new_node._v, 5)
        self.assertEqual(len(lst), 8)
        self.assertEqual(str(lst), "[-1 > 0 > 1 > 10 > 2 > 3 > 4 > 5]")

    def test_insert_at_idx(self):
        lst = SinglyLinkedList()

        # prepend
        for n in range(1, 4):
            new_node = lst.insert_at_idx(0, -n)
            self.assertTrue(new_node.is_some)
            self.assertEqual(new_node.unwrap()._v, -n)

        # append
        for n in range(1, 4):
            new_node = lst.insert_at_idx(len(lst), n)
            self.assertTrue(new_node.is_some)
            self.assertEqual(new_node.unwrap()._v, n)

        # insert in the middle
        new_node = lst.insert_at_idx(3, 0)
        self.assertTrue(new_node.is_some)
        self.assertEqual(new_node.unwrap()._v, 0)

        new_node = lst.insert_at_idx(1, -10)
        self.assertTrue(new_node.is_some)
        self.assertEqual(new_node.unwrap()._v, -10)

        new_node = lst.insert_at_idx(len(lst) - 1, 10)
        self.assertTrue(new_node.is_some)
        self.assertEqual(new_node.unwrap()._v, 10)

        # insert out of bounds
        new_node = lst.insert_at_idx(-2, -100)
        self.assertTrue(new_node.is_none)

        new_node = lst.insert_at_idx(len(lst) + 1, 100)
        self.assertTrue(new_node.is_none)

        self.assertFalse(lst.is_empty)
        self.assertEqual(len(lst), 9)
        self.assertEqual(str(lst), "[-3 > -10 > -2 > -1 > 0 > 1 > 2 > 10 > 3]")

    def test_append(self):
        lst = SinglyLinkedList()
        for n in range(5):
            new_node = lst.append(n)
            self.assertEqual(new_node._v, n)

        self.assertFalse(lst.is_empty)
        self.assertEqual(len(lst), 5)
        self.assertEqual(str(lst), "[0 > 1 > 2 > 3 > 4]")

    def test_prepend(self):
        lst = SinglyLinkedList()
        for n in range(5):
            new_node = lst.prepend(n)
            self.assertEqual(new_node._v, n)

        self.assertFalse(lst.is_empty)
        self.assertEqual(len(lst), 5)
        self.assertEqual(str(lst), "[4 > 3 > 2 > 1 > 0]")

    def test_delete(self):
        # One-element list
        lst = SinglyLinkedList()
        new_node = lst.prepend(0)
        lst.delete(new_node)
        self.assertEqual(lst.is_empty, True)
        self.assertEqual(len(lst), 0)
        self.assertEqual(str(lst), "[]")

        # N-elements list
        lst = SinglyLinkedList(list(range(5)))

        # delete at the beginning
        hd = lst.get_at_idx(0).unwrap()
        lst.delete(hd)
        self.assertEqual(len(lst), 4)
        self.assertEqual(str(lst), "[1 > 2 > 3 > 4]")

        # delete in the middle
        node = lst.get_at_idx(1).unwrap()
        lst.delete(node)
        self.assertEqual(len(lst), 3)
        self.assertEqual(str(lst), "[1 > 3 > 4]")

        # delete at the ned
        tl = lst.get_at_idx(len(lst) - 1).unwrap()
        lst.delete(tl)
        self.assertEqual(len(lst), 2)
        self.assertEqual(str(lst), "[1 > 3]")

    def test_delete_at_idx(self):
        lst = SinglyLinkedList(list(range(5)))

        # delete out of bounds
        deleted_node = lst.delete_at_idx(-2)
        self.assertTrue(deleted_node.is_none)
        self.assertEqual(len(lst), 5)
        self.assertEqual(str(lst), "[0 > 1 > 2 > 3 > 4]")

        deleted_node = lst.delete_at_idx(5)
        self.assertTrue(deleted_node.is_none)
        self.assertEqual(len(lst), 5)
        self.assertEqual(str(lst), "[0 > 1 > 2 > 3 > 4]")

        # delete at the beginning
        deleted_node = lst.delete_at_idx(0)
        self.assertTrue(deleted_node.is_some)
        self.assertEqual(deleted_node.unwrap()._v, 0)
        self.assertEqual(len(lst), 4)
        self.assertEqual(str(lst), "[1 > 2 > 3 > 4]")

        # delete in the middle
        deleted_node = lst.delete_at_idx(2)
        self.assertTrue(deleted_node.is_some)
        self.assertEqual(deleted_node.unwrap()._v, 3)
        self.assertEqual(len(lst), 3)
        self.assertEqual(str(lst), "[1 > 2 > 4]")

        deleted_node = lst.delete_at_idx(1)
        self.assertTrue(deleted_node.is_some)
        self.assertEqual(deleted_node.unwrap()._v, 2)
        self.assertEqual(len(lst), 2)
        self.assertEqual(str(lst), "[1 > 4]")

        # delete at the end
        deleted_node = lst.delete_at_idx(len(lst) - 1)
        self.assertTrue(deleted_node.is_some)
        self.assertEqual(deleted_node.unwrap()._v, 4)
        self.assertEqual(len(lst), 1)
        self.assertEqual(str(lst), "[1]")

    def test_delete_by_val(self):
        lst = SinglyLinkedList(list(range(5)))

        # delete inexistant values
        deleted_node = lst.delete_by_val(-1)
        self.assertTrue(deleted_node.is_none)
        self.assertEqual(len(lst), 5)
        self.assertEqual(str(lst), "[0 > 1 > 2 > 3 > 4]")

        deleted_node = lst.delete_by_val(5)
        self.assertTrue(deleted_node.is_none)
        self.assertEqual(len(lst), 5)
        self.assertEqual(str(lst), "[0 > 1 > 2 > 3 > 4]")

        # delete at the beginning
        deleted_node = lst.delete_by_val(0)
        self.assertTrue(deleted_node.is_some)
        self.assertEqual(deleted_node.unwrap()._v, 0)
        self.assertEqual(len(lst), 4)
        self.assertEqual(str(lst), "[1 > 2 > 3 > 4]")

        # delete in the middle
        deleted_node = lst.delete_by_val(3)
        self.assertTrue(deleted_node.is_some)
        self.assertEqual(deleted_node.unwrap()._v, 3)
        self.assertEqual(len(lst), 3)
        self.assertEqual(str(lst), "[1 > 2 > 4]")

        deleted_node = lst.delete_by_val(2)
        self.assertTrue(deleted_node.is_some)
        self.assertEqual(deleted_node.unwrap()._v, 2)
        self.assertEqual(len(lst), 2)
        self.assertEqual(str(lst), "[1 > 4]")

        # delete at the end
        deleted_node = lst.delete_by_val(4)
        self.assertTrue(deleted_node.is_some)
        self.assertEqual(deleted_node.unwrap()._v, 4)
        self.assertEqual(len(lst), 1)
        self.assertEqual(str(lst), "[1]")

    def test_delitem(self):
        lst = SinglyLinkedList(list(range(5)))

        def f1():
            del lst[-2]

        self.assertRaises(IndexError, f1)

        def f2():
            del lst[len(lst)]

        self.assertRaises(IndexError, f2)

        del lst[0]
        self.assertEqual(str(lst), "[1 > 2 > 3 > 4]")

        del lst[-1]
        self.assertEqual(str(lst), "[1 > 2 > 3]")

        del lst[1]
        self.assertEqual(str(lst), "[1 > 3]")

    def test_extend(self):
        test_cases = [
            (SinglyLinkedList(), SinglyLinkedList(), SinglyLinkedList()),
            (
                SinglyLinkedList(),
                SinglyLinkedList([0, 1, 2]),
                SinglyLinkedList([0, 1, 2]),
            ),
            (
                SinglyLinkedList([0, 1, 2]),
                SinglyLinkedList(),
                SinglyLinkedList([0, 1, 2]),
            ),
            (
                SinglyLinkedList([0, 1, 2]),
                SinglyLinkedList([3]),
                SinglyLinkedList([0, 1, 2, 3]),
            ),
            (
                SinglyLinkedList([0]),
                SinglyLinkedList([1, 2, 3]),
                SinglyLinkedList([0, 1, 2, 3]),
            ),
            (
                SinglyLinkedList([0, 1, 2]),
                SinglyLinkedList([3, 4, 5]),
                SinglyLinkedList([0, 1, 2, 3, 4, 5]),
            ),
        ]

        for lst1, lst2, expected_lst in test_cases:
            self.assertEqual(lst1.extend(lst2), expected_lst)

    def test_add(self):
        test_cases = [
            (SinglyLinkedList(), SinglyLinkedList(), SinglyLinkedList()),
            (
                SinglyLinkedList(),
                SinglyLinkedList([0, 1, 2]),
                SinglyLinkedList([0, 1, 2]),
            ),
            (
                SinglyLinkedList([0, 1, 2]),
                SinglyLinkedList(),
                SinglyLinkedList([0, 1, 2]),
            ),
            (
                SinglyLinkedList([0, 1, 2]),
                SinglyLinkedList([3]),
                SinglyLinkedList([0, 1, 2, 3]),
            ),
            (
                SinglyLinkedList([0]),
                SinglyLinkedList([1, 2, 3]),
                SinglyLinkedList([0, 1, 2, 3]),
            ),
            (
                SinglyLinkedList([0, 1, 2]),
                SinglyLinkedList([3, 4, 5]),
                SinglyLinkedList([0, 1, 2, 3, 4, 5]),
            ),
        ]

        for lst1, lst2, expected_lst in test_cases:
            self.assertEqual(lst1 + lst2, expected_lst)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
