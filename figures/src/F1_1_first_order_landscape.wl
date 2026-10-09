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
sideBodySize = 15;
sideHeadSize = 19;

figure = Graphics[
 {
  Text[Style["A first-order containment map", 26, Bold], {7.0, 9.35}],
  Text[Style[
    "Containment is not a total ordering of computational difficulty",
    17, Italic], {7.0, 8.92}],

  {FaceForm[GrayLevel[.97]],
   EdgeForm[{GrayLevel[.18], AbsoluteThickness[1.6]}],
   Rectangle[{0.5, 7.35}, {7.9, 8.45}],
   Rectangle[{0.5, 5.65}, {7.9, 6.75}],
   Rectangle[{0.5, 3.95}, {7.9, 5.05}],
   Rectangle[{0.5, 2.25}, {7.9, 3.35}]},

  Text[Style["P", classLabelSize, Bold, Italic], {1.35, 7.90}],
  Text[Style["polynomial time", bodySize], {5.05, 7.90}],

  Text[Style["NP", classLabelSize, Bold, Italic], {1.40, 6.20}],
  Text[Style[
    Column[{"polynomial-size witness", "polynomial-time verifier"},
      Center, Spacings -> .05], 15], {5.15, 6.20}],

  Text[Style["PSPACE", 23, Bold, Italic], {1.90, 4.50}],
  Text[Style["polynomial space", bodySize], {5.05, 4.50}],

  Text[Style["DECIDABLE", 20, Bold], {1.85, 2.80}],
  Text[Style["total decider exists", 17], {5.30, 2.80}],

  (* Relation labels occupy whitespace; no connector line passes through text. *)
  Text[Style["⊆  equality open", relationSize], {4.20, 7.05}],
  Text[Style["⊆  equality open", relationSize], {4.20, 5.35}],
  Text[Style["⊊  strict known", relationSize], {4.20, 3.65}],

  {AbsoluteThickness[2.4], Line[{{0.4, 1.55}, {8.0, 1.55}}]},
  Text[Style["COMPUTABILITY BOUNDARY", 16, Bold], {4.2, 1.28}],
  Text[Style["UNDECIDABLE", 21, Bold], {1.85, 0.66}],
  Text[Style["no total decider", 17], {5.55, 0.66}],

  {FaceForm[GrayLevel[.985]],
   EdgeForm[{GrayLevel[.25], AbsoluteThickness[1.3]}],
   Rectangle[{8.45, 5.15}, {13.75, 8.45}]},
  Text[Style["Anchor examples", sideHeadSize, Bold], {11.10, 8.03}],
  Text[Style["P: reachability", sideBodySize], {11.10, 7.48}],
  Text[Style["shortest-path decision", sideBodySize], {11.10, 7.08}],
  Text[Style["NP: SAT; Hamiltonian cycle", sideBodySize],
    {11.10, 6.53}],
  Text[Style["PSPACE: TQBF / QBF", sideBodySize], {11.10, 5.98}],
  Text[Style["Undecidable: halting problem", sideBodySize],
    {11.10, 5.43}],

  {FaceForm[GrayLevel[.985]],
   EdgeForm[{Dashing[{.025, .018}], GrayLevel[.25]}],
   Rectangle[{8.45, 2.05}, {13.75, 4.75}]},
  Text[Style["Hardness is relational", sideHeadSize, Bold],
    {11.10, 4.40}],
  Text[Style["NP-hard is reduction-based,", sideBodySize],
    {11.10, 3.84}],
  Text[Style["not a horizontal class band.", sideBodySize],
    {11.10, 3.38}],
  Text[Style["Factorization is not known", sideBodySize],
    {11.10, 2.78}],
  Text[Style["to be NP-complete.", sideBodySize], {11.10, 2.32}]
 },
 PlotRange -> {{0, 14.1}, {0, 9.7}},
 ImageSize -> 800,
 Background -> White,
 ImagePadding -> 18
];

Export[FileNameJoin[{outDir, "F1_1_first_order_landscape.svg"}], figure];
Export[FileNameJoin[{outDir, "F1_1_first_order_landscape.pdf"}], figure];

figure
