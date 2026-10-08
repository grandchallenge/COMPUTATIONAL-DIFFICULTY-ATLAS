# Pedagogical Charter

Status: normative baseline  
Project: *A Mathematical Atlas of Computational Difficulty*

## Mission

The monograph shall optimize for durable conceptual understanding of computational difficulty while preserving theorem-grade correctness.

The reader should leave each chapter able to explain the central distinction using a concrete example, not merely repeat terminology.

## Governing priorities

1. Mathematical correctness is a hard constraint.
2. Pedagogical utility governs architecture, exposition, example choice, and visual design.
3. Formalism follows motivating intuition whenever this does not distort the mathematics.
4. Completeness is progressive: advanced structure is added only after the reader has the conceptual tools to absorb it.
5. Epistemic status is explicit: theorem, known containment, strict separation, conjecture, open equality, heuristic evidence, and engineering practice must not be visually or verbally conflated.

## Chapter contract

Every substantial chapter should implement the sequence:

1. Question.
2. Intuition.
3. Formal definition.
4. Canonical example.
5. Reduction, theorem, or structural result.
6. Boundary of what is known.
7. Common mistake.
8. Exercises or thought experiments.
9. Map update.

The final "map update" states exactly how the reader's current model of computational difficulty has changed.

## Expository test

A section is not complete until an intelligent reader could answer:

> What distinction did this section introduce, and what concrete example shows why the distinction matters?

without reproducing the section's language verbatim.

## Layering rule

Early diagrams and explanations may be intentionally simplified, but every simplification must be:
- declared,
- mathematically safe for its local purpose,
- scheduled for later refinement,
- and never allowed to become a false global statement.

## Recurring distinctions

The monograph shall repeatedly distinguish:

- decision vs search vs optimization vs counting;
- worst-case vs average-case vs parameterized behavior;
- membership vs hardness vs completeness;
- time vs space vs randomness vs interaction vs quantum resources;
- theoretical tractability vs practical solvability;
- decidable vs undecidable.

## Reader profile

Assume discrete mathematics and basic proof literacy. Do not assume prior complexity theory.

Advanced sections may be marked as optional depth, but prerequisite concepts may not be silently assumed.
