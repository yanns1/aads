from __future__ import annotations


class Cell:
    def __init__(self, val: int, prev: Cell | None, next: Cell | None) -> None:
        self.val: int = val
        self.prev: Cell | None = prev
        self.next: Cell | None = next


# Un maillon fictif "sentinelle" n'est pas utile. L'idée du "sentinelle" c'est de pouvoir traiter les listes vides comme les listes remplies, en faisant les opérations sur le maillon sentinelle. Mais il suffit de faire le test size == 0 pour le cas de la liste vide à la place.
# Tel quelle, la liste est potentiellement infinie.
class LinkedList:
    def __init__(self, elements: list[int] = []) -> None:
        # See access modifiers in Python: https://www.geeksforgeeks.org/access-modifiers-in-python-public-private-and-protected/
        self.__head: Cell | None = None
        self.__size: int = 0
        self.__next_cell: Cell | None = self.__head
        self.__next_i: int = 0

        for el in elements:
            self.append(el)

    def __len__(self) -> int:
        return self.__size

    def __repr__(self) -> str:
        if self.__head == None:
            return "(LinkedList) []"

        s = "(LinkedList) ["
        curr_cell = self.__head
        count = 0
        length = self.__size
        # on traite tous les éléments sauf le dernier
        while count < length - 1 and curr_cell != None:
            s += str(curr_cell.val) + ", "
            curr_cell = curr_cell.next
            count += 1

        # on traite le dernier élément
        if curr_cell != None:
            s += str(curr_cell.val)
        s += "]"

        return s

    # See this for how to make a class a generator, or more precisely, an iterator: https://stackoverflow.com/questions/42983569/how-to-write-a-generator-class
    def __next__(self) -> int:
        if (self.__next_i < self.__size and self.__next_cell is not None):
            val = self.__next_cell.val
            self.__next_cell = self.__next_cell.next
            self.__next_i += 1
            return val
        else:
            self.__next_cell = self.__head
            self.__next_i = 0
            raise StopIteration

    def __iter__(self):
        return self

    def __bool__(self) -> bool:
        # The condition self.__head == None is equivalent, and sometimes better than user this function for type checking
        return self.__size != 0

    def __eq__(self, other) -> bool:
        if not isinstance(other, LinkedList):
            return False

        curr_cell_self = self.__head
        curr_cell_other = other.get_head()
        i = 0
        while i < self.__size and curr_cell_self is not None and curr_cell_other is not None:
            if curr_cell_other.val != curr_cell_self.val:
                return False
            curr_cell_self = curr_cell_self.next
            curr_cell_other = curr_cell_other.next
            i += 1

        if ((curr_cell_self is None and curr_cell_other is not None) or (curr_cell_self is not None and curr_cell_other is None)):
            return False
            
        return True

    def get_head(self) -> Cell | None:
        return self.__head

    def get_tail(self) -> Cell | None:
        if self.__head == None:
            return None
        return self.__head.prev  # car liste circulaire

    def insert(self, c: int, neighbor: Cell | None = None, after: bool = True) -> Cell:
        self.__size += 1

        if neighbor == None or self.__head == None:
            self.__head = Cell(c, None, None)
            self.__head.prev = self.__head
            self.__head.next = self.__head
            return self.__head

        if neighbor == self.__head and not after:
            tail = self.get_tail()
            if tail == None:
                raise Exception("La liste n'est pas circulaire! Elle devrait l'être.")

            new_cell = Cell(c, tail, self.__head)
            self.__head.prev = new_cell
            tail.next = new_cell
            self.__head = new_cell
            return new_cell

        # lorsque after == False, on s'arrange pour se ramener au cas où after == True, de manière à traiter qu'un seul cas après
        if after == False:
            # si on veut insérer avant, ça revient à insérer après la cellule d'avant
            neighbor = neighbor.prev
            # on n'a pas besoin d'affecter "True" à after, il suffit de considérer qu'il est True par la suite

        if neighbor == None:
            raise Exception("La liste n'est pas circulaire! Elle devrait l'être.")

        new_cell = Cell(c, neighbor, neighbor.next)
        if neighbor.next != None:
            neighbor.next.prev = new_cell
        neighbor.next = new_cell

        return new_cell

    def append(self, val: int) -> None:
        self.__size += 1

        # si la liste est vide
        if self.__head == None:
            self.__head = Cell(val, None, None)
            self.__head.prev = self.__head
            self.__head.next = self.__head
            return

        if self.__head.prev is not None:
            if self.__head.prev.next is not None:
                new_cell = Cell(val, self.__head.prev, self.__head)
                self.__head.prev.next = new_cell
                self.__head.prev = new_cell

    def prepend(self, val: int) -> None:
        self.__size += 1

        # si la liste est vide
        if self.__head == None:
            self.__head = Cell(val, None, None)
            self.__head.prev = self.__head
            self.__head.next = self.__head
            return

        if self.__head.prev is not None and self.__head.next is not None:
            if self.__head.prev.next is not None:
                new_cell = Cell(val, self.__head.prev, self.__head)
                self.__head.prev.next = new_cell
                self.__head = new_cell

    def lookup(self, item: int) -> Cell | None:
        if self.__head == None:
            return None

        curr_cell: Cell | None = self.__head
        count = 1
        length = self.__size
        while count < length and curr_cell is not None and curr_cell.val != item:
            curr_cell = curr_cell.next
            count += 1

        return curr_cell if count < length else None

    def cell_at(self, i: int) -> Cell | None:
        # on suppose que les cells sont indéxées à partir de 0, donc i=0 correspond au premier élément (la head)

        # si la liste est vide, on la traite directement pour ne pas avoir un modulo 0, qui est interdit
        if self.__head == None:
            return None

        # si i est plus grand que la taille de la liste, on obtiendra l'élément à la place i % taille_liste car la liste est circulaire
        i = i % self.__size

        final_cell = self.__head
        for _ in range(i):
            if final_cell == None:
                return None
            else:
                final_cell = final_cell.next

        return final_cell

    def remove(self, c: Cell | None) -> LinkedList:
        if c is None:
            return self

        if c.prev == None or c.next == None:
            raise Exception("La liste n'est pas circulaire! Elle devrait l'être.")

        if self.__size == 1:
            self.__head = None
            self.__size = 0
            return self

        c.prev.next = c.next
        c.next.prev = c.prev

        if c == self.__head:
            self.__head = c.next

        self.__size -= 1
        return self

    def extend(self, ll: LinkedList) -> LinkedList:
        if self.__head == None:
            return ll

        ll_head = ll.get_head()
        self_tail = self.get_tail()

        if ll_head == None:
            return self

        if self_tail == None:
            raise Exception("La liste self n'est pas circulaire! Elle devrait l'être.")

        # le next de la queue de self devient la tête de ll
        self_tail.next = ll_head
        # le prev de la tête de ll devient la queue de self
        ll_head.prev = self_tail

        # change the size of self
        self.__size += len(ll)

        return self


