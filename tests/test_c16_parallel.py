"""C16 parallel parity construction and proof/typography source contract."""
from itertools import product
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

def sequential_parity(bits):
    value=False
    for b in bits:
        value=bool(value)^bool(b)
    return value

def parallel_parity(bits):
    layers=[]
    vals=[bool(b) for b in bits]
    while len(vals)>1:
        assert len(vals)%2==0
        nxt=[vals[2*i]^vals[2*i+1] for i in range(len(vals)//2)]
        layers.append(len(nxt))
        vals=nxt
    return vals[0],layers

class C16FiniteChecks(unittest.TestCase):
    def test_exhaustive_eight_bit_parity(self):
        for bits in product((False,True),repeat=8):
            p,layers=parallel_parity(bits)
            self.assertEqual(p,sequential_parity(bits))
            self.assertEqual(layers,[4,2,1])
            self.assertEqual(sum(layers),7)

    def test_power_of_two_work_depth(self):
        for k in range(1,10):
            n=2**k
            p,layers=parallel_parity([bool(i%3==0) for i in range(n)])
            self.assertEqual(len(layers),k)
            self.assertEqual(sum(layers),n-1)
            self.assertEqual(p,sequential_parity([bool(i%3==0) for i in range(n)]))

    def test_work_span_lower_bounds(self):
        for w,d,p in ((7,3,1),(7,3,2),(7,3,4),(15,4,8)):
            self.assertGreaterEqual(max(w/p,d),d)
            self.assertGreaterEqual(max(w/p,d),w/p)

    def test_math_source_contract(self):
        s=(ROOT/"chapters/C16.md").read_text(encoding="utf-8")
        self.assertTrue(s.startswith("# C16"))
        for word in ("DLOGTIME", "logspace", "Circuit Value",
                     "## Exercises", "## Map update", "unproduced",
                     "P-complete", "uniform"):
            self.assertIn(word,s)
        self.assertGreater(len(s),9500)
        self.assertEqual(sum(line.strip()=="$$" for line in s.splitlines())%2,0)
        for line in s.splitlines():
            if line.strip()!="$$" and "$$" not in line:
                self.assertEqual(line.count("$")%2,0,line)

if __name__=="__main__":
    unittest.main()
