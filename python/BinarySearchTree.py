from BinaryTree import BinaryTree, Node


class BinarySearchTree(BinaryTree):
    def __init__(self, root: Node | None = None) -> None:
        super().__init__(root)
        if not self.is_bst():
            raise Exception("Binary tree is not a binary search tree.")

    def __rec_lookup_rec(self, node: Node | None, key: int) -> Node | None:
        if node == None:
            return None
        elif node.val == key:
            return node
        elif key < node.val:
            return self.__rec_lookup_rec(node.left, key)
        else:
            return self.__rec_lookup_rec(node.right, key)

    def lookup_rec(self, key: int) -> Node | None:
        return self.__rec_lookup_rec(self._root, key)

    def lookup_it(self, key: int) -> Node | None:
        n = self._root
        while n != None:
            if n.val == key:
                return n
            elif key < n.val:
                n = n.left
            else:
                n = n.right

        return None

    def __rec_insert_rec(self, node: Node | None, key: int) -> Node | None:
        if node == None:
            node = Node(key, None, None)
        elif key == node.val:
            pass
        elif key < node.val:
            node.left = self.__rec_insert_rec(node.left, key)
        else:
            node.right = self.__rec_insert_rec(node.right, key)
        return node

    def insert_rec(self, key: int) -> "BinarySearchTree":
        self._root = self.__rec_insert_rec(self._root, key)
        return self

    def insert_it(self, key: int) -> "BinarySearchTree":
        if self._root == None:
            self._root = Node(key, None, None)
            return self

        n = self._root
        while n != None:
            if n.val == key:
                return self
            elif key < n.val:
                if n.left == None:
                    n.left = Node(key, None, None)
                    return self
                else:
                    n = n.left
            else:
                if n.right == None:
                    n.right = Node(key, None, None)
                    return self
                else:
                    n = n.right

        return self

    def __rec_remove(self, node: Node | None, key: int) -> Node | None:
        if node == None:
            return None
        elif key < node.val:
            node.left = self.__rec_remove(node.left, key)
            return node
        elif key > node.val:
            node.right = self.__rec_remove(node.right, key)
            return node
        # maintenant on sait que key == node.val, donc on cherche à supprimer node
        elif node.left == None and node.right == None:  # si leaf node
            return None
        elif node.right == None:  # no right branch
            return node.left
        elif node.left == None:  # no left branch
            return node.right
        elif node.left.right == None:  # predecessor is node.left
            node.left.right = node.right
            return node.left
        else:  # predecessor is further down the left subtree
            parent: Node = node.left
            pred: Node = node.left.right
            while pred.right != None:
                parent = pred
                pred = pred.right
            parent.right = pred.left
            pred.left = node.left
            pred.right = node.right
            return pred

    def remove(self, key: int) -> "BinarySearchTree":
        self._root = self.__rec_remove(self._root, key)
        return self

    @staticmethod
    def min(node: Node | None) -> Node | None:
        prev = node
        while node != None:
            prev = node
            node = node.left
        return prev

    @staticmethod
    def max(node: Node | None) -> Node | None:
        prev = node
        while node != None:
            prev = node
            node = node.right
        return prev

    # The successor of a node n in a bst (with all the keys distinct) is the node that has the smallest key greater than n's key.
    @staticmethod
    def successor(node: Node | None) -> Node | None:
        if node == None or node.right == None:
            return None
        else:
            return BinarySearchTree.min(node.right)

    # The predecessor of a node n in a bst (with all the keys distinct) is the node that has the largest key smaller than n's key.
    @staticmethod
    def predecessor(node: Node | None) -> Node | None:
        if node == None or node.left == None:
            return None
        else:
            return BinarySearchTree.max(node.left)

    @staticmethod
    def array_to_bst(nodes: list[int | None] = []) -> "BinarySearchTree":
        return BinarySearchTree(BinaryTree.array_to_bt(nodes).root())

    @staticmethod
    def bst_to_array(bst: "BinarySearchTree") -> list[int | None]:
        return BinaryTree.bt_to_array(bst)


