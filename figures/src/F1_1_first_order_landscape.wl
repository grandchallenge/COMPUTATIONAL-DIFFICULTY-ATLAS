(* F1.1 — First-order landscape of computational difficulty
   Purpose: containment spine, not a scalar hardness hierarchy.
   Typography follows governance/WOLFRAM_FIGURE_TYPOGRAPHY.md.
   Run from repository root. Exports SVG and PDF.
*)

ClearAll["Global`*"];

outDir = FileNameJoin[{"figures", "generated"}];
If[! DirectoryQ[outDir],
  CreateDirectory[outDir, CreateIntermediateDirectories -> True]
];

classLabelSize = 26;
bodySize = 18;
relationSize = 16;
sideBodySize = 16;
sideHeadSize = 19;

figure = Graphics[
 {
  Text[Style["A first-order containment map", 26, Bold], {6.8, 9.35}],
  Text[Style[
    "Containment is not a total ordering of computational difficulty",
    17, Italic], {6.8, 8.92}],

  {FaceForm[GrayLevel[.97]],
   EdgeForm[{GrayLevel[.18], AbsoluteThickness[1.6]}],
   Rectangle[{0.6, 7.35}, {7.65, 8.45}],
   Rectangle[{0.6, 5.65}, {7.65, 6.75}],
   Rectangle[{0.6, 3.95}, {7.65, 5.05}],
   Rectangle[{0.6, 2.25}, {7.65, 3.35}]},

  Text[Style["P", classLabelSize, Bold, Italic], {1.45, 7.90}],
  Text[Style["polynomial time", bodySize], {4.75, 7.90}],

  Text[Style["NP", classLabelSize, Bold, Italic], {1.50, 6.20}],
  Text[Style["polynomial-time verifier", bodySize], {4.85, 6.20}],

  Text[Style["PSPACE", 23, Bold, Italic], {1.90, 4.50}],
  Text[Style["polynomial space", bodySize], {4.85, 4.50}],

  Text[Style["DECIDABLE", 20, Bold], {1.95, 2.80}],
  Text[Style["total algorithm", bodySize], {4.95, 2.80}],

  (* Relation labels occupy whitespace; no connector line passes through text. *)
  Text[Style["⊆  equality open", relationSize], {4.15, 7.05}],
  Text[Style["⊆  equality open", relationSize], {4.15, 5.35}],
  Text[Style["⊊  strict known", relationSize], {4.15, 3.65}],

  {AbsoluteThickness[2.4], Line[{{0.45, 1.55}, {7.80, 1.55}}]},
  Text[Style["COMPUTABILITY BOUNDARY", 16, Bold], {4.1, 1.28}],
  Text[Style["UNDECIDABLE", 21, Bold], {1.80, 0.66}],
  Text[Style["no total algorithm", bodySize], {5.25, 0.66}],

  {FaceForm[GrayLevel[.985]],
   EdgeForm[{GrayLevel[.25], AbsoluteThickness[1.3]}],
   Rectangle[{8.10, 5.40}, {13.25, 8.45}]},
  Text[Style["Anchor examples", sideHeadSize, Bold], {10.68, 8.02}],
  Text[Style["P: reachability; shortest paths", sideBodySize],
    {10.68, 7.44}],
  Text[Style["NP: SAT; Hamiltonian cycle", sideBodySize],
    {10.68, 6.90}],
  Text[Style["PSPACE: TQBF / QBF", sideBodySize], {10.68, 6.36}],
  Text[Style["Undecidable: halting problem", sideBodySize],
    {10.68, 5.82}],

  {FaceForm[GrayLevel[.985]],
   EdgeForm[{Dashing[{.025, .018}], GrayLevel[.25]}],
   Rectangle[{8.10, 2.05}, {13.25, 4.95}]},
  Text[Style["Hardness is relational", sideHeadSize, Bold],
    {10.68, 4.55}],
  Text[Style["NP-hard is reduction-based,", sideBodySize],
    {10.68, 3.93}],
  Text[Style["not a horizontal class band.", sideBodySize],
    {10.68, 3.43}],
  Text[Style["Factorization is not known", sideBodySize],
    {10.68, 2.80}],
  Text[Style["to be NP-complete.", sideBodySize], {10.68, 2.30}]
 },
 PlotRange -> {{0, 13.75}, {0, 9.7}},
 ImageSize -> 720,
 Background -> White,
 ImagePadding -> 15
];

Export[FileNameJoin[{outDir, "F1_1_first_order_landscape.svg"}], figure];
Export[FileNameJoin[{outDir, "F1_1_first_order_landscape.pdf"}], figure];

figure
