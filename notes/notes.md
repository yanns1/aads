---
title: Algorithms and data structures
author: Yann Salmon
date: 2023-08-21
---

# Algorithms and data structures

## Resources

- [FrontendMasters course by ThePrimeagen](https://frontendmasters.com/courses/algorithms/): Too shallow for me at this point (2023-08-21), but learned some new things: LRU cache, ring buffer, the two crystal balls problem.
- Cours "Algorithmes et programmation" en info3, 1er semestre

## Array List

An array is a sequence of contiguous memory slots, all having the same size.
This is close to the simplest data structure we can make, and this is a fundamental one.

An array list is an array that can grow, much like a list does.
This works by allocating a first array, usually of a small size (but depends on user input), and reallocating a bigger one (often bigger by a factor of two) when the first one is full.
All of this is hidden to the user, of course.
The implementation can vary quite a bit: - Instead of reallocating, which requires copying the previous array to the new array, we can allocate a new array and link the previous one to it. It's however not as fast when getting and setting, and can be tricky to manage on the implementation side. - We could make the ArrayList shrink whenever we find it not filled enough.

### Time complexity

| Operation       | Best case | Worst case | Comments                               |
| --------------- | --------- | ---------- | -------------------------------------- |
| Set by index    | $O(1)$    | $O(1)$     |                                        |
| Get by index    | $O(1)$    | $O(1)$     |                                        |
| Get by value    | $O(1)$    | $O(n)$     |                                        |
| Insert at index | $O(1)$    | $O(n)$     |                                        |
| Prepend         | $O(n)$    | $O(n)$     | correspond to worst case of insert     |
| Append          | $O(1)$    | $O(1)$     | correspond to best case of insert      |
| Extend          | $O(n)$    | $O(n)$     | where n is the size of the array added |
| Remove by index | $O(1)$    | $O(n)$     |                                        |

An array (un tableau) is a sequence of (n) contiguous memory slots of the same size (i.e. that can contain the same number of bits). So accessing or changing a value in the k-th slot (so via indexing) is O(1), because you only need to multiply the address of the first slot by k to access that particular slot.

Searching (aka. get by value) is O(n) in the worst case. If the array is not sorted, there is no better alternative than linear search, and you may need to read all memory slots to find the value searched, if that value is in the last slot, or if it is not in the array.
In the average case, it is O(n/2), if we assume that it is equally likely for each value to be searched.

For insertion, it depends on the place where we want to insert. If we insert at the end of the array (append), then it is O(1): we just have to reach the slot next to the last, and write our value there (provided that the array has been initialized with a sufficient number of slots). In any other case, we need to reach the slot where we want to write (still O(1)), but also move all the already filled slots after "one step to the right". This requires starting from the end of the array, and for a given slot, copy it in the slot on its right, until we have reached the slot where we want to right our value. In the worst case, inserting at the beginning of the array (prepend), it is O(n). In the average case, it is O(n/2).

For deletion, it is similar to insertion, but instead of shifting the slots on the right, we shift them on the left.

## (Doubly) Linked List

### Time complexity

| Operation        | Best case | Worst case | Comments                     |
| ---------------- | --------- | ---------- | ---------------------------- |
| Set from cell    | $O(1)$    | $O(1)$     |                              |
| Get from cell    | $O(1)$    | $O(1)$     |                              |
| Get by index     | $O(1)$    | $O(n)$     |                              |
| Insert from cell | $O(1)$    | $O(1)$     |                              |
| Insert by index  | $O(1)$    | $O(n)$     |                              |
| Remove from cell | $O(1)$    | $O(1)$     |                              |
| Remove by index  | $O(1)$    | $O(n)$     |                              |
| Extend           | $O(n)$    | $O(n)$     | n the size of the list added |

Linked lists are better than arrays for frequent insertions/removals, given that there is no need for reallocation.
However, they are bad for random access, access by index.

### Links

- https://en.wikipedia.org/wiki/Linked_list

## Stack (LIFO)

LIFO (Last In First Out): le dernier élément inséré/le plus récent est le premier à sortir.

Pour une pile, il faut insérer et supprimer en tête (ou en queue, mais insertion et suppression du même côté).
Le tableau comme la liste sont en $O(1)$ pour ces deux opérations, mais le tableau est légèrement plus simple que la liste. La liste serait un peu "overkill".
Cependant, la liste à l'avantage d'être de taille indéfinie.

## Queue (FIFO)

FIFO (First In First Out): le premier élément inséré/le plus vieux est le premier à sortir).

Pour une file, c'est la tête qui sort en premier et on insère à la queue.

Même réflexion que pour la pile concernant son implémentation avec le tableau ou la liste, simplement ici on est obligé d'insérer ou supprimer à la queue, et le tableau est en O(n) dans ce cas. On préférera donc la liste.

## Hash map

A hash map is an implementation of the concept of _associative array_ (or dictionanry), that is a mapping from some keys to some values. One key maps to exactly one value, which means that an associative array corresponds to a mathematical function from a finite set to another finite set.

Another implementation of associative arrays are self-balancing binary search trees, such as AVL trees.
Une autre implémentation du tableau associatif est l'arbre équilibré (il y en a d'autres mais ces deux-là semblent être les plus efficaces).

We can see the traditional array as a special associative array, where keys are indices.

Another use of hash maps is to implement the mathematical equivalent of a set. We can do this by using the set values as keys.

### Time complexity

| Operation | Best case | Average case | Worst case | Comments                                                                                                                                                      |
| --------- | --------- | ------------ | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Get       | $O(1)$    | $O(1)$       | $O(1)$     |                                                                                                                                                               |
| Set       | $O(1)$    | $O(1)$       | $O(n)$     | average case under the assumptions that the hash function distributes outputs uniformly, avoiding too much collisions, and that the load factor is reasonable |
| Delete    | $O(1)$    | $O(1)$       | $O(1)$     |                                                                                                                                                               |

