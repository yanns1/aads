from typing import Callable, TypeVar, Generic, Iterator
from copy import deepcopy
from math import floor

K = TypeVar("K")
Number = TypeVar("Number", int, float)


class Item(Generic[K, Number]):
    """
    Un item est la donnée d'une clé et d'un entier qui représente la priorité
    de l'item.
    C'est un élément d'un tas-min/max binaire (classes MinHeap et MaxHeap).
    Un item ayant une priorité plus grande qu'un autre sera servi
    avant/après par le tas-max/min.
    """

    def __init__(self, key: K, priority: Number) -> None:
        """
        Initialise un objet de type Item ayant pour clé key et pour priorité priority.

        Params:
          - key : K : La clé que va contenir l'item.
            Cette clé peut être un objet Python
            de n'importe quel type, que l'on nomme K. Cependant, lors de la création
            d'un tas binaire, il faudra rester consistant: tous les items devront avoir
            le même type K.
          - priority : Number : La priorité de l'item.

        Returns:
          - Item[K, Number] : L'item nouvellement crée.
        """
        self.key: K = key
        self.priority: Number = priority

    def __repr__(self) -> str:
        return "Item(" + str(self.key) + ", " + str(self.priority) + ")"

    def __eq__(self, other) -> bool:
        if isinstance(other, Item):
            return other.priority == self.priority and other.key == self.key
        return False