if __name__ == "__main__":

    print("BinarySearchTree.lookup_rec", end="")
    expected = 6
    arr: list[int | None] = [5, 4, expected]
    bst = BinarySearchTree.array_to_bst(arr)
    node = bst.lookup_rec(expected)
    assert (
        node is not None and node.val == expected
    ), f"Expected node value to be {expected}, but got {node.val}"  # pyright: ignore [reportOptionalMemberAccess]
    node = bst.lookup_rec(10)
    assert node is None, "Expected node to be None."
    print(": tests passed!")

    print("BinarySearchTree.lookup_it", end="")
    expected = 6
    arr: list[int | None] = [5, 4, expected]
    bst = BinarySearchTree.array_to_bst(arr)
    node = bst.lookup_it(expected)
    assert (
        node is not None and node.val == expected
    ), f"Expected node value to be {expected}, but got {node.val}"  # pyright: ignore [reportOptionalMemberAccess]
    node = bst.lookup_it(10)
    assert node is None, "Expected node to be None."
    print(": tests passed!")

    print("BinarySearchTree.insert_rec", end="")
    arr: list[int | None] = [10, 5, 15]
    bst = BinarySearchTree.array_to_bst(arr)
    bst.insert_rec(3).insert_rec(7).insert_rec(12).insert_rec(17)
    expected_list: list[int | None] = [10, 5, 15, 3, 7, 12, 17]
    got = BinarySearchTree.bst_to_array(bst)
    assert got == expected_list, f"Expected {expected_list} to be equal to {got}."
    print(": tests passed!")

    print("BinarySearchTree.insert_it", end="")
    arr: list[int | None] = [10, 5, 15]
    bst = BinarySearchTree.array_to_bst(arr)
    bst.insert_it(3).insert_it(7).insert_it(12).insert_it(17)
    expected_list: list[int | None] = [10, 5, 15, 3, 7, 12, 17]
    got = BinarySearchTree.bst_to_array(bst)
    assert got == expected_list, f"Expected {expected_list} to be equal to {got}."
    print(": tests passed!")

    print("BinarySearchTree.remove", end="")
    q = 20
    v = 30
    u = 28
    w = 32
    s = 26
    r = 22
    t = 27
    bst = BinarySearchTree.array_to_bst(
        [
            q,
            None,
            v,
            None,
            None,
            u,
            w,
            None,
            None,
            None,
            None,
            s,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            r,
            t,
        ]
    )
    bst.remove(v)
    expected = BinarySearchTree.array_to_bst(
        [
            q,
            None,
            u,
            None,
            None,
            s,
            w,
            None,
            None,
            None,
            None,
            r,
            t,
        ]
    )
    assert bst.is_equal_to(expected), "Expected binary trees to be equal"
    print(": tests passed!")

    print("BinarySearchTree.min", end="")
    arr: list[int | None] = []
    bst = BinarySearchTree.array_to_bst(arr)
    node = BinarySearchTree.min(bst.root())
    assert node is None, f"Expected node to be None."
    arr: list[int | None] = [10, 5, 15, 3, 7, 12, 17]
    bst = BinarySearchTree.array_to_bst(arr)
    node = BinarySearchTree.min(bst.root())
    expected = 3
    assert (
        node is not None and node.val == expected
    ), f"Expected min to be {expected}, but got {node.val}"  # pyright: ignore [reportOptionalMemberAccess]
    print(": tests passed!")

    print("BinarySearchTree.max", end="")
    arr: list[int | None] = []
    bst = BinarySearchTree.array_to_bst(arr)
    node = BinarySearchTree.max(bst.root())
    assert node is None, f"Expected node to be None."
    arr: list[int | None] = [10, 5, 15, 3, 7, 12, 17]
    bst = BinarySearchTree.array_to_bst(arr)
    node = BinarySearchTree.max(bst.root())
    expected = 17
    assert (
        node is not None and node.val == expected
    ), f"Expected max to be {expected}, but got {node.val}"  # pyright: ignore [reportOptionalMemberAccess]
    print(": tests passed!")

    print("BinarySearchTree.predecessor", end="")
    arr: list[int | None] = []
    bst = BinarySearchTree.array_to_bst(arr)
    node = BinarySearchTree.predecessor(bst.root())
    assert node is None, f"Expected node to be None."
    arr: list[int | None] = [10, 5, 15, 3, 7, 12, 17]
    bst = BinarySearchTree.array_to_bst(arr)
    node = BinarySearchTree.predecessor(bst.root())
    expected = 7
    assert (
        node is not None and node.val == expected
    ), f"Expected predecessor to be {expected}, but got {node.val}"  # pyright: ignore [reportOptionalMemberAccess]
    print(": tests passed!")

    print("BinarySearchTree.successor", end="")
    arr: list[int | None] = []
    bst = BinarySearchTree.array_to_bst(arr)
    node = BinarySearchTree.successor(bst.root())
    assert node is None, f"Expected node to be None."
    arr: list[int | None] = [10, 5, 15, 3, 7, 12, 17]
    bst = BinarySearchTree.array_to_bst(arr)
    node = BinarySearchTree.successor(bst.root())
    expected = 12
    assert (
        node is not None and node.val == expected
    ), f"Expected successor to be {expected}, but got {node.val}"  # pyright: ignore [reportOptionalMemberAccess]
    print(": tests passed!")

    print("All tests passed!")
    pass
