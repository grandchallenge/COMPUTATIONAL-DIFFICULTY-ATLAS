"""C14 finite probability, randomized error direction and source-contract tests."""
from fractions import Fraction
from itertools import product
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

def f7(x):
    return (x*(x-1))%7

def binomial(n,r):
    from math import comb
    return comb(n,r)

class C14FiniteChecks(unittest.TestCase):
    def test_root_witness_on_field7(self):
        vals=[f7(x) for x in (0,1,2,3)]
        self.assertEqual(vals,[0,0,2,6])
        self.assertEqual(Fraction(sum(v!=0 for v in vals),4),Fraction(1,2))

    def test_root_bound_repetition(self):
        self.assertEqual(Fraction(1,2)**3,Fraction(1,8))
        # If root fraction <= 1/4, probability 3 misses <= 1/64.
        self.assertLessEqual(Fraction(1,4)**3,Fraction(1,64))

    def test_majority_amplification_for_three_trials(self):
        # Each trial is independently wrong with probability exactly 1/3.
        wrong = sum(Fraction(binomial(3,j)*2**(3-j),3**3) for j in (2,3))
        self.assertEqual(wrong,Fraction(7,27))
        self.assertLess(wrong,Fraction(1,3))

    def test_rp_and_corp_probability_directions(self):
        # Symbolic guarantees for yes/no outcomes.
        rp_yes_yes=Fraction(1,2)
        rp_no_yes=Fraction(0)
        corp_yes_yes=Fraction(1)
        corp_no_no=Fraction(1,2)
        self.assertGreaterEqual(rp_yes_yes,Fraction(1,2))
        self.assertEqual(rp_no_yes,0)
        self.assertEqual(corp_yes_yes,1)
        self.assertGreaterEqual(corp_no_no,Fraction(1,2))

    def test_source_scope_and_math(self):
        s=(ROOT/"chapters/C14.md").read_text(encoding="utf-8")
        for token in ("# C14", "BPP", "coRP", "ZPP", "## Exercises",
                      "## Map update", "Schwartz", "not", "expected",
                      "Figure obligation"):
            self.assertIn(token,s)
        self.assertGreater(len(s),10500)
        self.assertEqual(sum(t.strip()=="$$" for t in s.splitlines())%2,0)
        for line in s.splitlines():
            if line.strip()!="$$" and "$$" not in line:
                self.assertEqual(line.count("$")%2,0,line)
        self.assertFalse(any(ord(c)<32 and c not in "\n\t\r" for c in s))

if __name__=="__main__":
    unittest.main()
