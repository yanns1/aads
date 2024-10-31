import unittest

from option import Option

from trees import BinaryMaxHeap, BinaryMinHeap, Item


class TestBinaryMinHeap(unittest.TestCase):
    def test_init(self):
        bh = BinaryMinHeap()
        self.assertFalse(bool(bh))
        self.assertTrue(bh.is_empty)
        self.assertEqual(bh.size, 0)
        self.assertEqual(len(bh), 0)

    def test_size(self):
        test_cases = [
            (BinaryMinHeap(), 0),
            (BinaryMinHeap([(0, 0)]), 1),
            (BinaryMinHeap([(0, 0), (1, 1), (2, 2)]), 3),
            (BinaryMinHeap(list(zip(range(20), range(20)))), 20),
        ]

        for bh, expected_size in test_cases:
            self.assertEqual(bh.size, expected_size)
            self.assertEqual(len(bh), expected_size)

    def test_iter(self):
        test_cases = [
            ([],),
            ([0],),
            ([0, 1, 2],),
            ([2, 1, 0],),
            ([2, 4, 3, 1, 5],),
            ([7, 12, 6, 27, 29, 57, 4, 43],),
        ]

        for (xs,) in test_cases:
            items = [item for item in BinaryMinHeap(list(zip(xs, xs)))]
            sorted_xs = sorted(xs)
            expected_items = list(
                map(lambda t: Item(t[0], t[1]), zip(sorted_xs, sorted_xs))
            )
            self.assertListEqual(items, expected_items)

    def test_push_pop(self):
        test_cases = [
            ([],),
            ([0],),
            ([0, 1, 2],),
            ([2, 1, 0],),
            ([2, 4, 3, 1, 5],),
            ([7, 12, 6, 27, 29, 57, 4, 43],),
        ]

        for (xs,) in test_cases:
            bh = BinaryMinHeap()
            for x in xs:
                bh.push(Item(x, x))
                self.check_min_heap_invariant(bh)
            self.assertEqual(len(bh), len(xs))

            sorted_xs = sorted(xs)
            expected_items = list(
                map(lambda t: Item(t[0], t[1]), zip(sorted_xs, sorted_xs))
            )
            items = []
            for _ in range(len(xs)):
                item = bh.pop()
                self.check_min_heap_invariant(bh)
                self.assertTrue(item.is_some)
                items.append(item.unwrap())
            self.assertListEqual(items, expected_items)

    def test_peek(self):
        test_cases = [
            ([],),
            ([0],),
            ([0, 1, 2],),
            ([2, 1, 0],),
            ([2, 4, 3, 1, 5],),
            ([7, 12, 6, 27, 29, 57, 4, 43],),
        ]

        for (xs,) in test_cases:
            bh = BinaryMinHeap(list(zip(xs, xs)))
            expected_size = bh.size
            expected_res = Option.Some(Item(min(xs), min(xs))) if xs else Option.NONE()

            self.assertEqual(bh.peek(), expected_res)
            self.assertEqual(bh.size, expected_size)
            self.check_min_heap_invariant(bh)

    def test_delete(self):
        test_cases = [
            ([], 0, 0),
            ([0], 0, 0),
            ([0], 1, 1),
            ([0, 1, 2], 0, 2),
            ([0, 1, 2], 1, 2),
            ([0, 1, 2], 2, 2),
            ([0, 1, 2], 3, 3),
            ([2, 1, 0], 2, 2),
            ([2, 1, 0], 1, 2),
            ([2, 1, 0], 0, 2),
            ([2, 1, 0], 3, 3),
            ([2, 4, 3, 1, 5], 2, 4),
            ([2, 4, 3, 1, 5], 4, 4),
            ([2, 4, 3, 1, 5], 3, 4),
            ([2, 4, 3, 1, 5], 1, 4),
            ([2, 4, 3, 1, 5], 5, 4),
            ([2, 4, 3, 1, 5], 6, 5),
        ]

        for xs, el_to_del, expected_size in test_cases:
            bh = BinaryMinHeap(list(zip(xs, xs)))
            bh.delete(el_to_del)
            self.check_min_heap_invariant(bh)
            self.assertEqual(len(bh), expected_size)

    def check_min_heap_invariant(self, bh: BinaryMinHeap):
        n = len(bh._arr)
        for i in range(n):
            i1, i2 = BinaryMinHeap._children_idxs(i)
            if i1 < n:
                self.assertTrue(bh._arr[i].k <= bh._arr[i1].k)
            if i2 < n:
                self.assertTrue(bh._arr[i].k <= bh._arr[i2].k)


