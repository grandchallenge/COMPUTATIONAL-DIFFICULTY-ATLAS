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

def evaluate_circuit(inputs, gates, output):
    """Finite CVP language witness: validate indices/arity/topological order."""
    if not isinstance(inputs, (tuple,list)) or not all(type(x) is bool for x in inputs):
        return False
    values=list(inputs)
    for instruction in gates:
        if not isinstance(instruction,tuple) or len(instruction)!=2:
            return False
        op, refs=instruction
        if op not in ("AND","OR","NOT") or not isinstance(refs,tuple):
            return False
        if len(refs)!=(1 if op=="NOT" else 2):
            return False
        if not all(type(i) is int and 0<=i<len(values) for i in refs):
            return False
        vals=[values[i] for i in refs]
        values.append(not vals[0] if op=="NOT" else
                      all(vals) if op=="AND" else any(vals))
    if type(output) is not int or not 0<=output<len(values):
        return False
    return values[output]


def parity_dag(n, balanced):
    """Construct distinct sequential/balanced XOR circuits over AND/OR/NOT."""
    gates=[]
    def xor(a,b):
        total=n+len(gates)
        gates.extend((("OR",(a,b)), ("AND",(a,b)),
                      ("NOT",(total+1,)),("AND",(total,total+2))))
        return total+3
    live=list(range(n))
    if balanced:
        while len(live)>1:
            assert len(live)%2==0
            live=[xor(live[i],live[i+1]) for i in range(0,len(live),2)]
        return gates,live[0]
    z=live[0]
    for a in live[1:]:
        z=xor(z,a)
    return gates,z


def circuit_depth(num_inputs,gates):
    depth=[0]*num_inputs
    for _,refs in gates:
        depth.append(1+max(depth[i] for i in refs))
    return depth[-1]


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

    def test_cvp_finite_language_and_equivalent_parity_circuits(self):
        seq,seq_out=parity_dag(8,False)
        bal,bal_out=parity_dag(8,True)
        self.assertEqual(len(seq),28)
        self.assertEqual(len(bal),28)
        self.assertGreater(circuit_depth(8,seq),circuit_depth(8,bal))
        for bits in product((False,True),repeat=8):
            self.assertEqual(evaluate_circuit(bits,seq,seq_out),
                             sequential_parity(bits))
            self.assertEqual(evaluate_circuit(bits,bal,bal_out),
                             sequential_parity(bits))
        for bad in (
            ((True,),[("AND",(0,99))],1),
            ((True,),[("NOT",(4,))],1),
            ((True,),[("AND",(0,))],1),
            ((True,),[("XOR",(0,0))],1),
            ((True,),[("OR",(1,0))],1),
            ((True,),[("NOT",(0,))],100),
            ((True,),[],True),
            ((1,),[],0),
        ):
            self.assertFalse(evaluate_circuit(*bad))

    def test_source_bibliography_and_safe_anchors(self):
        import re
        s=(ROOT/"chapters/C16.md").read_text(encoding="utf-8")
        for token in ("10.1145/321812.321815","10.1145/990518.990519",
                      "malformed binary codes", "implicit promise",
                      "logspace reductions", "does not supply a proof",
                      "source", "unproduced"):
            self.assertIn(token,s)
        headings=re.findall(r"^## (.+)$",s,re.M)
        self.assertEqual(sum(h.startswith("Section ") for h in headings),9)
        self.assertFalse(any(re.match(r"^[0-9]",h) for h in headings))

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
