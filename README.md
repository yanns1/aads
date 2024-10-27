# Algorithms and data structures

## TODO

### python

- Implement radix sort on list of integers and strings.
- Implement all sorting algorithms for each kind of list (when it makes sense):
    selection sort, insertion sort, bubble sort, merge sort, quicksort
- Implement recursive and iterative versions when possible.
- For walk methods on trees, add a "traversal" parameter that can take values:
    - "depth-first pre-order"
    - "depth-first in-order"
    - "depth-first post-order"
    - "depth-first reverse pre-order"
    - "depth-first reverse in-order"
    - "depth-first reverse post-order"
    - "breadth-first"
  and adapt implementations accordingly.
- Replace LCRSNode by a node class and a Tree class (then adapt tests).
- Make implementations as generic as possible.

## Resources

- [FrontendMasters course by ThePrimeagen](https://frontendmasters.com/courses/algorithms/):
    Too shallow for me at this point (2023-08-21), but learned some new things:
    LRU cache, ring buffer, the two crystal balls problem.
- [Solutions for "Introduction to Algorithms by Charles E. Leiserson, Clifford Stein, Ronald Rivest, and Thomas H. Cormen" (CLRS)](https://github.com/gzc/CLRS)
- Cours "Algorithmes et programmation" en info3, 1er semestre.

## List of data structures

- Lists:
    - array list (or vector)
    - linked list (singly-linked, doubly-linked, doubly-linked and circular)
- Stack
- Queue
- Double-ended queue (deque)
- Associative array:
    - Hash map
- Set, Bag (or multiset)
- Priority queue (min/max binary heap)
- Binary tree
- Binary search tree
- Self-balancing trees:
    - Red-black tree
    - AVL tree
    - B-tree
- Circular/Ring buffer
- Graph ((un)directed, (un)weighted, with/without loops, etc.)
    - Adjacency list representation
    - Adjacency matrix representation
    - Incidence matrix representation
- Gap buffer (and the generalization <https://en.wikipedia.org/wiki/Zipper_(data_structure)>)
- [Piece table](https://en.wikipedia.org/wiki/Piece_table)
- [Rope](https://en.wikipedia.org/wiki/Rope_(data_structure))

## List of algorithms

- Sorting:
    - Insertion sort
    - Selection sort
    - Bubble sort
    - Merge sort
    - Quicksort

## About ongoing research on algorithms and data structures

See <https://qr.ae/pvlEYE> or <https://www.quora.com/What-are-the-ongoing-researches-on-algorithms-and-data-structures>.
The take-home message is that the usual subject of study called "algorithms and data structures" is
about algorithms and data structures on (sequential) computers with a Von Neumann architecture.
Designing and implementing algorithms and data structures for systems capable of running code in
parallel, or for quantum computers, is yet another problem. Remaining on Von Neumann-like
computers, it seems that most of the research now focuses on quite narrow problems, for example:
image processing, graphics algorithms, speech and language processing, security/cryptographic
algorithms, numerical algorithms, machine learning, etc.
