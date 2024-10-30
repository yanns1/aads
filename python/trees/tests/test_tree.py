import unittest

from trees import LCRSNode


class TestTree(unittest.TestCase):
    def test_size(self):
        t1 = LCRSNode(0)

        t2 = LCRSNode(0)
        t2.left = LCRSNode(0)

        t3 = LCRSNode(0)
        t3.left = LCRSNode(0)
        t3.right = LCRSNode(0)

        t4 = LCRSNode(0)
        t4.left = LCRSNode(0)
        t4.left.left = LCRSNode(0)
        t4.left.left.left = LCRSNode(0)
        t4.left.left.left.left = LCRSNode(0)

        t5 = LCRSNode(0)
        t5.left = LCRSNode(0)
        t5.right = LCRSNode(0)
        t5.right.right = LCRSNode(0)
        t5.right.right.right = LCRSNode(0)

        t6 = LCRSNode(0)
        t6.left = LCRSNode(0)
        t6.left.right = LCRSNode(0)
        t6.left.left = LCRSNode(0)
        t6.left.left.right = LCRSNode(0)
        t6.left.left.left = LCRSNode(0)
        t6.left.left.left.right = LCRSNode(0)

        t7 = LCRSNode(0)
        t7.left = LCRSNode(0)
        t7.right = LCRSNode(0)
        t7.left.left = LCRSNode(0)
        t7.left.right = LCRSNode(0)
        t7.right.left = LCRSNode(0)
        t7.right.right = LCRSNode(0)

        test_cases = [(t1, 1), (t2, 2), (t3, 3), (t4, 5), (t5, 5), (t6, 7), (t7, 7)]

        for t, expected_size in test_cases:
            self.assertEqual(LCRSNode._size_it(t), expected_size)
            self.assertEqual(LCRSNode._size_rec(t), expected_size)

    def test_degree(self):
        node1 = LCRSNode(0)

        node2 = LCRSNode(0)
        node2.left = LCRSNode(0)

        node3 = LCRSNode(0)
        node3.left = LCRSNode(0)
        node3.left.right = LCRSNode(0)
        node3.left.right.right = LCRSNode(0)
        node3.left.right.right.right = LCRSNode(0)
        node3.left.right.right.right.right = LCRSNode(0)

        node4 = LCRSNode(0)
        node4.left = LCRSNode(0)
        node4.left.left = LCRSNode(0)
        node4.left.left.left = LCRSNode(0)

        node5 = LCRSNode(0)
        node5.left = LCRSNode(0)
        node5.left.right = LCRSNode(0)
        node5.left.left = LCRSNode(0)
        node5.left.left.right = LCRSNode(0)

        test_cases = [(node1, 0), (node2, 1), (node3, 5), (node4, 1), (node5, 2)]

        for node, expected_degree in test_cases:
            self.assertEqual(node.degree(), expected_degree)

    def test_is_leaf(self):
        node1 = LCRSNode(0)

        node2 = LCRSNode(0)
        node2.left = LCRSNode(0)

        node3 = LCRSNode(0)
        node3.right = LCRSNode(0)

        node4 = LCRSNode(0)
        node4.left = LCRSNode(0)
        node4.right = LCRSNode(0)

        test_cases = [(node1, True), (node2, False), (node3, True), (node4, False)]

        for node, expected_is_leaf in test_cases:
            self.assertEqual(node.is_leaf(), expected_is_leaf)

    def test_height(self):
        t0 = None

        t1 = LCRSNode(0)

        t2 = LCRSNode(0)
        t2.left = LCRSNode(0)

        t3 = LCRSNode(0)
        t3.left = LCRSNode(0)
        t3.right = LCRSNode(0)

        t3 = LCRSNode(0)
        t3.left = LCRSNode(0)
        t3.right = LCRSNode(0)
        t3.right.right = LCRSNode(0)
        t3.right.right.right = LCRSNode(0)

        t4 = LCRSNode(0)
        t4.left = LCRSNode(0)
        t4.left.left = LCRSNode(0)
        t4.left.left.left = LCRSNode(0)
        t4.left.left.left.left = LCRSNode(0)

        t5 = LCRSNode(0)
        t5.left = LCRSNode(0)
        t5.left.right = LCRSNode(0)
        t5.left.right.left = LCRSNode(0)
        t5.left.right.left.right = LCRSNode(0)
        t5.left.right.left.right.left = LCRSNode(0)

        t6 = LCRSNode(0)
        t6.left = LCRSNode(0)
        t6.left.right = LCRSNode(0)
        t6.left.right.left = LCRSNode(0)
        t6.left.right.left.right = LCRSNode(0)
        t6.left.right.left.right.left = LCRSNode(0)
        t6.left.left = LCRSNode(0)
        t6.left.left.left = LCRSNode(0)
        t6.left.left.left.left = LCRSNode(0)

        test_cases = [(t0, -1), (t1, 0), (t2, 1), 
                      (t3, 1), (t4, 4), (t5, 3), (t6, 4)
                      ]

        for t, expected_height in test_cases:
            self.assertEqual(LCRSNode.height(t), expected_height)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
