import unittest
from io import StringIO

from graphs import ALSimpleGraph


class TestALSimpleGraph(unittest.TestCase):
    def test_init(self):
        g = ALSimpleGraph()
        self.assertEqual(g.order, 0)
        self.assertEqual(g.size, 0)

    def test_node_and_edge_insertion_and_removal(self):
        # Graph with one node.
        g = ALSimpleGraph()
        k1 = g.add_node(1)
        self.assertEqual(g.order, 1)
        self.assertEqual(g.size, 0)
        self.assertEqual(g.get_node_value(k1), 1)
        self.assertEqual(g.get_node_key(1), k1)
        g.remove_node(k1)
        self.assertEqual(g.order, 0)
        self.assertEqual(g.size, 0)
        self.assertEqual(g.get_node_value(k1), None)
        self.assertEqual(g.get_node_key(1), None)

        # Graph with 4 nodes and 0 edges.
        g = ALSimpleGraph()
        k1 = g.add_node(1)
        k2 = g.add_node(2)
        k3 = g.add_node(3)
        k4 = g.add_node(4)
        self.assertEqual(g.order, 4)
        self.assertEqual(g.size, 0)
        self.assertEqual(g.get_node_value(k1), 1)
        self.assertEqual(g.get_node_key(1), k1)
        self.assertEqual(g.get_node_value(k2), 2)
        self.assertEqual(g.get_node_key(2), k2)
        self.assertEqual(g.get_node_value(k3), 3)
        self.assertEqual(g.get_node_key(3), k3)
        self.assertEqual(g.get_node_value(k4), 4)
        self.assertEqual(g.get_node_key(4), k4)
        g.remove_node(k1)
        self.assertEqual(g.order, 3)
        self.assertEqual(g.size, 0)
        self.assertEqual(g.get_node_value(k1), None)
        self.assertEqual(g.get_node_key(1), None)
        g.remove_node(k2)
        self.assertEqual(g.order, 2)
        self.assertEqual(g.size, 0)
        self.assertEqual(g.get_node_value(k2), None)
        self.assertEqual(g.get_node_key(2), None)
        g.remove_node(k3)
        self.assertEqual(g.order, 1)
        self.assertEqual(g.size, 0)
        self.assertEqual(g.get_node_value(k3), None)
        self.assertEqual(g.get_node_key(3), None)
        g.remove_node(k4)
        self.assertEqual(g.order, 0)
        self.assertEqual(g.size, 0)
        self.assertEqual(g.get_node_value(k4), None)
        self.assertEqual(g.get_node_key(4), None)

        # K_4
        g = ALSimpleGraph()
        k1 = g.add_node(1)
        k2 = g.add_node(2)
        k3 = g.add_node(3)
        k4 = g.add_node(4)
        g.add_edge(k1, k1)  # should do nothing, loops not allowed
        g.add_edge(k1, k2)
        g.add_edge(k1, k3)
        g.add_edge(k1, k4)
        g.add_edge(k2, k3)
        g.add_edge(k2, k4)
        g.add_edge(k3, k2)
        g.add_edge(k3, k4)
        self.assertEqual(g.order, 4)
        self.assertEqual(g.size, 6)
        self.assertEqual(g.get_node_value(k1), 1)
        self.assertEqual(g.get_node_key(1), k1)
        self.assertEqual(g.get_node_value(k2), 2)
        self.assertEqual(g.get_node_key(2), k2)
        self.assertEqual(g.get_node_value(k3), 3)
        self.assertEqual(g.get_node_key(3), k3)
        self.assertEqual(g.get_node_value(k4), 4)
        self.assertEqual(g.get_node_key(4), k4)
        g.remove_edge(k1, k2)
        self.assertEqual(g.order, 4)
        self.assertEqual(g.size, 5)
        g.remove_edge(k2, k1)  # should do nothing, edge already deleted
        self.assertEqual(g.order, 4)
        self.assertEqual(g.size, 5)
        g.remove_edge(k4, k1)
        self.assertEqual(g.order, 4)
        self.assertEqual(g.size, 4)
        g.remove_node(k1)
        self.assertEqual(g.order, 3)
        self.assertEqual(g.size, 3)
        self.assertEqual(g.get_node_value(k1), None)
        self.assertEqual(g.get_node_key(1), None)
        k1 = g.add_node(1)
        self.assertEqual(g.order, 4)
        self.assertEqual(g.size, 3)
        self.assertEqual(g.get_node_value(k1), 1)
        self.assertEqual(g.get_node_key(1), k1)
        k5 = g.add_node(5)
        self.assertEqual(g.order, 5)
        self.assertEqual(g.size, 3)
        self.assertEqual(g.get_node_value(k1), 1)
        self.assertEqual(g.get_node_key(1), k1)
        self.assertEqual(g.get_node_value(k5), 5)
        self.assertEqual(g.get_node_key(5), k5)
        g.remove_node(k1)
        g.remove_node(k5)
        g.remove_node(k2)
        self.assertEqual(g.order, 2)
        self.assertEqual(g.size, 1)
        self.assertEqual(g.get_node_value(k2), None)
        self.assertEqual(g.get_node_key(2), None)
        g.remove_node(k3)
        self.assertEqual(g.order, 1)
        self.assertEqual(g.size, 0)
        self.assertEqual(g.get_node_value(k3), None)
        self.assertEqual(g.get_node_key(3), None)
        g.remove_node(k4)
        self.assertEqual(g.order, 0)
        self.assertEqual(g.size, 0)
        self.assertEqual(g.get_node_value(k4), None)
        self.assertEqual(g.get_node_key(4), None)

    def test_depth_first_traversal(self):
        # NOTE: Testing a depth-first traversal implementation for a graph is tricky
        # because the depth-first property alone doesn't completely determine the order
        # of traversal of the nodes. The root (arbitrarily chosen node to start the
        # traversal) and the order of visit of adjacent nodes also impact the order of
        # traversal.
        # Take this "diamond" graph, for example:
        #         O
        #       /  \
        #      1    2
        #      \   /
        #        3
        # Depending on the root we choose and the order of visit of adjacent nodes,
        # we can get multiple valid depth-first traversals:
        #   1. By taking 0 as root and visiting adjacent nodes from "left" to "right",
        #      the traversal order is: 0 1 3 2.
        #   2. By taking 0 as root and visiting adjacent nodes from "right" to "left",
        #      the traversal order is: 0 2 3 1.
        #   3. By taking 1 as root and visiting adjacent nodes from "left" to "right",
        #      the traversal order is: 1 3 2 0.
        #   4. etc.
        # The only thing required for the depth-first property is to *not* produce
        # breadth-first traversals such as:
        #   - 0 1 2 3 (0 as root, from "left" to "right")
        #   - 1 0 3 2 (1 as root, from "right" to "left")
        #   - etc.
        #
        # A better and ultimately more robust way to ensure that a depth-first traversal
        # implementation is valid would be to formally check it.
        # But we won't do that here. Instead, we rely on implementation details that are
        # *not* part of the API of ALSimpleGraph in order reduce the possible traversals
        # to one.

        # Empty graph
        g1 = ALSimpleGraph()

        # Graph with only one node.
        g2 = ALSimpleGraph()
        g2.add_node(0)

        # K_3
        g3 = ALSimpleGraph()
        n = 3
        ks = []
        for i in range(n):
            ks.append(g3.add_node(i))
        for i in range(n):
            for j in range(i + 1, n):
                g3.add_edge(ks[i], ks[j])

        # K_4
        g4 = ALSimpleGraph()
        n = 4
        ks = []
        for i in range(n):
            ks.append(g4.add_node(i))
        for i in range(n):
            for j in range(i + 1, n):
                g4.add_edge(ks[i], ks[j])

        # K_10
        g5 = ALSimpleGraph()
        n = 10
        ks = []
        for i in range(n):
            ks.append(g5.add_node(i))
        for i in range(n):
            for j in range(i + 1, n):
                g5.add_edge(ks[i], ks[j])

        # "Diamond" graph
        #         O
        #       /  \
        #      1    2
        #      \   /
        #        3
        g6 = ALSimpleGraph()
        k0 = g6.add_node(0)
        k1 = g6.add_node(1)
        k2 = g6.add_node(2)
        k3 = g6.add_node(3)
        g6.add_edge(k0, k1)
        g6.add_edge(k0, k2)
        g6.add_edge(k1, k3)
        g6.add_edge(k2, k3)

        # "Almost tree" graph
        #                _____0_____
        #               /     |     \
        #       ______1       2      3
        #      /      |       |      |
        #     4       5       6      |
        #             |______________|
        g7 = ALSimpleGraph()
        k0 = g7.add_node(0)
        k1 = g7.add_node(1)
        k2 = g7.add_node(2)
        k3 = g7.add_node(3)
        k4 = g7.add_node(4)
        k5 = g7.add_node(5)
        k6 = g7.add_node(6)
        g7.add_edge(k0, k1)
        g7.add_edge(k0, k2)
        g7.add_edge(k0, k3)
        g7.add_edge(k1, k4)
        g7.add_edge(k1, k5)
        g7.add_edge(k2, k6)
        g7.add_edge(k3, k5)

        test_cases = [
            (g1.depth_first_traversal_rec, ""),
            (g1.depth_first_traversal_it, ""),
            (g2.depth_first_traversal_rec, "0"),
            (g2.depth_first_traversal_it, "0"),
            (g3.depth_first_traversal_rec, "0 1 2"),
            (g3.depth_first_traversal_it, "0 2 1"),
            (g4.depth_first_traversal_rec, "0 1 2 3"),
            (g4.depth_first_traversal_it, "0 3 2 1"),
            (g5.depth_first_traversal_rec, "0 1 2 3 4 5 6 7 8 9"),
            (g5.depth_first_traversal_it, "0 9 8 7 6 5 4 3 2 1"),
            (g6.depth_first_traversal_rec, "0 1 3 2"),
            (g6.depth_first_traversal_it, "0 2 3 1"),
            (g7.depth_first_traversal_rec, "0 1 4 5 3 2 6"),
            (g7.depth_first_traversal_it, "0 3 5 1 4 2 6"),
        ]

        for depth_first_traversal, expected_result in test_cases:
            s = StringIO()
            depth_first_traversal(lambda v: s.write(f"{v} "))
            self.assertEqual(s.getvalue().strip(), expected_result)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
