"""Finite C13 counting, permanent, PP threshold and source-format replay."""
from itertools import permutations, product
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
B=(False, True)

def count_sat(clauses,n):
    return sum(all(any((bits[abs(z)-1] if z>0 else not bits[-z-1])
                       for z in clause) for clause in clauses)
               for bits in product(B,repeat=n))

def permanent(matrix):
    size=len(matrix)
    return sum(all(matrix[i][p[i]] for i in range(size))
               for p in permutations(range(size)))

def determinant3(matrix):
    value=0
    for p in permutations(range(3)):
        inversions=sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
        value+=(-1)**inversions*int(all(matrix[i][p[i]] for i in range(3)))
    return value

class C13FiniteChecks(unittest.TestCase):
    def test_named_sat_count_and_unused_variable(self):
        self.assertEqual(count_sat([(1,2)],2),3)
        self.assertEqual(count_sat([(1,2)],3),6)
        self.assertEqual(count_sat([(1,),(-1,)],2),0)

    def test_parsimonious_counterexample(self):
        for clauses in ([(1,)],[(1,2)],[(1,),(-1,)]):
            self.assertEqual(count_sat(clauses,3),2*count_sat(clauses,2))

    def test_gate_extension_is_unique_not_just_equisatisfiable(self):
        # The counting-preserving gate Tseitin clauses encode g <-> (x and y).
        # For each fixed (x,y), exactly one auxiliary g value satisfies them.
        for x,y in product(B,repeat=2):
            valid = [
                g for g in B
                if ((not g or x) and (not g or y)
                    and (g or not x or not y))
            ]
            self.assertEqual(valid,[x and y])

        # Omitting equivalence directions can introduce unwanted solutions.
        x,y=False,False
        one_way=[g for g in B if (not g or x) and (not g or y)]
        self.assertEqual(one_way,[False])
        no_gate_constraint=[g for g in B]
        self.assertEqual(len(no_gate_constraint),2)

    def test_permanent_example(self):
        A=((1,1,0),(1,1,1),(0,1,1))
        self.assertEqual(permanent(A),3)
        self.assertEqual(determinant3(A),-1)

    def test_np_to_pp_acceptance_baseline(self):
        for p in range(0,7):
            paths=1<<p
            for accepting in range(paths+1):
                total=2*paths
                accepted=paths+accepting
                self.assertEqual(2*accepted>total, accepting>0)

    def test_source_epistemics_and_markup(self):
        s=(ROOT/"chapters/C13.md").read_text(encoding="utf-8")
        self.assertTrue(s.startswith("# C13"))
        for required in (r"\#SAT", r"\operatorname{perm}", "parsimonious",
                         "Valiant", "## Exercises", "## Map update",
                         "not a subclass of NP", "No figure has yet been produced",
                         "strictly greater than", "unique", "Lemma 3.2",
                         "Turing (oracle) counting reductions", "non-square matrices",
                         "not accepted"):
            self.assertIn(required,s)
        self.assertGreater(len(s),10000)
        self.assertEqual(sum(t.strip()=="$$" for t in s.splitlines())%2,0)
        for line in s.splitlines():
            if line.strip()!="$$" and "$$" not in line:
                self.assertEqual(line.count("$")%2,0,line)
        self.assertFalse(any(ord(ch)<32 and ch not in "\n\t\r" for ch in s))

if __name__=="__main__":
    unittest.main()
