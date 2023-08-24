from typing import Iterator, Union
from functools import partial
from collections.abc import Callable, Iterator
import math


def encode(s: str) -> int:
    res = 0
    for char in s:
        res += ord(char)
    return res


def compress(m: int, n: int) -> int:
    return n % m


def my_hash(m: int, s: str) -> int:
    return compress(m, encode(s))


def python_hash(m: int, s: str) -> int:
    return compress(m, hash(s))


def quadratic_probing(
    h: Callable[[int, str], int], max_size: int, k: str
) -> Iterator[int]:
    i = 0
    hash_val = h(max_size, k)
    c1 = 0.5
    c2 = 0.5
    c3 = 0
    while True:
        yield compress(max_size, int(hash_val + c1 * i**2 + c2 * i + c3))
        i += 1


class Sentinel(object):
    def __init__(self, sentinel_name: str):
        self.__name = sentinel_name

    def __repr__(self):
        return self.__name


Deleted = Sentinel("Deleted")
EmptySlot = Union[None, Sentinel]


class Item:
    def __init__(self, key: str, val: int):
        self.key = key
        self.val = val

    def __repr__(self) -> str:
        return "Item(" + str(self.key) + ", " + str(self.val) + ")"

    def to_tuple(self) -> tuple[str, int]:
        return (self.key, self.val)


class HashMap:
    def __init__(self, max_size: int, items: list[tuple[str, int]]):
        if len(items) > max_size:
            max_size = len(items)

        # Pour un fonctionnement optimal du sondage quadratique, il faut max_size qui soit une puissance de deux.
        # Il faut aussi size <= 2/3 max_size.
        # Ducoup, on remplace la max_size par la puissance de deux supérieure la plus proche de max_size. Cela revient à regarder le nombre de chiffres qu'il faudrait pour encoder max_size en base 2, plus un.
        self.__max_size = (
            2 if max_size == 0 else 2 ** math.ceil(math.log(max_size) / math.log(2))
        )

        self.__probe = partial(quadratic_probing, my_hash)
        partial_probe = partial(self.__probe, self.__max_size)
        self.__items: list[Item | EmptySlot] = [None] * self.__max_size
        for (k, v) in items:
            nb_tests = 0
            gen_indice = partial_probe(k)
            indice = next(gen_indice)
            while nb_tests <= self.__max_size and self.__items[indice] != None:
                indice = next(gen_indice)
                nb_tests += 1
            self.__items[indice] = Item(k, v)

        self.__i_next = 0

    def __repr__(self) -> str:
        s = "{"
        is_empty = True
        is_first_item = True
        for i in range(self.__max_size):
            item = self.__items[i]
            if not isinstance(item, EmptySlot):
                if is_empty:
                    is_empty = False
                if is_first_item:
                    s += "\n"
                    is_first_item = False
                else:
                    s += ",\n"
                s += "  '" + item.key + "': " + str(item.val)

        if is_empty:
            s += "}"
        else:
            s += "\n}"

        return s

    def __len__(self) -> int:
        size = 0
        for item in self.__items:
            if not isinstance(item, EmptySlot):
                size += 1
        return size

    # Previously called is_empty, __bool__ is almost like it, but not quite.
    # See https://docs.python.org/3.5/reference/datamodel.html#object.__bool__
    # for the semantic.
    def __bool__(self) -> bool:
        return len(self) != 0

    def __getitem__(self, k) -> int:
        if not isinstance(k, str):
            raise TypeError("Key should be a string.")

        max_size = self.__max_size
        gen_indice = self.__probe(max_size, k)
        item = self.__items[next(gen_indice)]
        nb_tests = 0

        while (
            nb_tests <= max_size
            and item != None
            and (item == Deleted or item.key != k)  # pyright: ignore
        ):
            item = self.__items[next(gen_indice)]
            nb_tests += 1

        if nb_tests > max_size or item == None or item == Deleted:
            raise KeyError(f"Key '{k}' not found.")

        return item.val  # pyright: ignore [reportGeneralTypeIssues]

    def __setitem__(self, k, v: int):
        if not isinstance(k, str):
            raise TypeError("Key should be a string.")

        max_size = self.__max_size
        gen_indice = self.__probe(max_size, k)
        indice = next(gen_indice)
        item = self.__items[indice]
        nb_tests = 0

        while (
            nb_tests <= max_size
            and item != None
            and item != Deleted
            and item.key != k  # pyright: ignore [reportGeneralTypeIssues]
        ):
            indice = next(gen_indice)
            item = self.__items[indice]
            nb_tests += 1

        if (
            item == None
            or item == Deleted
            or item.key == k  # pyright: ignore [reportGeneralTypeIssues]
        ):
            self.__items[indice] = Item(k, v)

        # Si plus de place dans la liste, il faut étendre la liste.
        # La méthode de réindexation choisie est simplement de reconstruire un hash map de zéro, avec la nouvelle taille prise en compte. Donc c'est essentiellement le même code que __init__ de HashMap.
        # Il doit y avoir moyen de réindexer plus efficacement. En plus je ne fais pas le changement "in place". Je crée un nouveau hashmap.
        if nb_tests > max_size:
            items: list[tuple[str, int]] = [(k, v)]
            size = 1
            for item in self.__items:
                if item != None and item != Deleted:
                    items.append(
                        (
                            item.key,  # pyright: ignore
                            item.val,  # pyright: ignore
                        )
                    )
                    size += 1
            new_max_size = max_size
            if size > max_size:
                new_max_size = 2 ** math.ceil(math.log(size + 1) / math.log(2))
            return HashMap(new_max_size, items)

        return self

    def __delitem__(self, k):
        if not isinstance(k, str):
            raise TypeError("Key should be a string.")

        max_size = self.__max_size
        gen_indice = self.__probe(max_size, k)
        indice = next(gen_indice)
        item = self.__items[indice]
        nb_tests = 0

        while (
            nb_tests <= max_size
            and item != None
            and (item == Deleted or item.key != k)  # pyright: ignore
        ):
            indice = next(gen_indice)
            item = self.__items[indice]
            nb_tests += 1

        if nb_tests > max_size or item == None:
            # key not found
            raise KeyError(f"Key '{k}' not found.")
        else:
            # key has been found, so delete
            self.__items[indice] = Deleted

    def __eq__(self, other) -> bool:
        if not isinstance(other, HashMap):
            return False

        for k in self.keys():
            try:
                if other[k] != self[k]:
                    return False
            except KeyError:
                return False

        return True

    # See this for how to make a class a generator, or more precisely, an iterator: https://stackoverflow.com/questions/42983569/how-to-write-a-generator-class
    def __next__(self) -> tuple[str, int]:
        while self.__i_next < len(self.__items) and isinstance(
            self.__items[self.__i_next], EmptySlot
        ):
            self.__i_next += 1

        if self.__i_next >= len(self.__items):
            self.__i_next = 0
            raise StopIteration

        val = self.__items[self.__i_next].to_tuple()  # pyright: ignore
        self.__i_next += 1
        return val

    def __iter__(self):
        return self

    def keys(self) -> Iterator[str]:
        for item in self.__items:
            if not isinstance(item, EmptySlot):
                yield item.key

    def values(self) -> Iterator[int]:
        for item in self.__items:
            if not isinstance(item, EmptySlot):
                yield item.val


