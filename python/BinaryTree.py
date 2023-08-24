from typing import Callable

# ===============================================================================
# TREE TRAVERSAL: NOTES
# ===============================================================================
# Il y a plusieurs manières de traverser un arbre, càd visiter chaque noeud de l'arbre exactement une fois. Traverser/parcourir (au moins partiellement) un arbre est nécessaire pour trouver un élément en particulier, pour supprimer un élément, pour modifier un élément, etc.) Les manières les plus connues sont:
#       1) pre-order search/traversal/walk (NLR)
#       2) in-order search/traversal/walk (LNR)
#       3) post-order search/traversal/walk (LRN)
#       4) breadth-first search (or BFS for short)
# Les trois premières manières sont qualifiées de "depth-first search (DFS)" par opposition à "breadth-first search" car pour un noeud donné, on commence par visiter un enfant (descendre en profondeur) plutôt que de visiter un noeud voisin (explorer la largeur avant de poursuivre la descente).
# Ces algorithmes de parcours d'arbre se généralise à n'importe quel type d'arbre (voir https://en.wikipedia.org/wiki/Tree_traversal#Arbitrary_trees).
# Les depth-first searches admettent des solutions récursives simples pour le cas de l'arbre binaire:
#       1) pre-order search/traversal/walk (NLR)
#           > N: Visit the current node.
#           > L: Recursively traverse the current node's left subtree.
#           > R: Recursively traverse the current node's right subtree.
#       2) in-order search/traversal/walk (LNR)
#           > L: Recursively traverse the current node's left subtree.
#           > N: Visit the current node.
#           > R: Recursively traverse the current node's right subtree.
#       3) post-order search/traversal/walk (LRN)
#           > L: Recursively traverse the current node's left subtree.
#           > R: Recursively traverse the current node's right subtree.
#           > N: Visit the current node.
#
# Source: https://en.wikipedia.org/wiki/Tree_traversal
#
# Dans les implémentations qui vont suivre, j'ai fais le choix de faire comme si je voulais changer tous les noeuds d'un arbre binaire ayant pour éléments des entiers, ce à l'aide d'une fonction "modify".
# Évidemment, on peut facilement adatper les algorithmes de parcours à d'autres tâches: trouver un élément qui satisfie un prédicat, supprimer un élément en particulier, modifier un élément en particulier, etc., ainsi qu'à d'autres types d'arbres, avec d'autres éléments que des entiers.


class Sentinel(object):
    def __init__(self, nom_sentinelle: str):
        self.name = nom_sentinelle

    def __repr__(self):
        return self.name


LastNone = Sentinel("LastNone")


class Node:
    def __init__(self, val: int, left: "Node | None", right: "Node | None"):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return "Node(" + str(self.val) + ")"


def node_are_equal(node1: Node | None, node2: Node | None):
    if node1 == None:
        return node2 == None
    if node2 == None:
        return node1 == None
    return node1.val == node2.val


