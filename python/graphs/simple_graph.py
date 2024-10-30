from typing import Any, Callable


class ALSimpleGraph[T]:
    """
    A simple graph (i.e. unweighted, undirected graph containing
    no graph loops or multiple edges) implemented using an adjacency list.
    """

    def __init__(self):
        self._nodes: list[T | None] = []
        self._empty_slots: list[int] = []
        self._adj: list[set[int]] = []
        self._order: int = 0
        self._size: int = 0
        self._visited: set[int] = set()

    @property
    def order(self) -> int:
        """
        The order of the graph, i.e. its number of nodes/vertices.
        """
        return self._order

    @property
    def size(self) -> int:
        """
        The size of the graph, i.e. its number of edges.
        """
        return self._size

    def add_node(self, v: T) -> int:
        """
        Adds a new node with value *v* to the graph.

        Parameters
        ----------
        v
            The value of the new node.

        Returns
        -------
        `int`
            The "key" used to refer to the created node later on (which happens
            to be the index of the node in the adjacency list).
        """
        if self._empty_slots:
            k = self._empty_slots[-1]
            self._nodes[k] = v
            del self._empty_slots[-1]
        else:
            self._nodes.append(v)
            self._adj.append(set())
            k = self._order

        self._order += 1
        return k

    def remove_node(self, k: int):
        """
        Removes the node with key *k* from the graph.

        Parameters
        ----------
        k
            The key (aka. index in the adjacency list) of the node to remove.
        """
        # Remove node from the list of nodes and the adjacency list.
        # But don't delete, simply insert None, otherwise we would loose the property
        # of a node's key to be its index in the adjacency/nodes list, in addition
        # to deletion being computationally costly.
        # The downsides, however, are:
        #   1. Slightly increased complexity of the implementation because need to keep
        #      track of the empty slots and reuse them appropriately.
        #   2. We never shrink the adjacency/nodes list, even though it might sometimes
        #      make sense, when a lot of nodes got deleted.
        #      This could be considered a memory leak, but is unlikely to matter in
        #      most cases.
        self._nodes[k] = None
        for i in self._adj[k]:
            self._adj[i].remove(k)
        self._size -= len(self._adj[k])
        self._adj[k] = set()
        self._empty_slots.append(k)
        self._order -= 1

    def add_edge(self, k1: int, k2: int):
        """
        Adds an edge between node with key *k1* and node with key *k2*.

        Parameters
        ----------
        k1
        k2
        """
        # Loops are not allowaed.
        if k1 == k2:
            return

        # Edge between k1 and k2 already exists, so do nothing.
        # Multiple edges with the same source and target are not
        # allowed.
        if k2 in self._adj[k1]:
            return

        # Undirected edge so add neighbor to both k1 and k2.
        self._adj[k1].add(k2)
        self._adj[k2].add(k1)
        self._size += 1

    def remove_edge(self, k1: int, k2: int):
        """
        Removes the edge between node with key *k1* and node with key *k2*.

        Parameters
        ----------
        k1
        k2
        """
        if k2 not in self._adj[k1]:  # do nothing, edge k1 <-> k2 does not exist
            return

        self._adj[k1].remove(k2)
        self._adj[k2].remove(k1)
        self._size -= 1

    def get_node_value(self, k: int) -> T | None:
        """
        Returns the value of the node with key *k*,
        or `None` if the key is invalid (doesn't
        point to an existing node).

        Parameters
        ----------
        k

        Returns
        -------
        `T`
        """
        if k < 0 or k >= self._order:
            return None
        return self._nodes[k]

    def get_node_key(self, v: T) -> int | None:
        """
        Returns the key of the node with value *v*, or `None` if not found.

        Note
        ----
        If multiple nodes have the value *v*, there is no guarentee on which
        is going to be returned, it can be any of them.

        Parameters
        ----------
        v

        Returns
        -------
        `int | None`
        """
        for i in range(self._order):
            if self._nodes[i] == v:
                return i

        return None

    def depth_first_traversal_rec(self, f: Callable[[T], Any]):
        """
        Traverses the graph in a depth-first manner, running *f* on the value
        of each node encountered.

        Implementation details
        ----------------------
        This function traverses the graph recursively.

        Parameters
        ----------
        f
            A function to apply on the value of each node traversed.
        """
        if self._order == 0:
            return

        # Choose an arbitrary node as the "root" from which to start the traversal,
        # here the first node found in `self._nodes`.
        rk = 0
        while self._nodes[rk] is None:
            rk += 1

        self._visited = set()
        self._depth_first_traversal_rec(f, rk)

    def _depth_first_traversal_rec(self, f: Callable[[T], Any], rk: int):
        """
        Traverses the graph in a depth-first manner, running *f* on the value
        of each node encountered.

        Implementation details
        ----------------------
        This function traverses the graph recursively.

        Parameters
        ----------
        f
            A function to apply on the value of each node traversed.
        rk
            The key of the "root" node, i.e. the node from which to
            start the traversal.
        """
        f(self._nodes[rk])  # type: ignore
        self._visited.add(rk)
        for i in self._adj[rk]:
            if i not in self._visited:
                self._depth_first_traversal_rec(f, i)

    def depth_first_traversal_it(self, f: Callable[[T], Any]):
        """
        Traverses the graph in a depth-first manner, running *f* on the value
        of each node encountered.

        Implementation details
        ----------------------
        This function traverses the graph iteratively.

        Parameters
        ----------
        f
            A function to apply on the value of each node traversed.
        """
        if self._order == 0:
            return

        # Choose an arbitrary node as the "root" from which to start the traversal,
        # here the first node found in `self._nodes`.
        rk = 0
        while self._nodes[rk] is None:
            rk += 1

        self._visited = set()
        stack = [rk]
        while stack:
            k = stack.pop()

            if k in self._visited:
                continue

            f(self._nodes[k])  # type: ignore
            self._visited.add(k)

            # NOTE: Because we use sets instead of lists to store adjacent vertices
            # (faster for checking the existence of an edge or removing one), the
            # order of iteration over the adjacent vertices is undeterministic.
            # If we were to use lists, we could guarantee the user that adjacent
            # vertices would be visited from the first inserted to the last inserted.
            # But that is not a very useful guarantee, and one we usually don't
            # expect from a graph implementation.
            for i in self._adj[k]:
                if i not in self._visited:
                    stack.append(i)