class BinaryHeap(Generic[K, Number]):
    """
    Implémentation du tas binaire, avec l'ordre appliqué sur les items fournit
    par l'utilisteur l'ordre de l'instanciation de cette classe.
    Par example, l'ordre:
      lambda a, b: a >= b
    crée un tas-max binaire, et l'ordre:
      lambda a, b: a <= b
    crée un tas-min binaire.

    Les noeuds du tas sont des items de type Item, et tous les items
    doivent avoir leurs clés de même type, que l'on nomme K.
    """

    def __init__(
        self,
        items: list[Item[K, Number]] = [],
        order: Callable[[Number, Number], bool] = lambda a, b: a >= b,
    ) -> None:
        """
        Initialise un tas binaire d'ordre order et ayant pour éléments items.
        L'objet crée est donc un arbre binaire qui vérifie la propriété de tas:
          Pour chaque item de l'arbre, la priorité de celui-ci est supérieure à
          celles de ses items fils, selon order.
        Par défaut, l'ordre est:
          lambda a, b: a >= b
        ce qui génère un tas-max binaire.

        Params:
          - items : list[Item[K, Number]] : Les items (donnée d'un clé et d'une
            priorité) servant de noeuds du tas, ayant leurs clés de type K.
          - order : Callable[[Number, Number], bool] : Une fonction définissant un
            ordre sur les items à partir de leurs priorités.
            Pour deux items a et b, si order(a.priority, b.priority) == True, alors
            a est considéré comme "supérieur" à b, c'est-à-dire que le tas binaire va
            servir a avant de servir b. Sinon c'est l'inverse.

        Returns:
          - BinaryHeap[K, Number]: Le tas binaire nouvellement crée.
        """
        n: int = len(items)
        i_start: int = floor(n / 2) - 1
        i_end: int = n - 1
        for i_parent in range(i_start, -1, -1):
            self.__percolate_down_item(order, items, i_end, i_parent)

        self._array: list[Item[K, Number]] = items
        self._order: Callable[[Number, Number], bool] = order
        self.__make_copy = True

    def __repr__(self) -> str:
        return "(BinaryHeap) " + str(self._array)

    def __eq__(self, bh: "BinaryHeap[K, Number]") -> bool:
        return self._array == bh._array

    # See this for how to make a class a generator, or more precisely, an iterator: https://stackoverflow.com/questions/42983569/how-to-write-a-generator-class
    def __next__(self) -> Item[K, Number]:
        if self.__make_copy:
            self.__copy = deepcopy(self)
            self.__make_copy = False

        item = self.__copy.pop()
        while item is not None:
            return item
        else:
            self.__make_copy = True
            raise StopIteration

    def __iter__(self):
        return self

    def __children_indexes(self, parent_idx: int) -> tuple[int, int]:
        """
        Pour un indice d'un noeud parent donné en entrée, renvoie les indices des deux
        noeuds enfants (sachant que l'arbre binaire est codé sous forme de tableau).

        Params:
          - parent_idx : int : Indice du noeud parent pour lequel on souhaite obtenir
            les indices des noeuds enfants.

        Returns:
          - tuple[int, int] : Les indices des noeuds enfants.
        """
        return 2 * parent_idx + 1, 2 * parent_idx + 2

    def __parent_index(self, child_idx: int) -> int:
        """
        Pour un indice d'un noeud enfant donné en entrée, renvoie l'indice du
        noeud parent (sachant que l'arbre binaire est codé sous forme de tableau).

        Params:
          - child_idx : int : Indice du noeud enfant pour lequel on souhaite obtenir
            l'indice du noeud parent.

        Returns:
          - int : L'indice du noeud parent.
        """
        return floor((child_idx - 1) / 2)

    def __percolate_down_item(
        self,
        order: Callable[[Number, Number], bool],
        ns: list[Item[K, Number]],
        i_end: int,
        i: int,
    ) -> list[Item[K, Number]]:
        """
        Pour une liste d'items ns encodant un arbre binaire, on fait descendre l'item
        d'indice i jusqu'à sa véritable place dans l'arbre (étant donné sa priorité) en
        l'échangeant, à une étape donnée, avec son item fils de priorité la plus grande
        s'il a une priorité plus faible que ce fils (selon l'ordre order).
        La notation "percolate_down" vient de https://fr.wikipedia.org/wiki/Tas_binaire.

        Params:
          - order : Callable[[Number, Number], bool] : L'ordre avec lequel comparer
            les items de l'arbre.
          - ns : list[Item[K, Number]] : Les items de l'arbre binaire.
          - i_end : int : L'indice de l'élément où s'arrête la descente de l'item
            d'indice i. Généralement, on ventu i_end = len(items) - 1.
          - i : int : L'indice de l'item que l'on souhaite "percolate down".

        Returns:
          - list[Item[K, Number]] : La liste des items après avoir descendu l'item
            d'indice i.
        """
        if i_end < 1:
            return ns
        if not (0 <= i <= i_end):
            raise Exception(
                "The index given is not in the range [0, " + str(i_end) + "]."
            )

        parent_priority = ns[i].priority
        i_child1, i_child2 = self.__children_indexes(i)
        i_sup_child = i_child1
        if i_child1 <= i_end and i_child2 <= i_end:
            if order(ns[i_child2].priority, ns[i_child1].priority):
                i_sup_child = i_child2
        if i_child1 > i_end and i_child2 <= i_end:
            i_sup_child = i_child2
        # if i_child2 > i_end and i_child1 <= i_end:
        # stay as is
        # if i_child1 > i_end and i_child2 > i_end:
        # should not happen however, because we only consider nodes with at least one child
        # stay as is; will not be able to enter while loop anyway

        while i_sup_child <= i_end and order(ns[i_sup_child].priority, parent_priority):
            # swap parent and sup_child
            ns[i], ns[i_sup_child] = ns[i_sup_child], ns[i]

            # determine new sup_child
            i = i_sup_child
            parent_priority = ns[i].priority
            i_child1, i_child2 = self.__children_indexes(i)
            i_sup_child = i_child1
            if i_child1 <= i_end and i_child2 <= i_end:
                if order(ns[i_child2].priority, ns[i_child1].priority):
                    i_sup_child = i_child2
            if i_child1 > i_end and i_child2 <= i_end:
                i_sup_child = i_child2

        return ns

    def is_empty(self) -> bool:
        return self._array == []

    def size(self) -> int:
        return len(self._array)

    def push(self, item: Item[K, Number]) -> "BinaryHeap[K, Number]":
        i_item: int = len(self._array)
        i_parent: int = self.__parent_index(i_item)

        # On insère le nouvel item à la fin du tas...
        self._array.append(item)

        # ... puis on le fait remonter jusqu'à sa place finale,
        # en fonction de sa priorité,
        # en l'échangeant avec son parent direct à chaque étape
        # s'il a une priorité supérieure à celui-ci.
        while i_item > 0 and not self._order(
            self._array[i_parent].priority, self._array[i_item].priority
        ):
            self._array[i_item], self._array[i_parent] = (
                self._array[i_parent],
                self._array[i_item],
            )
            i_item, i_parent = i_parent, self.__parent_index(i_parent)

        return self

    def remove(self, key: K) -> "BinaryHeap[K, Number]":
        # On cherche la clé à supprimer (en linear search,
        # pas le choix car les clés ne sont a priori pas ordrées),
        # puis une fois l'item i trouvé, on l'échange avec le dernier
        # de la liste j,
        # puis on supprime le dernier élément de la liste
        # (càd l'élement qu'on voulait supprimer). Ensuite on
        # "percolate_down" j qui a pris la place de i, si nécessaire.

        i: int = 0
        n: int = len(self._array)
        while i < n and self._array[i].key != key:
            i += 1

        if i >= n:
            raise Exception("Item with key " + str(key) + " not found.")
        else:  # on a trouvé la clé
            self._array[i] = self._array[-1]
            del self._array[-1]
            n -= 1
            self.__percolate_down_item(self._order, self._array, n - 1, i)

        return self

    def __remove_at_index(self, i: int) -> "BinaryHeap[K, Number]":
        if i == -1:
            i = len(self._array) - 1

        if i < 0 or i >= len(self._array):
            raise Exception(
                "Tried to delete element at index {i}, but it's out of bounds."
            )

        n = len(self._array)
        self._array[i] = self._array[-1]
        del self._array[-1]
        n -= 1
        self.__percolate_down_item(self._order, self._array, n - 1, i)

        return self

    def pop(self) -> Item[K, Number] | None:
        if len(self._array) == 0:
            return None

        item = self._array[0]
        self.__remove_at_index(0)

        return item

    def peek(self) -> Item[K, Number] | None:
        if len(self._array) == 0:
            return None
        return self._array[0]

    def breadth_first_traversal(self) -> Iterator[Item[K, Number]]:
        """
        Retourne un itérateur qui renvoie un item du tas après l'autre en traversant
        celui-ci en largeur.
        Étant donné l'implémentation du tas sous forme de tableau, cela revient
        à traverser linéairement le tableau.

        Returns:
          - Iterator[Item[K, Number]]
        """
        for item in self._array:
            yield item


