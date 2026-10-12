"""Bounded falsification tests for C06 3SAT-to-CLIQUE and Tseitin gates.

Finite tests support, but DO NOT replace, the two universal proofs in C06.
"""
from __future__ import annotations

from itertools import combinations, product
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
# signed ints 1..m represent positive variables; negatives represent negations


def truth(lit, bits):
    return (bool(bits[abs(lit)-1]) if lit > 0 else not bool(bits[-lit-1]))


def sat(clauses, variables=2):
    return any(all(any(truth(lit, bits) for lit in clause) for clause in clauses)
               for bits in product((False, True), repeat=variables))


def reduce_to_clique(clauses):
    if not clauses:
        return 1, [(0, 0, 1)], set()
    if any(not clause for clause in clauses):
        return 2, [(0, 0, 1)], set()
    vertices = [(i,j,lit) for i,clause in enumerate(clauses)
                for j,lit in enumerate(clause)]
    edges = set()
    for v,w in combinations(range(len(vertices)),2):
        i,_,lit = vertices[v]
        j,_,other = vertices[w]
        if i != j and lit != -other:
            edges.add((v,w))
    return len(clauses), vertices, edges


def has_clique(k, vertices, edges):
    for chosen in combinations(range(len(vertices)), k):
        if all((a,b) in edges for a,b in combinations(chosen,2)):
            return True
    return False


def gate_and(p, q, z):
    return ((not z or p) and (not z or q)
            and (z or not p or not q))


def gate_or(p, q, z):
    return ((z or not p) and (z or not q)
            and (not z or p or q))


def gate_not(p, z):
    return ((not z or not p) and (z or p))


class C06MathematicalReplay(unittest.TestCase):
    def test_gate_truth_tables(self):
        for p,q,z in product((False,True),repeat=3):
            self.assertEqual(gate_and(p,q,z), z == (p and q))
            self.assertEqual(gate_or(p,q,z), z == (p or q))
        for p,z in product((False,True),repeat=2):
            self.assertEqual(gate_not(p,z), z == (not p))

    def test_all_one_two_clause_3cnf_two_variables(self):
        literals=(-2,-1,1,2)
        options=[c for size in (1,2,3) for c in product(literals,repeat=size)]
        count=0
        for clauses in product(options,repeat=2):
            k, v, edges = reduce_to_clique(clauses)
            self.assertEqual(sat(clauses),has_clique(k,v,edges),clauses)
            count += 1
        self.assertEqual(count,84**2)

    def test_all_three_clauses_up_to_two_literals(self):
        literals=(-2,-1,1,2)
        options=[c for size in (1,2) for c in product(literals,repeat=size)]
        count=0
        for clauses in product(options,repeat=3):
            k, v, edges=reduce_to_clique(clauses)
            self.assertEqual(sat(clauses),has_clique(k,v,edges),clauses)
            count += 1
        self.assertEqual(count,20**3)

    def test_empty_and_contradictory(self):
        for clauses in ((), ((),), ((1,),(-1,)),((1,2),(-1,-2),(1,2))):
            k,v,edges=reduce_to_clique(clauses)
            self.assertEqual(sat(clauses),has_clique(k,v,edges))

    def test_total_encoding_reduction_invalid_strings(self):
        # This independent encoded-language adapter models the chapter's
        # explicit validation rule; parse-invalid inputs must be rejected.
        def map_input(encoded):
            if not isinstance(encoded, tuple):
                return 2, [(0, 0, 1)], set()
            if any(not isinstance(c, tuple) for c in encoded):
                return 2, [(0, 0, 1)], set()
            if any(not isinstance(v, int) or v == 0 or abs(v) > 2
                   for c in encoded for v in c):
                return 2, [(0, 0, 1)], set()
            return reduce_to_clique(encoded)
        for bad in ("not a formula", [(1,)], ((0,),), ((3,),), (4,)):
            k,vertices,edges = map_input(bad)
            self.assertFalse(has_clique(k,vertices,edges),bad)
        for valid in ((),((),),((1,),(-1,)),((1,2),(-1,2))):
            k,vertices,edges = map_input(valid)
            self.assertEqual(sat(valid),has_clique(k,vertices,edges),valid)

    def test_named_examples(self):
        yes = ((1,2,3),(-1,2,3),(1,-2,3))
        self.assertTrue(sat(yes,3))
        k,v,edges=reduce_to_clique(yes)
        self.assertTrue(has_clique(k,v,edges))
        no = ((1,),(-1,))
        self.assertFalse(sat(no,3))
        k,v,edges=reduce_to_clique(no)
        self.assertFalse(has_clique(k,v,edges))

    def test_manuscript_scope_and_renderable_math(self):
        chapter = (ROOT / "chapters/C06.md").read_text(encoding="utf-8")
        self.assertTrue(chapter.startswith("# C06"))
        for required in ("Cook–Levin", "3SAT to CLIQUE", "NP-hard",
                         "## Exercises", "## Map update",
                         "empty clause", "unproduced", "Figure obligation"):
            self.assertIn(required, chapter)
        displays=sum(s.strip()=="$$" for s in chapter.splitlines())
        self.assertGreater(displays,8)
        self.assertEqual(displays%2,0)
        self.assertFalse(any(ord(x)<32 and x not in "\n\t\r" for x in chapter))
        for line in chapter.splitlines():
            if line.strip() != "$$" and "$$" not in line:
                self.assertEqual(line.count("$")%2,0,line)


if __name__ == "__main__":
    unittest.main()
