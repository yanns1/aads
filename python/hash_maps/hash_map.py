import math
from collections.abc import Callable, Iterator
from functools import partial
from typing import Union


def _encode(s: str) -> int:
    res = 0
    for char in s:
        res += ord(char)
    return res


def _compress(m: int, n: int) -> int:
    return n % m


def my_hash(m: int, s: str) -> int:
    return _compress(m, _encode(s))


def _py_hash(m: int, s: str) -> int:
    return _compress(m, hash(s))


def quadratic_probing(
    h: Callable[[int, str], int], max_size: int, k: str
) -> Iterator[int]:
    i = 0
    hval = h(max_size, k)
    c1 = 0.5
    c2 = 0.5
    c3 = 0
    while True:
        yield _compress(max_size, int(hval + c1 * i**2 + c2 * i + c3))
        i += 1


class Sentinel(object):
    def __init__(self, sentinel_name: str):
        self.__name = sentinel_name

    def __repr__(self):
        return self.__name


Deleted = Sentinel("Deleted")
EmptySlot = Union[None, Sentinel]


class Entry[T]:
    """
    An entry of `HashMap[T]`.

    Parameters
    ----------
    k
        The key of the entry.
    v
        The value of the entry.
    """

    def __init__(self, k: str, v: T):
        self.k: str = k
        self.v: T = v

    def __repr__(self) -> str:
        return "(" + str(self.k) + ", " + str(self.v) + ")"

    def to_tuple(self) -> tuple[str, T]:
        return (self.k, self.v)


class HashMap[T]:
    """
    A hash map using quadratic probing for collision resolution.

    Parameters
    ----------
    max_size
        (Optional) The maximum number of entries this hash map can contain.

        Defaults to `8`.
    items
        (Optional) A list of initial items to insert into this hash map.

        Defaults to `[]`.
    """

    def __init__(self, items: list[tuple[str, T]] = [], max_size: int = 8):
        if len(items) > max_size:
            max_size = len(items)

        # Pour un fonctionnement optimal du sondage quadratique, il faut que max_size
        # soit une puissance de deux. Il faut aussi size <= 2/3 max_size.
        # Ducoup, on remplace max_size par la puissance de deux supérieure la plus proche.
        # Cela revient à regarder le nombre de chiffres qu'il faudrait pour encoder
        # max_size en base 2, plus un.
        self._max_size = (
            2 if max_size == 0 else 2 ** math.ceil(math.log(max_size) / math.log(2))
        )

        self._probe = partial(quadratic_probing, my_hash)
        partial_probe = partial(self._probe, self._max_size)
        self._items: list[Entry | EmptySlot] = [None] * self._max_size
        for k, v in items:
            n_tests = 0
            gen_idx = partial_probe(k)
            idx = next(gen_idx)
            while n_tests <= self._max_size and self._items[idx] is not None:
                idx = next(gen_idx)
                n_tests += 1
            self._items[idx] = Entry(k, v)

        self._i_next = 0

    def __repr__(self) -> str:
        s = "{"
        is_empty = True
        is_first_item = True
        for i in range(self._max_size):
            item = self._items[i]
            if not isinstance(item, EmptySlot):
                if is_empty:
                    is_empty = False
                if is_first_item:
                    s += "\n"
                    is_first_item = False
                else:
                    s += ",\n"
                s += "  '" + item.k + "': " + str(item.v)

        if is_empty:
            s += "}"
        else:
            s += "\n}"

        return s

    def __len__(self) -> int:
        size = 0
        for item in self._items:
            if not isinstance(item, EmptySlot):
                size += 1
        return size

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

    def __iter__(self):
        return self

    def __next__(self) -> tuple[str, T]:
        while self._i_next < len(self._items) and isinstance(
            self._items[self._i_next], EmptySlot
        ):
            self._i_next += 1

        if self._i_next >= len(self._items):
            self._i_next = 0
            raise StopIteration

        v = self._items[self._i_next].to_tuple()  # type: ignore
        self._i_next += 1
        return v

    def __bool__(self) -> bool:
        return len(self) != 0

    def __getitem__(self, k) -> T:
        if not isinstance(k, str):
            raise TypeError("Key should be a string.")

        max_size = self._max_size
        gen_idx = self._probe(max_size, k)
        item = self._items[next(gen_idx)]
        n_tests = 0
        while (
            n_tests <= max_size
            and item is not None
            and (item == Deleted or item.k != k)  # type: ignore
        ):
            item = self._items[next(gen_idx)]
            n_tests += 1

        if n_tests > max_size or item is None or item == Deleted:
            raise KeyError(f"Key '{k}' not found.")

        return item.v  # type: ignore

    def __setitem__(self, k, v: T):
        if not isinstance(k, str):
            raise TypeError("Key should be a string.")

        max_size = self._max_size
        gen_idx = self._probe(max_size, k)
        idx = next(gen_idx)
        item = self._items[idx]
        n_tests = 0
        while (
            n_tests <= max_size and item is not None and item != Deleted and item.k != k  # type: ignore
        ):
            idx = next(gen_idx)
            item = self._items[idx]
            n_tests += 1

        if (
            item is None or item == Deleted or item.k == k  # type: ignore
        ):
            self._items[idx] = Entry(k, v)

        # Si plus de place dans la liste, il faut étendre la liste.
        # La méthode de réindexation choisie est simplement de reconstruire un hash map de zéro
        # avec la nouvelle taille prise en compte. Donc c'est essentiellement le même code
        # que __init__. Il doit y avoir moyen de réindexer plus efficacement. En plus je ne
        # fais pas le changement "in place". Je crée un nouveau hashmap.
        if n_tests > max_size:
            items: list[tuple[str, T]] = [(k, v)]
            for item in self._items:
                if item is not None and item != Deleted:
                    items.append(
                        (
                            item.k,  # type: ignore
                            item.v,  # type: ignore
                        )
                    )
            return HashMap(items, len(items))

        return self

    def __delitem__(self, k):
        if not isinstance(k, str):
            raise TypeError("Key should be a string.")

        max_size = self._max_size
        gen_idx = self._probe(max_size, k)
        idx = next(gen_idx)
        item = self._items[idx]
        n_tests = 0
        while (
            n_tests <= max_size
            and item is not None
            and (item == Deleted or item.k != k)  # type: ignore
        ):
            idx = next(gen_idx)
            item = self._items[idx]
            n_tests += 1

        if n_tests > max_size or item is None:
            # key not found
            raise KeyError(f"Key '{k}' not found.")
        else:
            # key has been found, so delete
            self._items[idx] = Deleted

    def keys(self) -> Iterator[str]:
        """
        Yields the keys of this hash map.
        """
        for item in self._items:
            if not isinstance(item, EmptySlot):
                yield item.k

    def values(self) -> Iterator[T]:
        """
        Yields the values of this hash map.
        """
        for item in self._items:
            if not isinstance(item, EmptySlot):
                yield item.v
