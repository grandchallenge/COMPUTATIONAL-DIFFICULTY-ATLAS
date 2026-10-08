# Visual Production Specification

Status: normative baseline  
Monograph: *A Mathematical Atlas of Computational Difficulty*

## 1. Governing objective

Pedagogical utility is the controlling criterion for every visual decision.

A figure exists to improve the reader's mental model, expose structure, distinguish concepts, or make a proof or computational phenomenon easier to understand. Decorative complexity is not a sufficient reason to include a figure.

Correctness is non-negotiable. Completeness is added only when it does not obscure the concept being taught.

## 2. Production precedence

The default production path is:

1. Wolfram-generated graphics.
2. Evaluate the rendered result for pedagogical clarity.
3. Replace or supplement with an alternate medium only when that medium communicates the intended idea better.

This is a precedence rule, not a prohibition. TikZ/PGF, PGFPlots, SVG, hand-authored vector graphics, or other methods are preferred when they materially improve explanatory power, exact symbolic structure, accessibility, or typographic integration.

## 3. Proper mathematical typesetting

All production figures shall use publication-quality mathematical typesetting.

- Mathematical notation must be exact and consistent with the body text.
- Class names such as $P$, $NP$, $coNP$, $PSPACE$, $BQP$, and $\#P$ must be typeset as mathematics, not approximated as ordinary graphic text.
- Reduction symbols, quantifiers, theorem references, subscripts, superscripts, and operators must use canonical notation.
- AI-generated lettering is not permitted in final publication figures.
- Rasterized text is avoided unless there is no practical alternative.
- Final output should be vector-native where feasible.
- The same notation macros should govern body text and figure labels whenever the toolchain permits.

## 4. Semantic visual grammar

Visual encodings must have stable meanings throughout the monograph.

At minimum:

- proved containment or implication: solid treatment;
- conjectured or unresolved relation: visibly distinct dashed treatment;
- reduction: directed arrow labelled with the reduction notion when ambiguity is possible;
- complexity class: bounded region or other explicit grouping;
- proven impossibility or exclusion: explicit non-color marker;
- unresolved equality or separation: explicit question-mark or uncertainty convention.

Vertical position alone must never mean "harder."

Color must never be the sole carrier of mathematical meaning.

## 5. Wolfram-first use cases

Wolfram should normally be used for:

- computationally generated plots;
- parameter sweeps;
- graph and network layouts;
- class-containment visualizations when geometry is computed;
- quantitative comparisons;
- finite computational witnesses;
- interactive prototypes from which static publication figures are derived;
- figures whose educational value depends on reproducible computation.

The source notebook or Wolfram Language code is part of the figure's scholarly record.

## 6. When alternate presentation is preferred

Alternate presentation should take priority when it increases pedagogical utility.

Typical examples:

- TikZ/PGF for exact symbolic diagrams, theorem dependencies, proof structure, or reduction chains tightly integrated with LaTeX;
- PGFPlots when plot typography or document integration is materially better;
- SVG or equivalent vector authoring when a bespoke conceptual diagram is clearer than an automatically laid-out graphic;
- deliberately simple hand-constructed diagrams when algorithmic layout adds visual noise.

The decision is based on what best teaches the concept, not on tool loyalty.

## 7. Wolfram typography and box geometry

The normative typography, density, padding, and collision rules for Wolfram figures are defined in [WOLFRAM_FIGURE_TYPOGRAPHY.md](WOLFRAM_FIGURE_TYPOGRAPHY.md).

In particular: essential text must remain readable at intended manuscript width without zoom; boxes are sized to text rather than text being shrunk to boxes; and no label, symbol, or annotation may cross, touch, or visually compete with a boundary or structural line.

## 8. Figure-level acceptance test

A production figure should pass all of the following:

1. **First glance:** the principal structure is perceptible within a few seconds.
2. **Exact reading:** labels and notation are correct at normal page size.
3. **Readability:** essential text is comfortably readable at intended manuscript width without zoom.
4. **Containment fit:** no text crosses, touches, or visually competes with box lines, connectors, axes, or panel boundaries.
5. **Claim discipline:** the figure does not imply mathematical relations stronger than the text supports.
6. **Legend sufficiency:** all nonstandard encodings are explained.
7. **Accessibility:** meaning survives grayscale and is not dependent on color alone.
8. **Scale robustness:** the figure remains legible in print and on ordinary screens.
9. **Caption independence:** the caption states what the figure establishes and what it does not establish.
10. **Reproducibility:** source sufficient to regenerate the figure is version-controlled.

A figure should be inspected at its intended manuscript width, not only as a large standalone export.

## 9. Progressive-map doctrine

The monograph will not rely on a single master diagram of computational difficulty.

Instead, figures will progressively distinguish:

- containment;
- reductions;
- computational resources;
- known separations;
- conjectured separations;
- practical solvability;
- decidability versus undecidability.

Early figures may intentionally simplify the landscape, but every simplification must be declared and later repaired as the reader acquires the concepts needed for the more faithful map.

## 10. Prototype versus publication figure

Concept sketches, generated mock-ups, screenshots, and exploratory renderings may be used during development.

They are not publication figures unless they satisfy this specification.

The corrected computational-landscape image that initiated this monograph is therefore treated as a conceptual prototype. Its publication successor must be regenerated under this specification.

## 11. Source discipline

Each figure should have, where applicable:

- a stable figure identifier;
- editable source;
- generation instructions;
- data or computational witness inputs;
- exported vector artifact;
- caption source;
- provenance and version information;
- a short note explaining the pedagogical purpose of the figure.

## 12. Precedence rule

When production preferences conflict, apply:

**pedagogical utility > mathematical and typographic fidelity > reproducibility > stylistic consistency > convenience**

Mathematical correctness is a hard constraint and is not traded against any item in that ordering.
