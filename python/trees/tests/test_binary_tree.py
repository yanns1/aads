import unittest
from io import StringIO

from trees import BTree, DFTOrder


class TestBTree(unittest.TestCase):
    def test_init(self):
        bt = BTree()
        self.assertFalse(bool(bt))
        self.assertTrue(bt.is_empty)
        self.assertEqual(len(bt), 0)
        self.assertEqual(bt.size, 0)
        self.assertEqual(bt.height, -1)

    def test_size(self):
        bt0 = BTree()
        bt1 = BTree([1])
        bt2 = BTree([1, 2])
        bt3 = BTree([1, 2, 3])
        bt4 = BTree([1, 2, 3, 4])
        bt5 = BTree([1, 2, 3, 4, 5])
        bt6 = BTree([1, 2, 3, 4, 5, 6])
        bt7 = BTree([1, 2, 3, 4, 5, 6, 7])
        bt8 = BTree([1, 2, None, 3, None, None, None, 4])
        bt9 = BTree(
            [
                1,
                None,
                2,
                None,
                None,
                None,
                3,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                4,
            ]
        )
        test_cases = [
            (bt0, 0),
            (bt1, 1),
            (bt2, 2),
            (bt3, 3),
            (bt4, 4),
            (bt5, 5),
            (bt6, 6),
            (bt7, 7),
            (bt8, 4),
            (bt9, 4),
        ]

        for bt, expected_size in test_cases:
            self.assertEqual(bt.size, expected_size)
            self.assertEqual(len(bt), expected_size)

    def test_height(self):
        bt1 = BTree()
        bt2 = BTree([1])
        bt3 = BTree([1, None, 3])
        bt4 = BTree([1, 2, None])
        bt5 = BTree([1, 2, 3])
        bt6 = BTree([1, 2, None, 3, None, None, None, 4])
        bt7 = BTree(
            [
                1,
                None,
                2,
                None,
                None,
                None,
                3,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                4,
            ]
        )
        bt8 = BTree([1, 2, 3, 4, None, 5, None, 6, 7])
        test_cases = [
            (bt1, -1),
            (bt2, 0),
            (bt3, 1),
            (bt4, 1),
            (bt5, 1),
            (bt6, 3),
            (bt7, 3),
            (bt8, 3),
        ]

        for bt, expected_height in test_cases:
            self.assertEqual(bt.height, expected_height)

    def test_eq(self):
        test_cases = [
            (BTree(), BTree(), True),
            (BTree([0]), BTree([0]), True),
            (BTree(), BTree([0]), False),
            (BTree([0]), BTree(), False),
            (BTree(list(range(8))), BTree(list(range(8))), True),
            (BTree(), BTree(list(range(8))), False),
            (BTree(list(range(8))), BTree(), False),
            (BTree(list(range(5))), BTree(list(range(8))), False),
            (BTree(list(range(8))), BTree(list(range(5))), False),
        ]

        for bt1, bt2, expected_res in test_cases:
            self.assertEqual(bt1 == bt2, expected_res)

    def test_is_max_heap(self):
        test_cases = [
            (BTree(), True),
            (BTree([20]), True),
            (BTree([20, 10]), True),
            (BTree([20, 10, 15]), True),
            (BTree([20, 10, 15, 2, 7]), True),
            (BTree([20, 10, 15, None, None, 7, 12]), True),
            (BTree([20, 10, 15, 2, 8, 7, 12]), True),
            (BTree([10, 20]), False),
            (BTree([20, 10, 25]), False),
            (BTree([20, 10, 15, 2, 12]), False),
            (BTree([20, 10, 15, 2, 12]), False),
            (BTree([20, 10, 15, None, None, 12, 17]), False),
            (BTree([20, 10, 15, 2, 8, 12, 17]), False),
        ]

        for bt, expected_is_max_heap in test_cases:
            self.assertEqual(bt.is_max_heap, expected_is_max_heap)

    def test_is_min_heap(self):
        test_cases = [
            (BTree(), True),
            (BTree([0]), True),
            (BTree([0, 10]), True),
            (BTree([0, 10, 20]), True),
            (BTree([0, 10, 20, 30, 40]), True),
            (BTree([0, 10, 20, 30, None, None, 60]), True),
            (BTree([0, 10, 20, 30, 40, 50, 60]), True),
            (BTree([0, -10]), False),
            (BTree([0, 10, -20]), False),
            (BTree([0, 10, 20, -30]), False),
            (BTree([0, 10, 20, 30, -40]), False),
            (BTree([0, 10, 20, 30, 40, -50]), False),
            (BTree([0, 10, 20, 30, 40, 50, -60]), False),
        ]

        for bt, expected_is_min_heap in test_cases:
            self.assertEqual(bt.is_min_heap, expected_is_min_heap)

    def test_is_bst(self):
        test_cases = [
            (BTree(), True),
            (BTree([10]), True),
            (BTree([10, 5]), True),
            (BTree([10, 5, 15]), True),
            (BTree([10, 5, 15, 2]), True),
            (BTree([10, 5, 15, 2, 8]), True),
            (BTree([10, 5, 15, 2, 8, 12]), True),
            (BTree([10, 5, 15, 2, 8, 12, 18]), True),
            (BTree([10, 5, 15, None, 8, 12, 18]), True),
            (BTree([10, 5, 15, None, None, 12, 18]), True),
            (BTree([10, 5, 15, None, None, None, 18]), True),
            (BTree([10, 15]), False),
            (BTree([10, 5, 7]), False),
            (BTree([10, 5, 15, 7]), False),
            (BTree([10, 5, 15, 2, 3]), False),
            (BTree([10, 5, 15, 2, 7, 17]), False),
            (BTree([10, 5, 15, 2, 7, 12, 13]), False),
        ]

        for bt, expected_is_bst in test_cases:
            self.assertEqual(bt.is_bst, expected_is_bst)

    def test_is_complete(self):
        test_cases = [
            (BTree(), True),
            (BTree([10]), True),
            (BTree([10, None]), True),
            (BTree([10, None, None]), True),
            (BTree([10, 5]), True),
            (BTree([10, 5, 15]), True),
            (BTree([10, 5, None]), True),
            (BTree([10, None, 15]), False),
            (BTree([10, 5, 15, 2]), True),
            (BTree([10, 5, 15, 2, 8]), True),
            (BTree([10, 5, 15, 2, None]), True),
            (BTree([10, 5, 15, None, 8]), False),
            (BTree([10, 5, 15, 2, 8, 12]), True),
            (BTree([10, 5, 15, 2, 8, 12, 18]), True),
            (BTree([10, 5, 15, 2, None, None, None]), True),
            (BTree([10, 5, 15, 2, 8, None, None]), True),
            (BTree([10, 5, 15, 2, 8, 12, None]), True),
            (BTree([10, 5, 15, None, 8, 12, 18]), False),
            (BTree([10, 5, 15, None, None, 12, 18]), False),
            (BTree([10, 5, 15, None, None, None, 18]), False),
        ]

        for bt, expected_is_complete in test_cases:
            self.assertEqual(bt.is_complete, expected_is_complete)

    def test_lca(self):
        bt = BTree()
        res = bt.lca(0, 1)
        self.assertTrue(res.is_none)

        bt = BTree([0])
        res = bt.lca(-1, 1)
        self.assertTrue(res.is_none)

        bt = BTree([0])
        res = bt.lca(0, 1)
        self.assertTrue(res.is_some and res.unwrap() == 0)

        bt = BTree([10, 5, 15, 2, 8, 12, 18, 0, 4, 6, 9, 11, 14, 16, 20])
        res = bt.lca(-1, 1)
        self.assertTrue(res.is_none)
        res = bt.lca(5, 15)
        self.assertTrue(res.is_some and res.unwrap() == 10)
        res = bt.lca(2, 8)
        self.assertTrue(res.is_some and res.unwrap() == 5)
        res = bt.lca(12, 18)
        self.assertTrue(res.is_some and res.unwrap() == 15)
        res = bt.lca(0, 4)
        self.assertTrue(res.is_some and res.unwrap() == 2)
        res = bt.lca(6, 9)
        self.assertTrue(res.is_some and res.unwrap() == 8)
        res = bt.lca(11, 14)
        self.assertTrue(res.is_some and res.unwrap() == 12)
        res = bt.lca(16, 20)
        self.assertTrue(res.is_some and res.unwrap() == 18)
        res = bt.lca(10, 15)
        self.assertTrue(res.is_some and res.unwrap() == 10)
        res = bt.lca(5, 20)
        self.assertTrue(res.is_some and res.unwrap() == 10)
        res = bt.lca(11, 20)
        self.assertTrue(res.is_some and res.unwrap() == 15)

    def test_contains(self):
        test_cases = [
            (BTree(), 0, False),
            (BTree([0]), -1, False),
            (BTree([0]), 0, True),
            (BTree([0]), 1, False),
            (BTree([0, 1]), -1, False),
            (BTree([0, 1]), 0, True),
            (BTree([0, 1]), 1, True),
            (BTree([0, 1]), 2, False),
            (BTree([0, 1, 2]), -1, False),
            (BTree([0, 1, 2]), 0, True),
            (BTree([0, 1, 2]), 1, True),
            (BTree([0, 1, 2]), 2, True),
            (BTree([0, 1, 2]), 3, False),
        ]

        for bt, k, expected_res in test_cases:
            self.assertEqual(bt.contains(k), expected_res)

    def test_depth_first_pre_order_traversal(self):
        bt1 = BTree()
        bt2 = BTree([1])
        bt3 = BTree([1, None, 3])
        bt4 = BTree([1, 2, None])
        bt5 = BTree([1, 2, 3])
        bt6 = BTree([1, 2, None, 3, None, None, None, 4])
        bt7 = BTree(
            [
                1,
                None,
                2,
                None,
                None,
                None,
                3,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                4,
            ]
        )
        bt8 = BTree([1, 2, 3, 4, None, 5, None, 6, 7])

        test_cases = [
            (bt1, "", "", "", "", "", ""),
            (bt2, "1", "1", "1", "1", "1", "1"),
            (bt3, "1 3", "1 3", "3 1", "1 3", "3 1", "3 1"),
            (bt4, "1 2", "2 1", "2 1", "1 2", "1 2", "2 1"),
            (bt5, "1 2 3", "2 1 3", "2 3 1", "1 3 2", "3 1 2", "3 2 1"),
            (bt6, "1 2 3 4", "4 3 2 1", "4 3 2 1", "1 2 3 4", "1 2 3 4", "4 3 2 1"),
            (bt7, "1 2 3 4", "1 2 3 4", "4 3 2 1", "1 2 3 4", "4 3 2 1", "4 3 2 1"),
            (
                bt8,
                "1 2 4 6 7 3 5",
                "6 4 7 2 1 5 3",
                "6 7 4 2 5 3 1",
                "1 3 5 2 4 7 6",
                "3 5 1 2 7 4 6",
                "5 3 7 6 4 2 1",
            ),
        ]

        for (
            bt,
            expected_pre_order_res,
            expected_in_order_res,
            expected_post_order_res,
            expected_rev_pre_order_res,
            expected_rev_in_order_res,
            expected_rev_post_order_res,
        ) in test_cases:
            s = StringIO()
            bt.depth_first_traversal(
                lambda k: s.write(f"{k} "), order=DFTOrder.PRE_ORDER
            )
            self.assertEqual(s.getvalue().strip(), expected_pre_order_res)
            s = StringIO()
            bt.depth_first_traversal(
                lambda k: s.write(f"{k} "), order=DFTOrder.IN_ORDER
            )
            self.assertEqual(s.getvalue().strip(), expected_in_order_res)
            s = StringIO()
            bt.depth_first_traversal(
                lambda k: s.write(f"{k} "), order=DFTOrder.POST_ORDER
            )
            self.assertEqual(s.getvalue().strip(), expected_post_order_res)
            s = StringIO()
            bt.depth_first_traversal(
                lambda k: s.write(f"{k} "), order=DFTOrder.REVERSE_PRE_ORDER
            )
            self.assertEqual(s.getvalue().strip(), expected_rev_pre_order_res)
            s = StringIO()
            bt.depth_first_traversal(
                lambda k: s.write(f"{k} "), order=DFTOrder.REVERSE_IN_ORDER
            )
            self.assertEqual(s.getvalue().strip(), expected_rev_in_order_res)
            s = StringIO()
            bt.depth_first_traversal(
                lambda k: s.write(f"{k} "), order=DFTOrder.REVERSE_POST_ORDER
            )
            self.assertEqual(s.getvalue().strip(), expected_rev_post_order_res)

    def test_breadth_first_traversal(self):
        bt1 = BTree()
        bt2 = BTree([1])
        bt3 = BTree([1, None, 3])
        bt4 = BTree([1, 2, None])
        bt5 = BTree([1, 2, 3])
        bt6 = BTree([1, 2, None, 3, None, None, None, 4])
        bt7 = BTree(
            [
                1,
                None,
                2,
                None,
                None,
                None,
                3,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                4,
            ]
        )
        bt8 = BTree([1, 2, 3, 4, None, 5, None, 6, 7])
        test_cases = [
            (bt1, ""),
            (bt2, "1"),
            (bt3, "1 3"),
            (bt4, "1 2"),
            (bt5, "1 2 3"),
            (bt6, "1 2 3 4"),
            (bt7, "1 2 3 4"),
            (bt8, "1 2 3 4 5 6 7"),
        ]

        for bt, expected_result in test_cases:
            s = StringIO()
            bt.breadth_first_traversal(lambda k: s.write(f"{k} "))
            self.assertEqual(s.getvalue().strip(), expected_result)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