class BinaryTree:
    def __init__(self, root: Node | None = None):
        self._root = root

    def __repr__(self) -> str:
        # Source: https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python
        nlevels = self.height()
        width = pow(2, nlevels + 1)

        q: list[tuple[(Node | None, int, int, str)]] = [(self._root, 0, width, "c")]
        levels = []

        while q:
            node, level, x, align = q.pop(0)
            if node is not None:
                if len(levels) <= level:
                    levels.append([])

                levels[level].append([node, level, x, align])
                seg = width // (pow(2, level + 1))
                q.append((node.left, level + 1, x - seg, "l"))
                q.append((node.right, level + 1, x + seg, "r"))

        s = ""
        for i, l in enumerate(levels):
            pre = 0
            preline = 0
            linestr = ""
            pstr = ""
            seg = width // (pow(2, i + 1))
            for n in l:
                valstr = str(n[0].val)
                if n[3] == "r":
                    linestr += (
                        " " * (n[2] - preline - 1 - seg - seg // 2)
                        + "¯" * (seg + seg // 2)
                        + "\\"
                    )
                    preline = n[2]
                if n[3] == "l":
                    linestr += " " * (n[2] - preline - 1) + "/" + "¯" * (seg + seg // 2)
                    preline = n[2] + seg + seg // 2
                pstr += (
                    " " * (n[2] - pre - len(valstr)) + valstr
                )  # correct the position according to the number size
                pre = n[2]
            s += linestr + "\n" + pstr + "\n"
        return s

    def __rec_len(self, root: Node | None) -> int:
        if root == None:
            return 0

        return 1 + self.__rec_len(root.left) + self.__rec_len(root.right)

    def __len__(self) -> int:
        return self.__rec_len(self._root)

    def is_empty(self) -> bool:
        return self._root == None

    def root(self) -> Node | None:
        return self._root

    def __rec_height(self, root: Node | None) -> int:
        if root == None:
            return -1

        return 1 + max(self.__rec_height(root.left), self.__rec_height(root.right))

    def height(self) -> int:
        return self.__rec_height(self._root)

    def is_equal_to(self, bt: "BinaryTree") -> bool:
        queue1: list[Node | None] = [self._root]
        queue2: list[Node | None] = [bt.root()]
        n1: Node | None = None
        n2: Node | None = None

        while queue1 != [] and queue2 != []:
            n1 = queue1.pop(0)
            n2 = queue2.pop(0)
            if not node_are_equal(n1, n2):
                return False
            if n1 != None:
                queue1.append(n1.left)
                queue1.append(n1.right)
            if n2 != None:
                queue2.append(n2.left)
                queue2.append(n2.right)

        # on traite le cas où une queue s'est vidée avant l'autre
        # je me demande si ce cas est nécessaire à traiter car si un arbre à moins de noeuds que l'autre, il aura forcément des feuilles None qui ne vont pas passer le test dans la boucle while
        if not (queue1 == [] and queue2 == []):
            return False
        else:
            return True

    def __rec_is_max_heap(self, node: Node | None) -> bool:
        if node == None:
            return True

        cond = True
        if node.left != None:
            cond = cond and node.val >= node.left.val
        if node.right != None:
            cond = cond and node.val >= node.right.val

        return (
            cond
            and self.__rec_is_max_heap(node.left)
            and self.__rec_is_max_heap(node.right)
        )

    def is_max_heap(self) -> bool:
        # bt est une max_heap ssi tout noeud de bt à une valeur supérieure aux valeurs de ses noeuds fils
        return self.__rec_is_max_heap(self._root)

    def contains(self, v: int) -> bool:
        queue: list[Node | None] = [self._root]
        while queue != []:
            node = queue.pop(0)
            if node != None:
                if node.val == v:
                    return True
                queue.append(node.left)
                queue.append(node.right)
        return False

    def __rec_lca(self, node: Node | None, a: int, b: int) -> Node | None:
        # Je suis un noeud. Si je suis a ou b, je déclare être le lca. Dans le retour de la récursion, si je suis un noeud ayant deux fils qui me disent être lca, c'est que c'est moi le lca.
        if node == None or node.val == a or node.val == b:
            return node
        lca_l = self.__rec_lca(node.left, a, b)
        lca_r = self.__rec_lca(node.right, a, b)
        if lca_l != None and lca_r != None:
            return node
        elif lca_l != None:
            return lca_l
        elif lca_r != None:
            return lca_r
        else:
            return None

    def lca(self, a: int, b: int) -> int | None:
        lca_node = self.__rec_lca(self._root, a, b)
        if lca_node == None:
            return None
        else:
            return lca_node.val

    def __rec_is_bst(
        self, node: Node | None, inf_a: int | None, sup_a: int | None
    ) -> bool:
        if node == None:
            return True

        # on construit la condition sur "node"
        condition = True
        if inf_a != None:
            condition = condition and node.val <= inf_a
        if sup_a != None:
            condition = condition and node.val > sup_a

        return (
            self.__rec_is_bst(node.left, node.val, sup_a)
            and condition
            and self.__rec_is_bst(node.right, inf_a, node.val)
        )

    def is_bst(self) -> bool:
        return self.__rec_is_bst(self._root, None, None)

    def is_complete(self) -> bool:
        # Another way do to it, but more costly:
        #     1) traverse the tree in breadth-first search, storing values in an array, as well as Nones if they are (O(n))
        #     2) trim the Nones at the end (worst case is 2^height-1 Nones to trim, say O(n))
        #     3) check if there is a None in the array; if so, the binary tree isn't complete (O(n))
        # Total: O(3n) in time; O(2n) in space (queue + array)

        # The better way:
        #     1) compute the height of the tree (O(log n) time, if complete tree, O(n) in the worst case; O(1) space, but recursion)
        #     2) traverse the tree in breadth-first search:
        #         - if None encountered at any level other than the last, return false
        #         - if None encountered at the last level, set a boolean flag (say "shouldBeNone")
        #         - if any node of the last level should be None and isn't, return false
        #     3) return true
        # Total: O(2n) in time; O(n) in space (queue)
        if self._root is None:
            return True

        height: int = self.height()
        shouldBeNone: bool = False
        isLastLvl = False
        q: list[tuple[Node | None, int]] = [(self._root, 0)]
        while q != []:
            node, lvl = q.pop(0)
            isLastLvl = lvl >= height

            if isLastLvl and shouldBeNone and node is not None:
                return False

            if node is None:
                if not isLastLvl:
                    return False
                else:
                    shouldBeNone = True
                    continue

            if not isLastLvl:
                q.append((node.left, lvl + 1))
                q.append((node.right, lvl + 1))

        return True

    @staticmethod
    def __rec_array_to_bt(nodes: list[int | None] | None, i: int) -> Node | None:
        if nodes == None or i >= len(nodes) or nodes[i] == None:
            return None

        return Node(
            nodes[i],  # pyright: ignore [reportGeneralTypeIssues]
            BinaryTree.__rec_array_to_bt(nodes, 2 * i + 1),
            BinaryTree.__rec_array_to_bt(nodes, 2 * i + 2),
        )

    @staticmethod
    def array_to_bt(nodes: list[int | None] = []) -> "BinaryTree":
        return BinaryTree(BinaryTree.__rec_array_to_bt(nodes, 0))

    @staticmethod
    def complete_bt_to_array(bt: "BinaryTree") -> list[int | None] | None:
        if not bt.is_complete():
            return None

        root = bt.root()
        if root is None:
            return []

        q: list[tuple[Node, int]] = [(root, 1)]
        array: list[int | None] = []
        while q != []:
            node, depth = q.pop(0)
            array.append(node.val)
            if node.left != None:
                q.append((node.left, depth + 1))
            if node.right != None:
                q.append((node.right, depth + 1))

        return array

    # It seems that only complete binary trees can be converted to arrays.
    # I attempted to make it work for uncomplete binary trees, but I managed to only fill the first level of Nones.
    # I wonder if it is actually impossible. I don't see any reason for that.
    # Maybe keeping track of the level and the offset (from the left, say) of a node could allow to fill the Nones missing by looking at the length of the current array, and the length is should be.
    # See https://en.wikipedia.org/wiki/Binary_tree#Arrays
    # TODO
    @staticmethod
    def bt_to_array(bt: "BinaryTree") -> list[int | None]:
        q: list[Node | Sentinel | None] = [bt.root()]
        array: list[int | None] = []
        while q != []:
            n = q.pop(0)
            if n == LastNone:
                array.append(None)
            elif n == None:
                array.append(None)
                q.append(LastNone)
                q.append(LastNone)
            else:
                array.append(n.val)  # pyright: ignore [reportGeneralTypeIssues]
                q.append(n.left)  # pyright: ignore [reportGeneralTypeIssues]
                q.append(n.right)  # pyright: ignore [reportGeneralTypeIssues]

        # delete unecessary None at the end of the list
        while array[-1] == None:
            del array[-1]

        return array

    def __rec_pre_order_walk(
        self, node: Node | None, depth: int, modify: Callable[[int, int], int]
    ) -> None:
        if node != None:
            node.val = modify(node.val, depth)
            self.__rec_pre_order_walk(node.left, depth + 1, modify)
            self.__rec_pre_order_walk(node.right, depth + 1, modify)

    def pre_order_walk_rec(self, modify: Callable[[int, int], int]) -> "BinaryTree":
        self.__rec_pre_order_walk(self._root, 1, modify)
        return bt

    def pre_order_walk_it(self, modify: Callable[[int, int], int]) -> "BinaryTree":
        if self._root is None:
            return self

        stack: list[tuple[Node, int]] = [(self._root, 1)]
        while stack != []:
            node, depth = stack.pop()
            node.val = modify(node.val, depth)
            if node.right != None:
                stack.append((node.right, depth + 1))
            if node.left != None:
                stack.append((node.left, depth + 1))

        return self

    def __rec_in_order_walk(
        self, node: Node | None, depth: int, modify: Callable[[int, int], int]
    ) -> None:
        if node != None:
            self.__rec_in_order_walk(node.left, depth + 1, modify)
            node.val = modify(node.val, depth)
            self.__rec_in_order_walk(node.right, depth + 1, modify)

    def in_order_walk_rec(self, modify: Callable[[int, int], int]) -> "BinaryTree":
        self.__rec_in_order_walk(self._root, 1, modify)
        return self

    def in_order_walk_it(self, modify: Callable[[int, int], int]) -> "BinaryTree":
        if self._root is None:
            return self

        stack: list[tuple[Node | None, int]] = []
        nd = (self._root, 1)
        while stack != [] or nd[0] != None:
            n, d = nd
            if n != None:
                stack.append(nd)
                nd = (n.left, d + 1)
            else:
                nd = stack.pop()
                n, d = nd
                if n != None:
                    n.val = modify(n.val, d)
                    nd = (n.right, d + 1)

        return self

    def __rec_post_order_walk(
        self, node: Node | None, depth: int, modify: Callable[[int, int], int]
    ) -> None:
        if node != None:
            self.__rec_post_order_walk(node.left, depth + 1, modify)
            self.__rec_post_order_walk(node.right, depth + 1, modify)
            node.val = modify(node.val, depth)

    def post_order_walk_rec(self, modify: Callable[[int, int], int]) -> "BinaryTree":
        self.__rec_post_order_walk(self._root, 1, modify)
        return self

    def post_order_walk_it(self, modify: Callable[[int, int], int]) -> "BinaryTree":
        if self._root is None:
            return self

        stack: list[tuple[Node, int]] = []
        nd: tuple[Node | None, int] = (self._root, 1)
        last_node_visited: Node | None = None

        while stack != [] or nd[0] != None:
            if nd[0] != None:
                stack.append(nd)  # pyright: ignore [reportGeneralTypeIssues]
                nd = (nd[0].left, nd[1] + 1)
            else:
                n, d = stack[-1]
                if n.right != None and n.right != last_node_visited:
                    nd = (n.right, d + 1)
                else:
                    n.val = modify(n.val, d)
                    last_node_visited = n
                    stack.pop()

        return self

    # Je connais qu'une implémentation avec une queue, mais pas une récursive (en existe-t-il une? pas sûr).
    def breadth_first_search(self, modify: Callable[[int, int], int]) -> "BinaryTree":
        if self._root == None:
            return self

        q: list[tuple[Node, int]] = [(self._root, 1)]
        while q != []:
            node, depth = q.pop(0)
            node.val = modify(node.val, depth)
            if node.left != None:
                q.append((node.left, depth + 1))
            if node.right != None:
                q.append((node.right, depth + 1))

        return self


if __name__ == "__main__":

    print("BinaryTree.complete_bt_to_array", end="")
    initial_arr: list[int | None] = [1, 2, 3, 4, 5, 6, 7]
    bt = BinaryTree.array_to_bt(initial_arr)
    res = BinaryTree.complete_bt_to_array(bt)
    assert res == initial_arr, f"Expected {res} to be equal to {initial_arr}."
    initial_arr: list[int | None] = [1, 2, 3, 4]
    bt = BinaryTree.array_to_bt(initial_arr)
    res = BinaryTree.complete_bt_to_array(bt)
    assert res == initial_arr, f"Expected {res} to be equal to {initial_arr}."
    initial_arr: list[int | None] = [1, 2, 3, None, None]
    bt = BinaryTree.array_to_bt(initial_arr)
    res = BinaryTree.complete_bt_to_array(bt)
    expected = [1, 2, 3]
    assert res == expected, f"Expected {res} to be equal to {expected}."
    initial_arr: list[int | None] = [1, 2, 3, 4, None, 6, 7]
    bt = BinaryTree.array_to_bt(initial_arr)
    res = BinaryTree.complete_bt_to_array(bt)
    assert res is None, f"Expected {res} to be None."
    print(": test passed!")

    print("BinaryTree.array_to_bt/BinaryTree.bt_to_array", end="")
    # easy
    initial_arr: list[int | None] = [
        1,
        2,
        3,
        None,
        None,
        4,
        None,
        None,
        None,
        None,
        None,
        5,
        6,
    ]
    bt = BinaryTree.array_to_bt(initial_arr)
    arr: list[int | None] = BinaryTree.bt_to_array(bt)
    assert (
        arr == initial_arr
    ), f"Expected arr ({arr}) to be equal to initial_arr ({initial_arr})."
    # hard
    # q = 20
    # v = 30
    # u = 28
    # w = 32
    # s = 26
    # r = 22
    # t = 27
    # initial_arr = [
    #     q,
    #     None,
    #     u,
    #     None,
    #     None,
    #     s,
    #     w,
    #     None,
    #     None,
    #     None,
    #     None,
    #     r,
    #     t,
    # ]
    # bt = BinaryTree.array_to_bt(initial_arr)
    # arr: list[int | None] = BinaryTree.bt_to_array(bt)
    # assert (
    #     arr == initial_arr
    # ), f"Expected arr ({arr}) to be equal to initial_arr ({initial_arr})."
    print(": tests passed!")

    print("BinaryTree.is_empty", end="")
    bt = BinaryTree()
    assert bt.is_empty, "Binary tree should be empty."
    arr: list[int | None] = [1, 2, 3]
    bt = BinaryTree.array_to_bt(arr)
    assert bt.is_empty, "Binary tree shouldn't be empty."
    print(": tests passed!")

    print("BinaryTree.root", end="")
    expected = 1
    arr: list[int | None] = [expected, 2, 3]
    bt = BinaryTree.array_to_bt(arr)
    root = bt.root()
    assert (
        root is not None and root.val == expected
    ), f"Expected root value to be {expected}, but got {root.val}"  # pyright: ignore [reportOptionalMemberAccess]
    print(": tests passed!")

    print("BinaryTree.height", end="")
    expected = -1
    arr: list[int | None] = []
    bt = BinaryTree.array_to_bt(arr)
    height = bt.height()
    assert height == expected, f"Expected height to be {expected}, but got {height}."
    expected = 2
    arr: list[int | None] = [1, 2, 3, 4, 5, 6, 7]
    bt = BinaryTree.array_to_bt(arr)
    height = bt.height()
    assert height == expected, f"Expected height to be {expected}, but got {height}."
    print(": tests passed!")

    print("BinaryTree.__len__", end="")
    # without None
    expected = 3
    arr: list[int | None] = [1, 2, 3]
    bt = BinaryTree.array_to_bt(arr)
    length = len(bt)
    assert length == expected, f"Expected length to be {expected}, but got {length}."
    # with None
    expected = 2
    arr = [1, 2, None]
    bt = BinaryTree.array_to_bt(arr)
    length = len(bt)
    assert length == expected, f"Expected length to be {expected}, but got {length}."
    print(": tests passed!")

    print("BinaryTree.is_equal_to", end="")
    arr: list[int | None] = [1, 2, 3]
    bt = BinaryTree.array_to_bt(arr)
    assert bt.is_equal_to(
        BinaryTree.array_to_bt(arr)
    ), "Expected binary trees to be equal"
    assert not bt.is_equal_to(
        BinaryTree.array_to_bt()
    ), "Expected binary trees to not be equal"
    print(": tests passed!")

    print("BinaryTree.is_max_heap", end="")
    arr: list[int | None] = [10, 9, 8, 8, 7, 7, 6]
    bt = BinaryTree.array_to_bt(arr)
    assert bt.is_max_heap(), "Expected binary tree to be a max heap."
    arr: list[int | None] = [1, 2, 3]
    bt = BinaryTree.array_to_bt(arr)
    assert not bt.is_max_heap(), "Expected binary tree to not be a max heap."
    print(": tests passed!")

    print("BinaryTree.contains", end="")
    expected = 2
    arr: list[int | None] = [1, expected, 3]
    bt = BinaryTree.array_to_bt(arr)
    assert bt.contains(expected), f"Expected binary tree to contain {expected}."
    notExpected = 4
    assert not bt.contains(
        notExpected
    ), f"Expected binary tree to not contain {expected}."
    print(": tests passed!")

    print("BinaryTree.lca", end="")
    arr: list[int | None] = [1, 2, 3]
    bt = BinaryTree.array_to_bt(arr)
    lca = bt.lca(2, 3)
    expected = 1
    assert (
        lca is not None and lca == expected
    ), f"Expected lca to be {expected}, but got {lca}."
    arr: list[int | None] = [1, 2, 3, 4, 5, None, None, 6, None, 7, 8]
    bt = BinaryTree.array_to_bt(arr)
    lca = bt.lca(6, 8)
    expected = 2
    assert (
        lca is not None and lca == expected
    ), f"Expected lca to be {expected}, but got {lca}."
    print(": tests passed!")

    print("BinaryTree.is_bst", end="")
    arr: list[int | None] = [6, 2, 11, 1, 4, 7, 12]
    bt = BinaryTree.array_to_bt(arr)
    assert bt.is_bst(), f"Expected binary tree to be a binary search tree."
    arr: list[int | None] = [6, 7, 5]
    bt = BinaryTree.array_to_bt(arr)
    assert not bt.is_bst(), f"Expected binary tree to not be a binary search tree."
    print(": tests passed!")

    print("BinaryTree.is_complete", end="")
    arr: list[int | None] = []
    bt = BinaryTree.array_to_bt(arr)
    assert bt.is_complete(), f"Expected binary tree to be complete."
    arr: list[int | None] = [1, 2, 3, 4, 5, 6, 7]
    bt = BinaryTree.array_to_bt(arr)
    assert bt.is_complete(), f"Expected binary tree to be complete."
    arr: list[int | None] = [1, 2, 3, 4]
    bt = BinaryTree.array_to_bt(arr)
    assert bt.is_complete(), f"Expected binary tree to be complete."
    arr: list[int | None] = [1, 2, 3, 4, None, 5, 6]
    bt = BinaryTree.array_to_bt(arr)
    assert not bt.is_complete(), f"Expected binary tree to not be complete."
    arr: list[int | None] = [1, 2, 3, 4, None, None, None, 5, 6]
    bt = BinaryTree.array_to_bt(arr)
    assert not bt.is_complete(), f"Expected binary tree to not be complete."
    print(": tests passed!")

    got = []

    def f(x: int, depth: int) -> int:
        got.append(x)
        return x

    print("BinaryTree.pre_order_walk_rec", end="")
    arr: list[int | None] = [1, 2, 3, 4, 5, 6, 7]
    bt = BinaryTree.array_to_bt(arr)
    got = []
    bt.pre_order_walk_rec(f)
    expected = [1, 2, 4, 5, 3, 6, 7]
    assert got == expected, f"Expected {expected}, but got {got}."
    print(": tests passed!")

    print("BinaryTree.pre_order_walk_it", end="")
    arr: list[int | None] = [1, 2, 3, 4, 5, 6, 7]
    bt = BinaryTree.array_to_bt(arr)
    got = []
    bt.pre_order_walk_it(f)
    expected = [1, 2, 4, 5, 3, 6, 7]
    assert got == expected, f"Expected {expected}, but got {got}."
    print(": tests passed!")

    print("BinaryTree.in_order_walk_rec", end="")
    arr: list[int | None] = [1, 2, 3, 4, 5, 6, 7]
    bt = BinaryTree.array_to_bt(arr)
    got = []
    bt.in_order_walk_rec(f)
    expected = [4, 2, 5, 1, 6, 3, 7]
    assert got == expected, f"Expected {expected}, but got {got}."
    print(": tests passed!")

    print("BinaryTree.in_order_walk_it", end="")
    arr: list[int | None] = [1, 2, 3, 4, 5, 6, 7]
    bt = BinaryTree.array_to_bt(arr)
    got = []
    bt.in_order_walk_rec(f)
    expected = [4, 2, 5, 1, 6, 3, 7]
    assert got == expected, f"Expected {expected}, but got {got}."
    print(": tests passed!")

    print("BinaryTree.post_order_walk_rec", end="")
    arr: list[int | None] = [1, 2, 3, 4, 5, 6, 7]
    bt = BinaryTree.array_to_bt(arr)
    got = []
    bt.post_order_walk_rec(f)
    expected = [4, 5, 2, 6, 7, 3, 1]
    assert got == expected, f"Expected {expected}, but got {got}."
    print(": tests passed!")

    print("BinaryTree.post_order_walk_it", end="")
    arr: list[int | None] = [1, 2, 3, 4, 5, 6, 7]
    bt = BinaryTree.array_to_bt(arr)
    got = []
    bt.post_order_walk_rec(f)
    expected = [4, 5, 2, 6, 7, 3, 1]
    assert got == expected, f"Expected {expected}, but got {got}."
    print(": tests passed!")

    print("BinaryTree.breadth_first_search", end="")
    arr: list[int | None] = [1, 2, 3, 4, 5, 6, 7]
    bt = BinaryTree.array_to_bt(arr)
    got = []
    bt.breadth_first_search(f)
    expected = arr
    assert got == expected, f"Expected {expected}, but got {got}."
    print(": tests passed!")

    print("All tests passed!")
    pass
