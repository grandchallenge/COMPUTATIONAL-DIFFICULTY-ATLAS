"""Finite truth-table checks of C07's SAT, UNSAT and TAUT examples."""
from itertools import product
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]


def psi(a,b):
    return (a or not a) and (b or not b)


def theta(a,b):
    return (a or b) and ((not a) or b)


def chi(a,b):
    return a and not a


def assignments():
    return list(product((False,True),repeat=2))


class C07FiniteReplay(unittest.TestCase):
    def test_section_anchors_are_css_safe(self):
        import re
        from pathlib import Path
        path=Path(__file__).resolve().parents[1]/"chapters"/"C07.md"
        headings=re.findall(r"^## (.+)$",path.read_text(encoding="utf-8"),re.M)
        assert sum(h.startswith("Section ") for h in headings)>7
        assert not any(re.match(r"^[0-9]",h) for h in headings)

    def test_tautology_and_not_tautology(self):
        self.assertTrue(all(psi(a,b) for a,b in assignments()))
        self.assertTrue(any(theta(a,b) for a,b in assignments()))
        self.assertTrue(any(not theta(a,b) for a,b in assignments()))
        self.assertFalse(theta(False,False))

    def test_unsat_and_negation_tautology(self):
        self.assertFalse(any(chi(a,b) for a,b in assignments()))
        self.assertTrue(all(not chi(a,b) for a,b in assignments()))

    def test_identity_unsat_iff_negation_tautology_for_all_two_bit_predicates(self):
        vectors=list(product((False,True),repeat=4))
        for truth_table in vectors:
            self.assertEqual(not any(truth_table),all(not value for value in truth_table))
            self.assertEqual(not all(truth_table),any(not value for value in truth_table))
        self.assertEqual(len(vectors),16)

    def test_invalid_formula_convention_needs_explicit_branch(self):
        # The total SAT language rejects invalid encodings; its *exact*
        # complement treats invalid strings as yes-instances.
        cases=[
            {"valid":False,"satisfiable":False},
            {"valid":True,"satisfiable":False},
            {"valid":True,"satisfiable":True},
        ]
        for x in cases:
            in_sat = x["valid"] and x["satisfiable"]
            exact_sat_complement = not in_sat
            valid_unsat = x["valid"] and not x["satisfiable"]
            if not x["valid"]:
                self.assertTrue(exact_sat_complement)
                self.assertFalse(valid_unsat)
            else:
                self.assertEqual(exact_sat_complement,valid_unsat)

    def test_source_scope_and_math(self):
        s=(ROOT/"chapters/C07.md").read_text(encoding="utf-8")
        self.assertTrue(s.startswith("# C07"))
        for needle in ("coNP", "## Exercises", "## Map update", "Cook–Levin",
                       "UNSAT", "TAUT", "malformed", "Figure obligation"):
            self.assertIn(needle,s)
        self.assertGreater(len(s),9000)
        self.assertEqual(sum(line.strip()=="$$" for line in s.splitlines())%2,0)
        for line in s.splitlines():
            if line.strip()!="$$" and "$$" not in line:
                self.assertEqual(line.count("$")%2,0,line)


if __name__=="__main__":
    unittest.main()
