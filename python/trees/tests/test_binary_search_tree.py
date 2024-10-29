import unittest

from trees import BSTree
from trees.binary_search_tree import BSTNode


class TestBSTree(unittest.TestCase):
    def test_init(self):
        bst = BSTree()
        self.assertFalse(bool(bst))
        self.assertTrue(bst.is_empty, 0)
        self.assertEqual(len(bst), 0)
        self.assertEqual(bst.size, 0)

    def test_insert(self):
        test_cases = [
            ([], 0),
            ([10], 1),
            ([10, 10, 10], 1),
            ([10, 5], 2),
            ([10, 10, 10, 5, 5, 5], 2),
            ([10, 5, 15], 3),
            ([10, 5, 15, 2], 4),
            ([10, 5, 15, 2, 8], 5),
            ([10, 5, 15, 2, 8, 12], 6),
            ([10, 5, 15, 2, 8, 12, 18], 7),
            ([1, 2, 3, 4, 5], 5),
            ([5, 4, 3, 2, 1], 5),
        ]

        for xs, expected_size in test_cases:
            bst = BSTree()
            for i in range(len(xs)):
                new_node = bst._insert_it(xs[i])
                self.assertEqual(new_node.k, xs[i])
            self.assertEqual(len(bst), expected_size)
            self.check_binary_search_tree_invariant(bst)

            bst = BSTree()
            for i in range(len(xs)):
                new_node = bst._insert_rec(xs[i])
                self.assertEqual(new_node.k, xs[i])
            self.assertEqual(len(bst), expected_size)
            self.check_binary_search_tree_invariant(bst)

    def test_get(self):
        test_cases = [
            (BSTree(), 0, False),
            (BSTree(), 1, False),
            (BSTree([10]), 0, False),
            (BSTree([10]), 1, False),
            (BSTree([10]), 10, True),
            (BSTree([10, 5]), 0, False),
            (BSTree([10, 5]), 1, False),
            (BSTree([10, 5]), 10, True),
            (BSTree([10, 5]), 5, True),
            (BSTree([10, 15]), 0, False),
            (BSTree([10, 15]), 1, False),
            (BSTree([10, 15]), 10, True),
            (BSTree([10, 15]), 15, True),
            (BSTree([10, 5, 15]), 0, False),
            (BSTree([10, 5, 15]), 1, False),
            (BSTree([10, 5, 15]), 10, True),
            (BSTree([10, 5, 15]), 5, True),
            (BSTree([10, 5, 15]), 15, True),
            (BSTree([10, 5, 15, 2, 8, 12, 18]), 0, False),
            (BSTree([10, 5, 15, 2, 8, 12, 18]), 10, True),
            (BSTree([10, 5, 15, 2, 8, 12, 18]), 5, True),
            (BSTree([10, 5, 15, 2, 8, 12, 18]), 15, True),
            (BSTree([10, 5, 15, 2, 8, 12, 18]), 2, True),
            (BSTree([10, 5, 15, 2, 8, 12, 18]), 8, True),
            (BSTree([10, 5, 15, 2, 8, 12, 18]), 12, True),
            (BSTree([10, 5, 15, 2, 8, 12, 18]), 18, True),
        ]

        for bst, k, expected_found in test_cases:
            node = bst._get_it(k)
            if expected_found:
                self.assertTrue(node.is_some and node.unwrap()._k == k)
            else:
                self.assertTrue(node.is_none)

    def test_delete(self):
        test_cases = [
            (BSTree(), 0, False, 0),
            (BSTree(), 1, False, 0),
            (BSTree([10]), 0, False, 1),
            (BSTree([10]), 1, False, 1),
            (BSTree([10]), 10, True, 0),
            (BSTree([10, 5]), 0, False, 2),
            (BSTree([10, 5]), 1, False, 2),
            (BSTree([10, 5]), 10, True, 1),
            (BSTree([10, 5]), 5, True, 1),
            (BSTree([10, 15]), 0, False, 2),
            (BSTree([10, 15]), 1, False, 2),
            (BSTree([10, 15]), 10, True, 1),
            (BSTree([10, 15]), 15, True, 1),
            (BSTree([10, 5, 15]), 0, False, 3),
            (BSTree([10, 5, 15]), 1, False, 3),
            (BSTree([10, 5, 15]), 10, True, 2),
            (BSTree([10, 5, 15]), 5, True, 2),
            (BSTree([10, 5, 15]), 15, True, 2),
            (BSTree([10, 5, 15, 2, 8, 12, 18]), 0, False, 7),
            (BSTree([10, 5, 15, 2, 8, 12, 18]), 10, True, 6),
            (BSTree([10, 5, 15, 2, 8, 12, 18]), 5, True, 6),
            (BSTree([10, 5, 15, 2, 8, 12, 18]), 15, True, 6),
            (BSTree([10, 5, 15, 2, 8, 12, 18]), 2, True, 6),
            (BSTree([10, 5, 15, 2, 8, 12, 18]), 8, True, 6),
            (BSTree([10, 5, 15, 2, 8, 12, 18]), 12, True, 6),
            (BSTree([10, 5, 15, 2, 8, 12, 18]), 18, True, 6),
        ]

        for bst, k, expected_deleted, expected_size in test_cases:
            deleted_node = bst._delete_it(k)

            if expected_deleted:
                self.assertTrue(deleted_node.is_some and deleted_node.unwrap().k == k)
            else:
                self.assertTrue(deleted_node.is_none)

            self.assertEqual(len(bst), expected_size)
            self.check_binary_search_tree_invariant(bst)

    def test_contains(self):
        bst1 = BSTree()
        bst2 = BSTree([10])
        bst3 = BSTree([10, 5, 15, 2, 8, 12, 18])
        bst4 = BSTree([1, 2, 3, 4, 5])
        bst5 = BSTree([5, 4, 3, 2, 1])

        test_cases = [
            (bst1, 0, False),
            (bst1, 1, False),
            (bst1, 2, False),
            (bst2, 0, False),
            (bst2, 1, False),
            (bst2, 2, False),
            (bst2, 10, True),
            (bst3, 0, False),
            (bst3, 1, False),
            (bst3, 11, False),
            (bst3, 21, False),
            (bst3, 10, True),
            (bst3, 5, True),
            (bst3, 15, True),
            (bst3, 2, True),
            (bst3, 8, True),
            (bst3, 12, True),
            (bst3, 18, True),
            (bst4, 0, False),
            (bst4, 6, False),
            (bst4, 1, True),
            (bst4, 2, True),
            (bst4, 3, True),
            (bst4, 4, True),
            (bst4, 5, True),
            (bst5, 0, False),
            (bst5, 6, False),
            (bst5, 5, True),
            (bst5, 4, True),
            (bst5, 3, True),
            (bst5, 2, True),
            (bst5, 1, True),
        ]

        for bst, k, expected_found in test_cases:
            self.assertEqual(bst._contains_it(k), expected_found)
            self.assertEqual(bst._contains_rec(k), expected_found)

    def check_binary_search_tree_invariant[T](self, bst: BSTree[T]):
        """
        Asserts that for each node in *bst*, all values in the left subtree are strictly inferior
        and all values in the right subtree are strictly superior.

        Parameters
        ----------
        bst
        """
        if bst._root is None:
            return
        self._check_binary_search_tree_invariant_helper(bst._root)

    def _check_binary_search_tree_invariant_helper[T](
        self, node: BSTNode[T], min: T | None = None, max: T | None = None
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


def main():
    unittest.main()


if __name__ == "__main__":
    main()
