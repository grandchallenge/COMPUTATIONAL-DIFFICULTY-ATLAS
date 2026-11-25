"""Finite regressions for new examples, not proofs of general theorems."""
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

def branch(edges, k):
    if k < 0:
        return False
    if not edges:
        return True
    if k == 0:
        return False
    return any(branch(tuple(e for e in edges if v not in e), k-1) for v in edges[0])

def matching_cover(edges):
    cover = set()
    for u, v in edges:
        if u not in cover and v not in cover:
            cover.update((u, v))
    return cover

class Completion(unittest.TestCase):
    def test_graph_examples_exhaustive(self):
        for n in range(6):
            V = range(n)
            pairs = list(combinations(V, 2))
            for mask in range(1 << len(pairs)):
                edges = [e for i,e in enumerate(pairs) if mask >> i & 1]
                optimum = next(k for k in range(n+1)
                    if any(all(u in s or v in s for u,v in edges)
                           for s in combinations(V,k)))
                for k in range(n+1):
                    self.assertEqual(branch(edges,k), optimum <= k)
                self.assertFalse(branch(edges,-1))
                s = matching_cover(edges)
                self.assertTrue(all(u in s or v in s for u,v in edges))
                self.assertLessEqual(len(s),2*optimum)

    def test_average_example(self):
        for n in range(21):
            self.assertEqual(Fraction(1,2**n)*2**n,1)
        # pushforward from four equiprobable inputs to two outputs
        D = [Fraction(1,4)]*4
        E = [Fraction(1,4),Fraction(3,4)]
        f = [0,0,0,1]
        for cost in product(range(5),repeat=2):
            self.assertLessEqual(sum(D[x]*cost[f[x]] for x in range(4)),
                                 3*sum(p*c for p,c in zip(E,cost)))

    def test_parity_shortcut(self):
        # all assignments on a complete graph of four vertices
        edges = list(combinations(range(4),2))
        charges = set()
        for bits in product((0,1),repeat=len(edges)):
            charges.add(tuple(sum(b for e,b in zip(edges,bits) if v in e)%2
                              for v in range(4)))
        self.assertEqual(charges,{c for c in product((0,1),repeat=4) if sum(c)%2==0})

    def test_chapter_contract(self):
        for n in range(1,24):
            p = ROOT/"chapters"/f"C{n:02}.md"
            self.assertTrue(p.is_file(),str(p))
            s = p.read_text()
            self.assertTrue(s.startswith("# C"),p.name)
            self.assertRegex(s,r"(?im)^## .*Exercises")
            self.assertRegex(s,r"(?im)^## .*Map update")
        for n in (17,18,19,21,22,23):
            s=(ROOT/"chapters"/f"C{n:02}.md").read_text()
            self.assertIn("Editorial candidate",s)
            self.assertIn("Primary sources",s)

if __name__=="__main__":
    unittest.main()
