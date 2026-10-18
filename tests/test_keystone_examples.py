"""Deterministic finite witnesses for keystone chapter worked examples.

These tests replay illustrative calculations; they are NOT proofs of
complexity-class theorems and do not replace independent editorial review.
"""
from collections import deque
from itertools import permutations, product
import math
import unittest


def reach(adj, start, target):
    todo = deque([start])
    seen = {start}
    while todo:
        u = todo.popleft()
        if u == target:
            return True
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                todo.append(v)
    return False


def bounded_reach(adj, u, v, max_steps):
    # Actual breadth-first bounded walk reachability.
    reachable = {u}
    if u == v:
        return True
    for _ in range(max_steps):
        reachable = reachable | {w for a in reachable for w in adj[a]}
        if v in reachable:
            return True
    return False


def midpoint_reach(adj, u, v, depth):
    # Savitch's bounded-midpoint recurrence, for finite graphs only.
    if depth == 0:
        return u == v or v in adj[u]
    for m in range(len(adj)):
        if midpoint_reach(adj, u, m, depth - 1) and midpoint_reach(
            adj, m, v, depth - 1
        ):
            return True
    return False


class KeystoneExampleReplay(unittest.TestCase):
    def test_c01_tsp_four_city_example(self):
        cities = "ABCD"
        edge_weights = {
            frozenset("AB"): 2,
            frozenset("BC"): 2,
            frozenset("CD"): 2,
            frozenset("DA"): 2,
            frozenset("AC"): 7,
            frozenset("BD"): 7,
        }
        distinct = set()
        tour_weights = []
        for order in permutations(cities[1:]):
            seq = ("A",) + order
            reverse = ("A",) + tuple(reversed(order))
            canonical = min(seq, reverse)
            if canonical in distinct:
                continue
            distinct.add(canonical)
            cycle = canonical + ("A",)
            tour_weights.append(
                sum(edge_weights[frozenset(pair)] for pair in zip(cycle, cycle[1:]))
            )
        self.assertEqual(sorted(tour_weights), [8, 18, 18])
        self.assertEqual(sum(w <= 9 for w in tour_weights), 1)
        self.assertEqual(sum(w <= 7 for w in tour_weights), 0)

    def test_c04_sat_positive_and_negative_examples(self):
        def phi(a, b, c):
            return (a or b) and ((not a) or c) and ((not b) or (not c))
        self.assertTrue(phi(True, False, True))
        self.assertTrue(phi(False, True, False))
        self.assertTrue(any(phi(*values) for values in product([False, True], repeat=3)))
        self.assertFalse(any(a and (not a) for a in (False, True)))

    def test_c05_undirected_to_directed_reachability(self):
        vertices = range(4)
        possible = [(a, b) for a in vertices for b in vertices if a < b]
        for pattern in product([False, True], repeat=len(possible)):
            undirected = [set() for _ in vertices]
            directed = [set() for _ in vertices]
            for include, (a, b) in zip(pattern, possible):
                if include:
                    undirected[a].add(b)
                    undirected[b].add(a)
                    directed[a].add(b)
                    directed[b].add(a)
            for a in vertices:
                for b in vertices:
                    self.assertEqual(reach(undirected, a, b),
                                     reach(directed, a, b))

    def test_c10_midpoint_recurrence(self):
        # Every directed graph on three vertices, including self-loops.
        for bits in product([False, True], repeat=9):
            graph = [set() for _ in range(3)]
            for enabled, (u, v) in zip(bits, product(range(3), repeat=2)):
                if enabled:
                    graph[u].add(v)
            for depth in range(3):
                for u in range(3):
                    for v in range(3):
                        self.assertEqual(
                            midpoint_reach(graph, u, v, depth),
                            bounded_reach(graph, u, v, 2**depth),
                        )

    def test_c15_grover_input_size_warning(self):
        # Square-root of an exponential domain is still exponential.
        for n in range(0, 31, 2):
            N = 2**n
            self.assertEqual(math.isqrt(N), 2**(n // 2))
            self.assertEqual(math.isqrt(N)**2, N)

    def test_c20_sat_is_decidable_by_finite_enumeration(self):
        def sat(num_vars, predicate):
            return any(predicate(bits) for bits in product([False, True], repeat=num_vars))
        self.assertTrue(sat(2, lambda x: x[0] or x[1]))
        self.assertFalse(sat(1, lambda x: x[0] and not x[0]))



class KeystoneNavigationRegression(unittest.TestCase):
    def test_six_chapter_numbered_heading_ids_are_css_safe(self):
        from pathlib import Path
        import re
        root=Path(__file__).resolve().parents[1]
        for n in ("01", "04", "05", "10", "15", "20"):
            source=(root/"chapters"/f"C{n}.md").read_text(encoding="utf-8")
            headers=re.findall(r"^## (.+)$",source,re.M)
            self.assertGreaterEqual(sum(h.startswith("Section ") for h in headers),6,n)
            self.assertFalse(any(re.match(r"^[0-9]",h) for h in headers),n)

if __name__ == "__main__":
    unittest.main()
