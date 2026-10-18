"""Finite SAT self-reduction falsification replay for C08.

This uses brute force as a test oracle; it does NOT assert SAT is in P.
"""
from itertools import product
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]


def eval_clause(clause, assignment):
    return any((assignment[abs(lit)-1] if lit > 0
                else not assignment[abs(lit)-1]) for lit in clause)


def sat_with_fixed(clauses, n, fixed):
    for bits in product((False,True),repeat=n):
        if any(bits[i] != val for i,val in fixed.items()):
            continue
        if all(eval_clause(clause,bits) for clause in clauses):
            return True
    return False


def self_reduce(clauses, n):
    if not sat_with_fixed(clauses,n,{}):
        return None
    fixed={}
    for i in range(n):
        candidate={**fixed,i:False}
        fixed=candidate if sat_with_fixed(clauses,n,candidate) else {**fixed,i:True}
    return tuple(fixed[i] for i in range(n))


class C08Falsification(unittest.TestCase):
    def test_section_anchors_are_css_safe(self):
        import re
        from pathlib import Path
        path=Path(__file__).resolve().parents[1]/"chapters"/"C08.md"
        headings=re.findall(r"^## (.+)$",path.read_text(encoding="utf-8"),re.M)
        assert sum(h.startswith("Section ") for h in headings)>7
        assert not any(re.match(r"^[0-9]",h) for h in headings)

    def test_search_decision_reduction_on_all_small_cnf(self):
        lits=(-2,-1,1,2)
        pool=[clause for size in (1,2) for clause in product(lits,repeat=size)]
        ntests=0
        for formula in product(pool,repeat=3):
            witness=self_reduce(formula,2)
            oracle=sat_with_fixed(formula,2,{})
            self.assertEqual(witness is not None, oracle,formula)
            if witness is not None:
                self.assertTrue(all(eval_clause(c,witness) for c in formula))
            ntests+=1
        self.assertEqual(ntests,8000)

    def test_empty_formula_and_false_clause(self):
        self.assertEqual(self_reduce((),2),(False,False))
        self.assertIsNone(self_reduce(((),),2))

    def test_epistemic_and_math_source_invariants(self):
        chapter=(ROOT/"chapters/C08.md").read_text(encoding="utf-8")
        assert chapter.startswith("# C08")
        for statement in ("P\\subseteq NP", "P\\subsetneq EXPTIME",
                          "## Exercises", "## Map update",
                          "relativ", "Natural proofs", "Algebrization",
                          "self-reducibility", "open"):
            self.assertIn(statement,chapter)
        self.assertGreater(len(chapter),9000)
        self.assertEqual(sum(line.strip()=="$$" for line in chapter.splitlines())%2,0)
        for line in chapter.splitlines():
            if line.strip()!="$$" and "$$" not in line:
                self.assertEqual(line.count("$")%2,0,line)


if __name__=="__main__":
    unittest.main()
