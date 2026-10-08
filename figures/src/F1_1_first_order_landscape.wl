(* F1.1 — First-order landscape of computational difficulty
   Purpose: containment spine, not a scalar hardness hierarchy.
   Run from repository root. Exports SVG and PDF.
*)

ClearAll["Global`*"];

outDir = FileNameJoin[{"figures", "generated"}];
If[! DirectoryQ[outDir],
  CreateDirectory[outDir, CreateIntermediateDirectories -> True]
];

figure = Graphics[
 {
  {FaceForm[GrayLevel[.97]],
   EdgeForm[{GrayLevel[.2], AbsoluteThickness[1.6]}],
   Rectangle[{1.2, 7.25}, {7.8, 8.35}],
   Rectangle[{1.2, 5.55}, {7.8, 6.65}],
   Rectangle[{1.2, 3.85}, {7.8, 4.95}],
   Rectangle[{1.2, 2.15}, {7.8, 3.25}]},

  Text[Style["P", 24, Bold, Italic], {2.0, 7.8}],
  Text[Style["deterministic polynomial time", 13], {4.9, 7.8}],

  Text[Style["NP", 24, Bold, Italic], {2.0, 6.1}],
  Text[Style["polynomially verifiable certificates", 13], {4.9, 6.1}],

  Text[Style["PSPACE", 22, Bold, Italic], {2.25, 4.4}],
  Text[Style["polynomial space", 13], {4.9, 4.4}],

  Text[Style["DECIDABLE", 18, Bold], {2.45, 2.7}],
  Text[Style["some algorithm halts on every input", 13], {5.05, 2.7}],

  {AbsoluteThickness[1.5], Arrowheads[.028],
   Arrow[{{4.5, 7.22}, {4.5, 6.72}}],
   Arrow[{{4.5, 5.52}, {4.5, 5.02}}],
   Arrow[{{4.5, 3.82}, {4.5, 3.32}}]},

  Text[Style["⊆   equality open", 11], {5.85, 6.96}],
  Text[Style["⊆   equality open", 11], {5.85, 5.26}],
  Text[Style["⊊   strict containment known", 11], {5.95, 3.56}],

  {AbsoluteThickness[2.2], Line[{{.7, 1.45}, {8.3, 1.45}}]},
  Text[Style["COMPUTABILITY BOUNDARY", 12, Bold], {4.5, 1.17}],
  Text[Style["UNDECIDABLE", 18, Bold], {2.4, .55}],
  Text[Style["no algorithm solves every instance", 13], {5.1, .55}],

  Text[Style["Examples", 12, Bold], {10.15, 8.55}],
  Text[Style["P: directed reachability; shortest-path decision", 11],
    {10.15, 7.85}],
  Text[Style["NP: SAT; Hamiltonian cycle; TSP decision", 11],
    {10.15, 6.95}],
  Text[Style["PSPACE: TQBF / QBF", 11], {10.15, 6.05}],
  Text[Style["Undecidable: HALT_TM", 11], {10.15, 5.15}],

  {FaceForm[GrayLevel[.985]],
   EdgeForm[{Dashing[{.025, .018}], GrayLevel[.25]}],
   Rectangle[{8.45, 1.85}, {12.8, 4.35}]},
  Text[Style["Hardness is not a height", 13, Bold], {10.62, 4.05}],
  Text[Style["NP-hard is reduction-based,", 11], {10.62, 3.55}],
  Text[Style["not a complexity-class band.", 11], {10.62, 3.17}],
  Text[Style["NP-hard problems may lie", 11], {10.62, 2.68}],
  Text[Style["inside or outside NP.", 11], {10.62, 2.30}],

  Text[Style["Factorization is deliberately not placed on this spine:", 10, Bold],
    {10.62, 1.25}],
  Text[Style["it is not known NP-complete; formulation and model matter.", 10],
    {10.62, .88}],

  Text[Style[
    "First-order map: containment, not a total ordering of difficulty",
    12, Italic], {6.7, -.15}]
 },
 PlotRange -> {{0, 13.2}, {-0.5, 9}},
 ImageSize -> 1000,
 Background -> White
];

Export[FileNameJoin[{outDir, "F1_1_first_order_landscape.svg"}], figure];
Export[FileNameJoin[{outDir, "F1_1_first_order_landscape.pdf"}], figure];

figure