### Links

- https://en.wikipedia.org/wiki/Hash_table
- https://en.wikipedia.org/wiki/Associative_array
- https://en.wikipedia.org/wiki/Hash_function
- https://en.wikipedia.org/wiki/Open_addressing
- https://en.wikipedia.org/wiki/Self-balancing_binary_search_tree
- https://en.wikipedia.org/wiki/AVL_tree

## Binary Tree

### Time complexity

On considère l'arbre non-ordré, non-équilibré, non-dégénéré (càd n'est pas une liste) et qu'il est complet ou presque complet.

| Operation         | Best case      | Worst case     | Comments                                                            |
| ----------------- | -------------- | -------------- | ------------------------------------------------------------------- |
| Get/Set from node | $O(1)$         | $O(1)$         |                                                                     |
| Get/Set by index  | $O(n)$         | $O(n)$         |                                                                     |
| Get/Set by value  | $O(n)$         | $O(n)$         |                                                                     |
| Insert            | $O(\log_2(n))$ | $O(\log_2(n))$ | le pire des cas serait en $O(n)$ si arbre dégénéré (i.e. une liste) |
| Remove by value   | $O(\log_2(n))$ | $O(n)$         |                                                                     |

Insérer dans un arbre non-ordré et non-équilibré se fait en bas de l'arbre: on insére l'élément en tant que feuille. Il faut donc `<hauteur de l'arbre>` étapes, càd $\log_2(n)$ où $n$ est le nombre de noeuds de l'arbre.

### Links

- https://en.wikipedia.org/wiki/Binary_tree

## Binary Search Tree

### Time complexity

L'arbre est ordré, a priori non-équilibré.
On considère de plus qu'il n'est pas dégénéré (càd n'est pas une liste) et qu'il est complet ou presque complet.

| Operation         | Best case      | Worst case     | Comments                                                            |
| ----------------- | -------------- | -------------- | ------------------------------------------------------------------- |
| Get/Set from node | $O(1)$         | $O(1)$         |                                                                     |
| Get/Set by index  | $O(n)$         | $O(n)$         |                                                                     |
| Get/Set by value  | $O(\log_2(n))$ | $O(\log_2(n))$ | le pire des cas serait en $O(n)$ si arbre dégénéré (i.e. une liste) |
| Insert            | $O(\log_2(n))$ | $O(\log_2(n))$ | le pire des cas serait en $O(n)$ si arbre dégénéré (i.e. une liste) |
| Remove by value   | $O(\log_2(n))$ | $O(\log_2(n))$ |                                                                     |

Puisque l'arbre est ordré, on peut tirer avantage de la recherche dichotomique, et donc obtenir une insertion et suppression en $O(\log_2(n))$ même dans le pire des cas.

Même chose pour les arbres AVL, mais quand même mieux dans le cas moyen car cette fois-ci on est sûr qu'on aura pas affaire à un arbre déséquilibré (par ex. un arbre dégénéré!), ce qui peut rendre certaines opérations très coûteuses en temps dans certains cas.

## Binary Heap

Un tas binaire est un arbre binaire qui vérifie la propriété de tas: pour un ordre $<_o$, tout parent a une priorité inférieure à ses deux enfants selon $<_o$.

Si $<_o$ est `<=`, on parle de _min heap_ (la racine a la priorité minimale).

Si $<_o$ est `>=`, on parle de _max heap_ (la racine a la propriété maximale).

L'utilité de cette structure est dans son ordre partiel qui nous permet de facilement accéder à l'élément de priorité minimale selon $<_o$, en l'occurence la racine.

Le tas binaire permet d'implémenter la spécification qu'est la file de priorité: une file pour laquelle les éléments ont une priorité, et l'élément de priorité min./max. (selon un ordre) est servi en premier.

### Links

- https://en.wikipedia.org/wiki/Binary_heap
- https://en.wikipedia.org/wiki/Priority_queue

## Tradeoffs between data structures

On voit que la LinkedList est généralement plus efficace. Lorsque les cas d'utilisation consistent principalement à append et/ou à lire par indice, le tableau à l'avantage.
Mais si les insertions sont aléatoires (i.e. un peu n'importe où), la LinkedList est meilleure.

Lorsqu'il s'agit de faire beaucoup de recherches par valeur, les arbres sont plus intéressants, quoique le tableau avec recherche dichotomique est aussi bien (mais il faut trier le tableau).
Les arbres gardent cependant un avantage sur le tableau pour l'insertion. Les arbres ordrés et équilibrés permettent d'améliorer encore un peu plus les complexités des lectures/suppressions par valeur, mais au pris de réajustements plus ou moins coûteux lors de l'écriture, afin de garder l'arbre ordré/équilibré.

## Sort algorithms

### Quicksort

La méthode consiste à placer un élément du tableau (appelé pivot) à sa place définitive, en permutant tous les éléments de telle sorte que tous ceux qui sont inférieurs au pivot soient à sa gauche et que tous ceux qui sont supérieurs au pivot soient à sa droite.

Cette opération s'appelle le partitionnement. Pour chacun des sous-tableaux, on définit un nouveau pivot et on répète l'opération de partitionnement. Ce processus est répété récursivement, jusqu'à ce que l'ensemble des éléments soit trié.

On peut choisir le pivot arbitrairement (souvent le premier ou le dernier élément de la liste), mais pour rendre l'algorithme un peu plus résiliant aux entrées en $O(n^2)$, on peut choisir le pivot aléatoirement.

#### Links
- https://en.wikipedia.org/wiki/Quicksort