class TestBinaryMaxHeap(unittest.TestCase):
    def test_init(self):
        bh = BinaryMaxHeap()
        self.assertFalse(bool(bh))
        self.assertTrue(bh.is_empty)
        self.assertEqual(bh.size, 0)
        self.assertEqual(len(bh), 0)

    def test_size(self):
        test_cases = [
            (BinaryMaxHeap(), 0),
            (BinaryMaxHeap([(0, 0)]), 1),
            (BinaryMaxHeap([(0, 0), (1, 1), (2, 2)]), 3),
            (BinaryMaxHeap(list(zip(range(20), range(20)))), 20),
        ]

        for bh, expected_size in test_cases:
            self.assertEqual(bh.size, expected_size)
            self.assertEqual(len(bh), expected_size)

    def test_iter(self):
        test_cases = [
            ([],),
            ([0],),
            ([0, 1, 2],),
            ([2, 1, 0],),
            ([2, 4, 3, 1, 5],),
            ([7, 12, 6, 27, 29, 57, 4, 43],),
        ]

        for (xs,) in test_cases:
            items = [item for item in BinaryMaxHeap(list(zip(xs, xs)))]
            sorted_xs = sorted(xs, reverse=True)
            expected_items = list(
                map(lambda t: Item(t[0], t[1]), zip(sorted_xs, sorted_xs))
            )
            self.assertListEqual(items, expected_items)

    def test_push_pop(self):
        test_cases = [
            ([],),
            ([0],),
            ([0, 1, 2],),
            ([2, 1, 0],),
            ([2, 4, 3, 1, 5],),
            ([7, 12, 6, 27, 29, 57, 4, 43],),
        ]

        for (xs,) in test_cases:
            bh = BinaryMaxHeap()
            for x in xs:
                bh.push(Item(x, x))
                self.check_max_heap_invariant(bh)
            self.assertEqual(len(bh), len(xs))

            sorted_xs = sorted(xs, reverse=True)
            expected_items = list(
                map(lambda t: Item(t[0], t[1]), zip(sorted_xs, sorted_xs))
            )
            items = []
            for _ in range(len(xs)):
                item = bh.pop()
                self.check_max_heap_invariant(bh)
                self.assertTrue(item.is_some)
                items.append(item.unwrap())
            self.assertListEqual(items, expected_items)

    def test_peek(self):
        test_cases = [
            ([],),
            ([0],),
            ([0, 1, 2],),
            ([2, 1, 0],),
            ([2, 4, 3, 1, 5],),
            ([7, 12, 6, 27, 29, 57, 4, 43],),
        ]

        for (xs,) in test_cases:
            bh = BinaryMaxHeap(list(zip(xs, xs)))
            expected_size = bh.size
            expected_res = Option.Some(Item(max(xs), max(xs))) if xs else Option.NONE()

            self.assertEqual(bh.peek(), expected_res)
            self.assertEqual(bh.size, expected_size)
            self.check_max_heap_invariant(bh)

    def test_delete(self):
        test_cases = [
            ([], 0, 0),
            ([0], 0, 0),
            ([0], 1, 1),
            ([0, 1, 2], 0, 2),
            ([0, 1, 2], 1, 2),
            ([0, 1, 2], 2, 2),
            ([0, 1, 2], 3, 3),
            ([2, 1, 0], 2, 2),
            ([2, 1, 0], 1, 2),
            ([2, 1, 0], 0, 2),
            ([2, 1, 0], 3, 3),
            ([2, 4, 3, 1, 5], 2, 4),
            ([2, 4, 3, 1, 5], 4, 4),
            ([2, 4, 3, 1, 5], 3, 4),
            ([2, 4, 3, 1, 5], 1, 4),
            ([2, 4, 3, 1, 5], 5, 4),
            ([2, 4, 3, 1, 5], 6, 5),
        ]

        for xs, el_to_del, expected_size in test_cases:
            bh = BinaryMaxHeap(list(zip(xs, xs)))
            bh.delete(el_to_del)
            self.check_max_heap_invariant(bh)
            self.assertEqual(len(bh), expected_size)

    def check_max_heap_invariant(self, bh: BinaryMaxHeap):
        n = len(bh._arr)
        for i in range(n):
            i1, i2 = BinaryMaxHeap._children_idxs(i)
            if i1 < n:
                self.assertTrue(bh._arr[i].k >= bh._arr[i1].k)
            if i2 < n:
                self.assertTrue(bh._arr[i].k >= bh._arr[i2].k)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
