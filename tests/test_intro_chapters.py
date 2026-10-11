"""Finite educational witnesses and source contract for C02/C03 candidate chapters.

Checks do not establish complexity lower bounds, only exact local examples.
"""
from pathlib import Path
import re
import unittest
from collections import deque

ROOT = Path(__file__).resolve().parents[1]


def reach(vertices, edges, start, target):
    adj = {x: [] for x in vertices}
    for u, v in edges:
        adj[u].append(v)
    for values in adj.values():
        values.sort()
    discovered = {start}
    order = [start]
    q = deque([start])
    while q:
        u = q.popleft()
        if u == target:
            return True, order
        for v in adj[u]:
            if v not in discovered:
                discovered.add(v)
                order.append(v)
                q.append(v)
    return False, order


class IntroExamples(unittest.TestCase):
    def test_binary_input_length(self):
        for k in [0, 1, 3, 12, 30]:
            self.assertEqual((1 << k).bit_length(), k + 1)

    def test_big_o_quadratic_witness(self):
        for n in range(1, 500):
            value = 3 * n * n + 5 * n + 7
            self.assertGreaterEqual(value, 3 * n * n)
            self.assertLessEqual(value, 15 * n * n)

    def test_growth_table(self):
        expected = [(5, 25, 32), (10, 100, 1024),
                    (20, 400, 1048576), (30, 900, 1073741824)]
        self.assertEqual([(n, n*n, 2**n) for n, _, _ in expected], expected)

    def test_directional_graph_witness(self):
        v = list("abcde")
        e = [("a", "b"), ("b", "c"), ("c", "d"), ("a", "e")]
        self.assertEqual(reach(v, e, "a", "d"), (True, list("abecd")))
        self.assertEqual(reach(v, e, "e", "a"), (False, ["e"]))
        self.assertEqual(reach(v, e, "d", "d"), (True, ["d"]))

    def test_chapter_contract_and_math_delimiters(self):
        for id in ("C02", "C03"):
            text = (ROOT / "chapters" / f"{id}.md").read_text(encoding="utf-8")
            self.assertTrue(text.startswith(f"# {id} —"))
            for phrase in ("**Status:**", "## Exercises", "## Map update",
                           "**Exit test:**", "**Figure requirement"):
                self.assertIn(phrase, text, (id, phrase))
            self.assertGreater(len(text), 7500)
            self.assertEqual(sum(line.strip() == "$$" for line in text.splitlines()) % 2, 0)
            for n, line in enumerate(text.splitlines(), 1):
                if "$$" not in line:
                    self.assertEqual(line.count("$") % 2, 0, (id, n, line))
            # Bare HTML in drafts would need separate sanitization.
            self.assertNotRegex(text, r"<(?:script|iframe|style)\b")
            self.assertFalse(any(ord(ch) < 32 and ch not in "\n\t\r" for ch in text))

    def test_promises_not_overstated(self):
        c02 = (ROOT / "chapters/C02.md").read_text()
        c03 = (ROOT / "chapters/C03.md").read_text()
        self.assertIn("not a lower-bound proof", c02)
        self.assertIn("does not imply that SAT is outside P", c03)
        self.assertIn("decidability", c02.lower() + c03.lower())


if __name__ == "__main__":
    unittest.main()