class MinHeap(Generic[K, Number], BinaryHeap[K, Number]):
    """
    Une sous-classe de BinaryHeap, avec pour ordre:
      lambda a, b: a <= b
    ce qui donne un tas-min binaire.
    """

    def __init__(self, items: list[Item[K, Number]] = []) -> None:
        super().__init__(items, order=lambda a, b: a <= b)

    def __repr__(self) -> str:
        return "(MinHeap) " + str(self._array)


class MaxHeap(Generic[K, Number], BinaryHeap[K, Number]):
    """
    Une sous-classe de BinaryHeap, avec pour ordre:
      lambda a, b: a >= b
    ce qui donne un tas-max binaire.
    """

    def __init__(self, items: list[Item[K, Number]] = []) -> None:
        super().__init__(items, order=lambda a, b: a >= b)

    def __repr__(self) -> str:
        return "(MaxHeap) " + str(self._array)


def tests():
    print("BinaryHeap.__eq__", end="")
    items = [Item(i, i) for i in range(5)]
    bh1 = BinaryHeap(items)
    bh2 = BinaryHeap(items)
    assert bh1 == bh2, f"Expected binary heaps to be equal."
    print(": tests passed!")

    print("BinaryHeap.is_empty", end="")
    items = []
    bh = BinaryHeap(items)
    assert bh.is_empty(), "Expected binary heap to be empty."
    items = [Item(i, i) for i in range(5)]
    bh = BinaryHeap(items)
    assert not bh.is_empty(), "Expected binary heap to not be empty."
    print(": tests passed!")

    print("BinaryHeap.size", end="")
    expected = 10
    items = [Item(i, i) for i in range(expected)]
    bh = BinaryHeap(items)
    got = bh.size()
    assert got == expected, f"Expected size to be {expected}, but got {got}."
    expected = 0
    items = [Item(i, i) for i in range(expected)]
    bh = BinaryHeap(items)
    got = bh.size()
    assert got == expected, f"Expected size to be {expected}, but got {got}."
    print(": tests passed!")

    print("BinaryHeap.push/BinaryHeap.pop", end="")
    items = [Item(i, i) for i in range(5)]
    bh = BinaryHeap(items)
    bh.push(Item(-1, -1))
    expected = Item(4, 4)
    got = bh.pop()
    assert got == expected, f"Expected {expected}, but got {got}."
    items = [Item(i, i) for i in range(5)]
    bh = BinaryHeap(items)
    expected = Item(5, 5)
    bh.push(expected)
    got = bh.pop()
    assert got == expected, f"Expected {expected}, but got {got}."
    items = []
    bh = BinaryHeap(items)
    got = bh.pop()
    assert got is None, f"Expected {got} to be None."
    print(": tests passed!")

    print("BinaryHeap.delete", end="")
    items = [Item(i, i) for i in range(5)]
    bh = BinaryHeap(items)
    bh.remove(4)
    expected = Item(3, 3)
    got = bh.pop()
    assert got == expected, f"Expected {expected}, but got {got}."
    bh.remove(2)
    expected = Item(1, 1)
    got = bh.pop()
    assert got == expected, f"Expected {expected}, but got {got}."
    items = []
    bh = BinaryHeap(items)
    got_exception = False
    try:
        bh.remove(0)
    except Exception as _:
        got_exception = True
    assert (
        got_exception
    ), f"Expected exception to be raised because tried to remove element at index out of bounds."
    print(": tests passed!")

    print("BinaryHeap.peak", end="")
    items = [Item(i, i) for i in range(3)]
    bh = BinaryHeap(items)
    expected = Item(2, 2)
    got = bh.peek()
    assert got == expected, f"Expected {expected}, but got {got}."
    bh.remove(2)
    expected = Item(1, 1)
    got = bh.peek()
    assert got == expected, f"Expected {expected}, but got {got}."
    bh.remove(1)
    expected = Item(0, 0)
    got = bh.peek()
    assert got == expected, f"Expected {expected}, but got {got}."
    bh.remove(0)
    expected = None
    got = bh.peek()
    assert got == expected, f"Expected {expected}, but got {got}."
    print(": tests passed!")

    print("BinaryHeap.__iter__/BinaryHeap.__next__", end="")
    items = [Item(i, i) for i in range(5)]
    bh = BinaryHeap(items)
    i = 4
    for item in bh:
        expected = Item(i, i)
        assert item == expected, f"Expected {item} to be {expected}."
        i -= 1
    # Test a second time to test the reset in __next__
    i = 4
    for item in bh:
        expected = Item(i, i)
        assert item == expected, f"Expected {item} to be {expected}."
        i -= 1
    print(": tests passed!")

    print("All tests passed!")


if __name__ == "__main__":

    tests()
    pass