def tests():

    print("HashMap.__len__", end="")
    n = 0
    items = [(str(i), i) for i in range(n)]
    hm = HashMap(n, items)
    got = len(hm)
    assert got == n, f"Expected length to be {n} but got {got}."
    n = 5
    items = [(str(i), i) for i in range(n)]
    hm = HashMap(n, items)
    got = len(hm)
    assert got == n, f"Expected length to be {n} but got {got}."
    n = 5
    items = [(str(i), i) for i in range(n)]
    hm = HashMap(0, items)
    got = len(hm)
    assert got == n, f"Expected length to be {n} but got {got}."
    print(": tests passed!")

    print("HashMap.__bool__", end="")
    n = 0
    items = [(str(i), i) for i in range(n)]
    hm = HashMap(n, items)
    assert not hm, f"Expected hash map to be empty."
    n = 3
    items = [(str(i), i) for i in range(n)]
    hm = HashMap(n, items)
    assert hm, f"Expected hash map to not be empty."
    print(": tests passed!")

    print("HashMap.__getitem__", end="")
    n = 5
    items = [(str(i), i) for i in range(n)]
    hm = HashMap(n, items)
    for i in range(n):
        expected = i
        got = hm[str(i)]
        assert got == expected, f"Expected {expected}, but got {got}."
    n = 0
    items = [(str(i), i) for i in range(n)]
    hm = HashMap(n, items)
    got_error = False
    try:
        hm["key"]
    except (KeyError):
        got_error = True
    assert got_error, "Expected to get a KeyError."
    try:
        hm[1]
    except (TypeError):
        got_error = True
    assert got_error, "Expected to get a TypeError."
    print(": tests passed!")

    print("HashMap.__setitem__", end="")
    n = 3
    items = [(str(i), i) for i in range(n)]
    hm = HashMap(n, items)
    hm["0"] = 10
    got = len(hm)
    assert got == n, f"Expected length to be {n}, but got {got}."
    got = hm["0"]
    assert got == 10, f"Expected {n}, but got {got}."
    hm["3"] = 3
    got = len(hm)
    assert got == n + 1, f"Expected length to be {n+1}, but got {got}."
    got = hm["3"]
    assert got == 3, f"Expected {n}, but got {got}."
    n = 0
    items = [(str(i), i) for i in range(n)]
    hm = HashMap(n, items)
    got_error = False
    try:
        hm[1] = 1
    except (TypeError):
        got_error = True
    assert got_error, "Expected to get a TypeError."
    print(": tests passed!")

    print("HashMap.__delitem__", end="")
    n = 3
    items = [(str(i), i) for i in range(n)]
    hm = HashMap(n, items)
    del hm["0"]
    expected = n - 1
    got = len(hm)
    assert got == expected, f"Expected length to be {expected}, but got {got}."
    n = 3
    items = [(str(i), i) for i in range(n)]
    hm = HashMap(n, items)
    del hm["2"]
    expected = n - 1
    got = len(hm)
    assert got == expected, f"Expected length to be {expected}, but got {got}."
    got_error = False
    try:
        del hm[1]
    except (TypeError):
        got_error = True
    assert got_error, "Expected to get a TypeError."
    print(": tests passed!")

    print("HashMap.__eq__", end="")
    n = 10
    items = [(str(i), i) for i in range(n)]
    hm1 = HashMap(n, items)
    hm2 = HashMap(n, items)
    assert hm1 == hm2, "Expected hash maps to be equal."
    n = 5
    items = [(str(i), i) for i in range(n)]
    hm2 = HashMap(n, items)
    assert hm1 != hm2, "Expected hash maps to not be equal."
    print(": tests passed!")

    print("HashMap.__iter__/HashMap.__next__", end="")
    n = 10
    items = [(str(i), i) for i in range(n)]
    hm1 = HashMap(n, items)
    got = []
    for k, v in hm1:
        got.append((k, v))
    hm2 = HashMap(n, got)
    assert hm1 == hm2, "Expected hash maps to be equal."
    print(": tests passed!")

    print("All tests passed!")


if __name__ == "__main__":

    tests()
    pass
