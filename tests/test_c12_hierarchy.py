"""C12 finite witnesses: binary-length, modular-counter costs and hierarchy claims.

These checks do not pretend to prove deterministic hierarchy theorems.
"""
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]

def modular_counter(k):
    assert k>=0
    mask=(1<<k)-1
    state=0
    for _ in range(1<<k):
        state=(state+1)&mask
    return state

class C12Examples(unittest.TestCase):
    def test_binary_length(self):
        for k in range(0,15):
            self.assertEqual((1<<k).bit_length(),k+1)

    def test_modular_counter_returns_zero_after_full_cycle(self):
        for k in range(0,13):
            self.assertEqual(modular_counter(k),0)

    def test_number_of_steps_is_exponential_in_bit_length(self):
        for k in range(1,17):
            magnitude=1<<k
            length=magnitude.bit_length()
            self.assertEqual(magnitude, 1 << (length-1))
            self.assertLessEqual(k, length)

    def test_chapter_math_and_epistemic_contract(self):
        s=(ROOT/"chapters/C12.md").read_text(encoding="utf-8")
        self.assertTrue(s.startswith("# C12"))
        for token in (r"\mathrm{EXPTIME}",r"\mathrm{EXPSPACE}",
                      r"\mathrm{2EXPTIME}",r"PSPACE\subsetneq EXPSPACE",
                      r"EXPTIME\subsetneq 2EXPTIME",r"APSPACE=EXPTIME",
                      "## Exercises","## Map update","not yet produced",
                      "strict","configurations"):
            self.assertIn(token,s)
        self.assertGreater(len(s),10000)
        self.assertEqual(sum(line.strip()=="$$" for line in s.splitlines())%2,0)
        for line in s.splitlines():
            if line.strip() != "$$" and "$$" not in line:
                self.assertEqual(line.count("$")%2,0,line)
        self.assertFalse(any(ord(c)<32 and c not in "\n\r\t" for c in s))

if __name__=="__main__":
    unittest.main()
