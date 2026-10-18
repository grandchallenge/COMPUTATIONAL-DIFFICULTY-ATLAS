"""C11 bounded quantified-game falsification tests; not PSPACE-hardness proofs."""
from itertools import product
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
BITS=(False,True)


def qbf_eval(prefix, pred, assignment=()):
    if not prefix:
        return bool(pred(*assignment))
    left=qbf_eval(prefix[1:],pred,assignment+(False,))
    right=qbf_eval(prefix[1:],pred,assignment+(True,))
    return (left or right) if prefix[0]=="E" else (left and right)


def branch_table_truth(prefix, table):
    # Independent bottom-up truth-table collapse from the final quantifier.
    values=list(table)
    for quantifier in reversed(prefix):
        values=[((a or b) if quantifier=="E" else (a and b))
                for a,b in zip(values[::2],values[1::2])]
    return bool(values[0])


class C11TruthTests(unittest.TestCase):
    def test_all_boolean_predicates_and_prefixes_through_three_vars(self):
        count=0
        for n in range(4):
            for prefix in product("EA",repeat=n):
                for values in product(BITS,repeat=2**n):
                    pred=lambda *xs,values=values: values[sum(int(b) << (
                        n-1-i) for i,b in enumerate(xs))]
                    self.assertEqual(qbf_eval(prefix,pred),
                                     branch_table_truth(prefix,values),
                                     (prefix,values))
                    count+=1
        self.assertEqual(count,2+8+64+2048)

    def test_quantifier_order_matters(self):
        eq=lambda a,b: a==b
        self.assertTrue(qbf_eval("AE",eq))
        self.assertFalse(qbf_eval("EA",eq))
        self.assertTrue(qbf_eval("EAE",lambda u,x,z: (not u) and z==x))

    def test_binary_prefix_binding_contract(self):
        # A small finite grammar fixture: paired declarations, unique
        # binders, no free matrix variables, and no malformed token stream.
        def wellformed(prefix, matrix):
            if any(q not in ("E","A") or not isinstance(v,int) or v<0
                   for q,v in prefix):
                return False
            declarations=[v for _,v in prefix]
            if len(declarations)!=len(set(declarations)):
                return False
            if any(not isinstance(v,int) or v<0 for v in matrix):
                return False
            return set(matrix)<=set(declarations)
        self.assertTrue(wellformed([("A",0),("E",1)],[0,1]))
        self.assertTrue(wellformed([("A",0),("E",1)],[1])) # unused binder
        self.assertFalse(wellformed([("A",0),("E",0)],[0]))
        self.assertFalse(wellformed([("A",0)],[1]))
        self.assertFalse(wellformed([("X",0)],[0]))
        self.assertFalse(wellformed([("E",0)],[0,"bad"]))

    def test_source_review_bridge_and_safe_headings(self):
        import re
        s=(ROOT/"chapters/C11.md").read_text(encoding="utf-8")
        for token in ("Binary input contract","exactly one", "NO instances",
                      "polynomial-size verification circuit",
                      "successive players", "No exponentially",
                      "Theorem 4.13", "10.1017/CBO9780511804090.007",
                      "Sipser", "not a full proof", "No such figure has been produced"):
            self.assertIn(token,s)
        headers=re.findall(r"^## (.+)$",s,re.M)
        self.assertEqual(sum(x.startswith("Section ") for x in headers),9)
        self.assertFalse(any(re.match(r"^[0-9]",x) for x in headers))

    def test_source_and_markup(self):
        chapter=(ROOT/"chapters/C11.md").read_text(encoding="utf-8")
        self.assertTrue(chapter.startswith("# C11"))
        for term in ("PSPACE", "TQBF", "AP=PSPACE", "## Exercises",
                     "## Map update", "unbounded", "Chandra",
                     "Figure obligation", "not a time bound"):
            self.assertIn(term,chapter)
        self.assertIn("```text\nEVAL(prefix, matrix, partial_assignment):",chapter)
        self.assertNotIn("\\```",chapter)
        self.assertEqual(sum(s.startswith("```") for s in chapter.splitlines()),2)
        self.assertEqual(sum(s.strip()=="$$" for s in chapter.splitlines())%2,0)
        for line in chapter.splitlines():
            if "$$" not in line:
                self.assertEqual(line.count("$")%2,0,line)
        self.assertGreater(len(chapter),11000)


if __name__=="__main__":
    unittest.main()
