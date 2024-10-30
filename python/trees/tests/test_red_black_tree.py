import unittest
from collections import deque

from trees import RBTree
from trees.red_black_tree import Color, RBTNode


class TestRBTree(unittest.TestCase):
    def test_init(self):
        rbt = RBTree()
        self.assertFalse(bool(rbt))
        self.assertTrue(rbt.is_empty)
        self.assertEqual(len(rbt), 0)
        self.assertEqual(rbt.size, 0)
        self.assertEqual(rbt.height, -1)

    def test_size(self):
        rbt1 = RBTree()
        rbt2 = RBTree([10])
        rbt3 = RBTree([10, 5])
        rbt4 = RBTree([10, 5, 15])
        rbt5 = RBTree([10, 5, 15, 2])
        rbt6 = RBTree([10, 5, 15, 2, 8])
        rbt7 = RBTree([10, 5, 15, 2, 8, 12])
        rbt8 = RBTree([10, 5, 15, 2, 8, 12, 18])
        rbt9 = RBTree([1, 2, 3, 4, 5])
        rbt10 = RBTree([5, 4, 3, 2, 1])

        test_cases = [
            (rbt1, 0),
            (rbt2, 1),
            (rbt3, 2),
            (rbt4, 3),
            (rbt5, 4),
            (rbt6, 5),
            (rbt7, 6),
            (rbt8, 7),
            (rbt9, 5),
            (rbt10, 5),
        ]

        for rbt, expected_size in test_cases:
            self.assertEqual(rbt.size, expected_size)
            self.assertEqual(len(rbt), expected_size)

    def test_height(self):
        rbt1 = RBTree()
        rbt2 = RBTree([10])
        rbt3 = RBTree([10, 5])
        rbt4 = RBTree([10, 5, 15])
        rbt5 = RBTree([10, 5, 15, 2, 12])
        rbt6 = RBTree([10, 5, 15, 2, 12, 8, 18])
        rbt7 = RBTree([1, 2, 3, 4, 5, 6, 7])
        rbt8 = RBTree([7, 6, 5, 4, 3, 2, 1])

        test_cases = [
            (rbt1, -1),
            (rbt2, 0),
            (rbt3, 1),
            (rbt4, 1),
            (rbt5, 2),
            (rbt6, 2),
            (rbt7, 3),
            (rbt8, 3),
        ]

        for rbt, expected_height in test_cases:
            self.assertEqual(rbt.height, expected_height)

    def test_insert(self):
        test_cases = [
            # No need to rebalance.
            # ---------------------
            ([], 0, []),
            ([10], 1, [True]),
            ([10, 10, 10], 1, [True, False, False]),
            ([10, 5], 2, [True] * 2),
            ([10, 10, 10, 5, 5, 5], 2, [True, False, False, True, False, False]),
            ([10, 5, 15], 3, [True] * 3),
            ([10, 5, 15, 2], 4, [True] * 4),
            ([10, 5, 15, 2, 8], 5, [True] * 5),
            ([10, 5, 15, 2, 8, 12], 6, [True] * 6),
            ([10, 5, 15, 2, 8, 12, 18], 7, [True] * 7),
            # Need to rebalance.
            # ------------------
            # Inputs that would lead to degenerate binary search trees.
            ([1, 2, 3, 4, 5], 5, [True] * 5),
            ([5, 4, 3, 2, 1], 5, [True] * 5),
            (list(range(16)), 16, [True] * 16),
            (list(reversed(range(16))), 16, [True] * 16),
            (list(range(32)), 32, [True] * 32),
            (list(reversed(range(32))), 32, [True] * 32),
            # Inputs for case where parent is red and uncle is red.
            ([10, 5, 15, 2], 4, [True] * 4),
            ([10, 5, 15, 7], 4, [True] * 4),
            ([10, 5, 15, 12], 4, [True] * 4),
            ([10, 5, 15, 17], 4, [True] * 4),
            ([10, 5, 15, 2, 7, 12, 17, 0, 4, 1], 10, [True] * 10),
            # Inputs for case where parent is red and uncle is None.
            ([10, 5, 15, 2, 12, 1], 6, [True] * 6),
            ([10, 5, 15, 2, 12, 4], 6, [True] * 6),
            ([10, 5, 15, 2, 12, 11], 6, [True] * 6),
            ([10, 5, 15, 2, 12, 14], 6, [True] * 6),
            # Inputs for case where parent is red and uncle is black.
            ([1, 2, 3, 4, 5, 6, 7], 7, [True] * 7),
            ([7, 6, 5, 4, 3, 2, 1], 7, [True] * 7),
        ]

        for xs, expected_size, inserted in test_cases:
            rbt = RBTree()
            for i in range(len(xs)):
                res = rbt._insert_it(xs[i])
                self.assertEqual(res, inserted[i])
            self.assertEqual(len(rbt), expected_size)
            self.check_red_black_tree_invariants(rbt)

    def test_delete(self):
        test_cases = [
            (RBTree(), 0, False, 0),
            # Deleted node has one child (simple case).
            (RBTree([10, 5]), 10, True, 1),
            (RBTree([10, 5, 15, 2, 12]), 2, True, 4),
            (RBTree([10, 5, 15, 7, 17]), 7, True, 4),
            (RBTree([10, 5, 15, 2, 12]), 12, True, 4),
            (RBTree([10, 5, 15, 7, 17]), 17, True, 4),
            # Deleted node has two children (simple case).
            (RBTree([10, 5, 15]), 10, True, 2),
            (RBTree([10, 5, 15, 2, 7, 12, 17]), 5, True, 6),
            (RBTree([10, 5, 15, 2, 7, 12, 17]), 15, True, 6),
            (
                RBTree([10, 5, 15, 2, 7, 12, 17, 0, 4, 6, 9, 11, 14, 16, 20]),
                5,
                True,
                14,
            ),
            (
                RBTree([10, 5, 15, 2, 7, 12, 17, 0, 4, 6, 9, 11, 14, 16, 20]),
                15,
                True,
                14,
            ),
            # Deleted node has no child and is root (simple case).
            (RBTree([10]), 0, False, 1),
            (RBTree([10]), 10, True, 0),
            # Deleted node has no child and is red (simple case).
            (RBTree([10, 5]), 5, True, 1),
            (RBTree([10, 15]), 15, True, 1),
            (RBTree([10, 5, 15, 2, 7, 12, 17]), 2, True, 6),
            (RBTree([10, 5, 15, 2, 7, 12, 17]), 7, True, 6),
            (RBTree([10, 5, 15, 2, 7, 12, 17]), 12, True, 6),
            (RBTree([10, 5, 15, 2, 7, 12, 17]), 17, True, 6),
            # Deleted node has no child and is black (difficult case).
            (RBTree([10, 5, 15]), 5, True, 2),
            (RBTree([10, 5, 15]), 15, True, 2),
            (RBTree([10, 5, 15, 2]), 15, True, 3),
            (RBTree([10, 5, 15, 7]), 15, True, 3),
            (RBTree([10, 5, 15, 2, 7]), 15, True, 4),
            (RBTree([10, 5, 15, 12]), 5, True, 3),
            (RBTree([10, 5, 15, 17]), 5, True, 3),
            (RBTree([10, 5, 15, 12, 17]), 5, True, 4),
            (RBTree([10, 5, 15, 12, 17, 11, 14, 16, 20]), 5, True, 8),
            (RBTree([10, 5, 15, 2, 7, 1, 4, 6, 9]), 15, True, 8),
        ]
        for rbt, k, expected_deleted, expected_size in test_cases:
            deleted = rbt._delete_it(k)
            self.assertEqual(deleted, expected_deleted)
            self.assertEqual(len(rbt), expected_size)
            self.check_red_black_tree_invariants(rbt)

    def test_contains(self):
        rbt1 = RBTree()
        rbt2 = RBTree([10])
        rbt3 = RBTree([10, 5, 15, 2, 8, 12, 18])
        rbt4 = RBTree([1, 2, 3, 4, 5])
        rbt5 = RBTree([5, 4, 3, 2, 1])

        test_cases = [
            (rbt1, 0, False),
            (rbt1, 1, False),
            (rbt1, 2, False),
            (rbt2, 0, False),
            (rbt2, 1, False),
            (rbt2, 2, False),
            (rbt2, 10, True),
            (rbt3, 0, False),
            (rbt3, 1, False),
            (rbt3, 11, False),
            (rbt3, 21, False),
            (rbt3, 10, True),
            (rbt3, 5, True),
            (rbt3, 15, True),
            (rbt3, 2, True),
            (rbt3, 8, True),
            (rbt3, 12, True),
            (rbt3, 18, True),
            (rbt4, 0, False),
            (rbt4, 6, False),
            (rbt4, 1, True),
            (rbt4, 2, True),
            (rbt4, 3, True),
            (rbt4, 4, True),
            (rbt4, 5, True),
            (rbt5, 0, False),
            (rbt5, 6, False),
            (rbt5, 5, True),
            (rbt5, 4, True),
            (rbt5, 3, True),
            (rbt5, 2, True),
            (rbt5, 1, True),
        ]

        for rbt, k, expected_found in test_cases:
            self.assertEqual(rbt._contains_it(k), expected_found)
            self.assertEqual(rbt._contains_rec(k), expected_found)

    def check_binary_search_tree_invariant[T](self, rbt: RBTree[T]):
        """
        Asserts that for each node in *rbt*, all values in the left subtree are strictly inferior
        and all values in the right subtree are strictly superior.

        Parameters
        ----------
        rbt
        """
        if rbt._root is None:
            return
        self._check_binary_search_tree_invariant_helper(rbt._root)

    def _check_binary_search_tree_invariant_helper[T](
        self, node: RBTNode[T], min: T | None = None, max: T | None = None
    ):
        """
        Asserts that for each node in the binary search tree with root *node*, all values in the left subtree
        are strictly inferior and all values in the right subtree are strictly superior, imposing all the values
        (including that of *node*) to be within `[min, max]`.

        Parameters
        ----------
        node
        min
            The minimum bound.
            Setting it to `None` is equivalent to the lowest possible value of type `T`.
        max
            The maximum bound.
            Setting it to `None` is equivalent to the largest possible value of type `T`.
        """
        if min is not None:
            self.assertEqual(node._k > min, True)  # type: ignore
        if max is not None:
            self.assertEqual(node._k < max, True)  # type: ignore

        if node.left is not None:
            self._check_binary_search_tree_invariant_helper(node.left, min, node._k)

        if node.right is not None:
            self._check_binary_search_tree_invariant_helper(node.right, node._k, max)

    def check_red_black_tree_invariants[T](self, rbt: RBTree[T]):
        """
        Asserts that *rbt* has the required invariants of a red-black tree:

        1. *rbt* is a binary search tree, so for each node in *rbt*, all values
           in the left subtree are strictly inferior and all values in the right
           subtree are strictly superior.
        2. A red node does not have a red child.
        3. Every path from a given node to any of its descendant NIL nodes goes
           through the same number of black nodes.

        Parameters
        ----------
        rbt
        """
        self.check_binary_search_tree_invariant(rbt)
        self.check_for_red_violations(rbt)
        self.check_for_black_violations(rbt)

    def check_for_red_violations[T](self, rbt: RBTree[T]):
        """
        Asserts that there is no red violation in *rbt*, i.e. that the following invariant holds:

            A red node does not have a red child.

        Parameter
        ----------
        rbt
        """
        if rbt._root is None:
            return

        q = deque([rbt._root])
        while q:
            node = q.popleft()

            # Assert that if node is red, its children are black.
            if node.c == Color.RED:
                if node.left is not None:
                    self.assertTrue(node.left.c == Color.BLACK)
                if node.right is not None:
                    self.assertTrue(node.right.c == Color.BLACK)

            if node.left is not None:
                q.append(node.left)
            if node.right is not None:
                q.append(node.right)

    def check_for_black_violations[T](self, rbt: RBTree[T]):
        """
        Asserts that there is no black violation in *rbt*, i.e. that the following invariant holds:

            Every path from a given node to any of its descendant NIL nodes goes
            through the same number of black nodes.

        Parameter
        ----------
        rbt
        """
        self._check_for_black_violations_rec(rbt._root)

    def _check_for_black_violations_rec[T](self, node: RBTNode[T] | None) -> int:
        """
        Computes the number of black nodes in paths from *node* to any NIL leaf,
        and asserts that this "black height" is the same for the left subtree
        and the right subtree of every node.
        This is equivalent to checking that there is no black violation.

        Parameters
        ----------
        node

        Returns
        -------
        `int`
        """
        if node is None:
            return 0

        lh = self._check_for_black_violations_rec(node.left)
        rh = self._check_for_black_violations_rec(node.right)
        self.assertEqual(lh, rh)

        return lh + (1 if node.c == Color.BLACK else 0)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
