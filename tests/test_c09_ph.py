"""Finite truth-table falsification checks for C09 quantifier alternation."""
from itertools import product
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
B=(False,True)


def exists_forall(rel):
    return any(all(rel(x,y) for y in B) for x in B)


def forall_exists(rel):
    return all(any(rel(x,y) for x in B) for y in B)


class C09QuantifierReplay(unittest.TestCase):
    def test_equality_depends_on_quantifier_order(self):
        rel=lambda x,y: x==y
        self.assertFalse(exists_forall(rel))
        self.assertTrue(forall_exists(rel))

    def test_named_exists_forall_witness(self):
        rel=lambda x,y: (x or y) and (x or not y)
        self.assertTrue(exists_forall(rel))
        self.assertFalse(all(rel(False,y) for y in B))
        self.assertTrue(all(rel(True,y) for y in B))

    def test_forall_exists_does_not_imply_exists_forall(self):
        count=0
        for values in product(B,repeat=4):
            d={(x,y):values[2*int(x)+int(y)] for x in B for y in B}
            rel=lambda x,y: d[(x,y)]
            if exists_forall(rel):
                self.assertTrue(forall_exists(rel))
            count+=1
        self.assertEqual(count,16)

    def test_source_claim_scope_and_math(self):
        src=(ROOT/"chapters/C09.md").read_text(encoding="utf-8")
        self.assertTrue(src.startswith("# C09"))
        for token in ("\\Sigma_1^P=NP", "\\Pi_1^P=coNP", "PH\\subseteq PSPACE",
                      "## Exercises", "## Map update", "unrestricted",
                      "matrix", "collapse", "Figure obligation"):
            self.assertIn(token,src)
        self.assertGreater(len(src),9000)
        self.assertEqual(sum(line.strip()=="$$" for line in src.splitlines())%2,0)
        for line in src.splitlines():
            if line.strip()!="$$" and "$$" not in line:
                self.assertEqual(line.count("$")%2,0,line)


if __name__=="__main__":
    unittest.main()