if __name__ == "__main__":

    print("LinkedList.__init__/LinkedList.__repr__", end="")
    ll = LinkedList([1, 2, 3])
    expected = "(LinkedList) [1, 2, 3]"
    got = str(ll)
    assert got == expected, f"Expected {expected}, got {got}."
    print(": tests passed!")

    print("LinkedList.__len__", end="")
    ll = LinkedList([1, 2, 3])
    expected = 3
    got = len(ll)
    assert (
        got == expected
    ), f"Expected linked list to have {expected} elements, but got {got}."
    ll = LinkedList([])
    expected = 0
    got = len(ll)
    assert (
        got == expected
    ), f"Expected linked list to have {expected} elements, but got {got}."
    print(": tests passed!")

    print("LinkedList.__bool__", end="")
    ll = LinkedList([])
    assert not ll, "Linked list should be empty."
    ll = LinkedList([1])
    assert ll, "Linked list shouldn't be empty."
    print(": tests passed!")

    print("LinkedList.__eq__", end="")
    ll1 = LinkedList([])
    ll2 = LinkedList([])
    assert ll1 == ll2, "Linked lists should be equal."
    ll1 = LinkedList([1, 2, 3])
    ll2 = LinkedList([1, 2, 3])
    assert ll1 == ll2, "Linked lists should be equal."
    ll1 = LinkedList([1, 2, 3, 4, 5])
    ll2 = LinkedList([1, 2, 3])
    assert ll1 != ll2, "Linked lists should not be equal."
    ll1 = LinkedList([1, 2, 4])
    ll2 = LinkedList([1, 1, 3])
    assert ll1 != ll2, "Linked lists should not be equal."
    print(": tests passed!")

    print("LinkedList.get_head", end="")
    expected = 1
    ll = LinkedList([expected, 2, 3])
    head = ll.get_head()
    assert (
        head != None and head.val == expected
    ), f"Expected head value to be {expected}, but got {head.val}."  # pyright: ignore [reportOptionalMemberAccess]
    print(": tests passed!")

    print("LinkedList.get_tail", end="")
    expected = 3
    ll = LinkedList([1, 2, expected])
    tail = ll.get_tail()
    assert (
        tail != None and tail.val == expected
    ), f"Expected tail value to be {expected}, but got {tail.val}."  # pyright: ignore [reportOptionalMemberAccess]
    print(": tests passed!")

    print("LinkedList.lookup", end="")
    expected = 2
    ll = LinkedList([1, expected, 3])
    cell = ll.lookup(expected)
    assert (
        cell is not None and cell.val == 2
    ), f"Expected cell value to be {expected}, but got {cell.val}."  # pyright: ignore [reportOptionalMemberAccess]
    print(": tests passed!")

    print("LinkedList.insert", end="")
    # Inserting the first element
    ll = LinkedList([])
    expected = 1
    ll.insert(expected)
    head = ll.get_head()
    assert (
        head != None and head.val == expected
    ), f"Expected head value to be {expected}, but got {head.val}."  # pyright: ignore [reportOptionalMemberAccess]
    tail = ll.get_tail()
    assert (
        tail != None and tail.val == expected
    ), f"Expected tail value to be {expected}, but got {tail.val}."  # pyright: ignore [reportOptionalMemberAccess]
    length = len(ll)
    assert length == 1, f"Expected length to be 1, but got {length}."
    # Inserting at the beginning
    ll = LinkedList([1, 2, 3])
    head = ll.get_head()
    ll.insert(0, head, False)
    expected = "(LinkedList) [0, 1, 2, 3]"
    got = str(ll)
    assert got == expected, f"Expected {expected}, got {got}."
    # Inserting at the end
    ll = LinkedList([1, 2, 3])
    tail = ll.get_tail()
    ll.insert(4, tail, True)
    expected = "(LinkedList) [1, 2, 3, 4]"
    got = str(ll)
    assert got == expected, f"Expected {expected}, got {got}."
    # Inserting in the middle (before)
    ll = LinkedList([1, 3, 4])
    ll.insert(2, ll.lookup(3), False)
    expected = "(LinkedList) [1, 2, 3, 4]"
    got = str(ll)
    assert got == expected, f"Expected {expected}, got {got}."
    # Inserting in the middle (after)
    ll = LinkedList([1, 2, 4])
    ll.insert(3, ll.lookup(2), True)
    expected = "(LinkedList) [1, 2, 3, 4]"
    got = str(ll)
    assert got == expected, f"Expected {expected}, got {got}."
    print(": tests passed!")

    print("LinkedList.prepend", end="")
    ll = LinkedList([1, 2, 3])
    ll.prepend(0)
    expected = "(LinkedList) [0, 1, 2, 3]"
    got = str(ll)
    assert got == expected, f"Expected {expected}, got {got}."
    print(": tests passed!")

    print("LinkedList.append", end="")
    ll = LinkedList([1, 2, 3])
    ll.append(4)
    expected = "(LinkedList) [1, 2, 3, 4]"
    got = str(ll)
    assert got == expected, f"Expected {expected}, got {got}."
    print(": tests passed!")

    print("LinkedList.cell_at", end="")
    ll = LinkedList([1, 2, 3])
    zero = ll.cell_at(0)
    assert (
        zero != None and zero.val == 1
    ), f"Expected cell value to be 1, but got {zero.val}."  # pyright: ignore [reportOptionalMemberAccess]
    one = ll.cell_at(1)
    assert (
        one != None and one.val == 2
    ), f"Expected cell value to be 2, but got {one.val}."  # pyright: ignore [reportOptionalMemberAccess]
    two = ll.cell_at(2)
    assert (
        two != None and two.val == 3
    ), f"Expected cell value to be 3, but got {two.val}."  # pyright: ignore [reportOptionalMemberAccess]
    three = ll.cell_at(3)
    assert (
        three != None and three.val == 1
    ), f"Expected cell value to be 1, but got {three.val}."  # pyright: ignore [reportOptionalMemberAccess]
    print(": tests passed!")

    print("LinkedList.remove", end="")
    # remove head
    ll = LinkedList([1, 2, 3])
    ll.remove(ll.get_head())
    expected = "(LinkedList) [2, 3]"
    got = str(ll)
    assert got == expected, f"Expected {expected}, got {got}."
    # remove tail
    ll = LinkedList([1, 2, 3])
    ll.remove(ll.get_tail())
    expected = "(LinkedList) [1, 2]"
    got = str(ll)
    assert got == expected, f"Expected {expected}, got {got}."
    # remove in the middle
    ll = LinkedList([1, 2, 3])
    ll.remove(ll.cell_at(1))
    expected = "(LinkedList) [1, 3]"
    got = str(ll)
    assert got == expected, f"Expected {expected}, got {got}."
    print(": tests passed!")

    print("LinkedList.extend", end="")
    ll = LinkedList([1, 2, 3])
    ll.extend(LinkedList([4, 5, 6]))
    expected = "(LinkedList) [1, 2, 3, 4, 5, 6]"
    got = str(ll)
    assert got == expected, f"Expected {expected}, got {got}."
    print(": tests passed!")

    print("LinkedList.__iter__/LinkedList.__next__", end="")
    arr = [1, 2, 3, 4, 5, 6]
    ll = LinkedList(arr)
    i = 0
    for x in ll:
        assert x == arr[i], f"Expected {x} to be {arr[i]}."
        i += 1
    arr = [3, 1, 8, 9, 110]
    ll = LinkedList(arr)
    i = 0
    for x in ll:
        assert x == arr[i], f"Expected {x} to be {arr[i]}."
        i += 1
    print(": tests passed!")

    print("All tests passed!")
    pass
