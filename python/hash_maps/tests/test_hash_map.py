import unittest

from hash_maps import HashMap


class TestHashMap(unittest.TestCase):
    def test_init(self):
        hm = HashMap()
        self.assertFalse(bool(hm))
        self.assertEqual(len(hm), 0)

        hm = HashMap([("a", 1), ("b", 2), ("c", 3)])
        self.assertTrue(bool(hm))
        self.assertEqual(len(hm), 3)

    def test_get_set_del(self):
        hm = HashMap()
        ks = ["a", "b", "c", "d", "e"]
        vs = [1, 2, 3, 4, 5]
        for k, v in zip(ks, vs):
            hm[k] = v
            self.assertEqual(len(hm), v)
            self.assertEqual(hm[k], v)

        self.assertRaises(KeyError, lambda: hm["f"])

        expected_size = 5
        for k in ks:
            del hm[k]
            expected_size -= 1
            self.assertEqual(len(hm), expected_size)

    def test_iter(self):
        hm = HashMap()
        ks = ["a", "b", "c", "d", "e"]
        vs = [1, 2, 3, 4, 5]
        for c, i in zip(ks, vs):
            hm[c] = i

        self.assertEqual(set(hm.keys()), set(ks))
        self.assertEqual(set(hm.values()), set(vs))


def main():
    unittest.main()


if __name__ == "__main__":
    main()
