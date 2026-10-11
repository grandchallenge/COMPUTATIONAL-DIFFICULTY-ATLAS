(* F15.1: Quantum versus classical unstructured-search oracle-query scaling.
   The curves N and Sqrt[N] are asymptotic, not measured device runtimes.
   Wolfram Language is the publication authority for this plot.
   Reproduce by evaluating this file in a Wolfram kernel. *)
ClearAll[n, fig];
fig = LogLogPlot[
  {n, Sqrt[n]}, {n, 10^2, 10^8},
  PlotRange -> All,
  Frame -> True, Axes -> False,
  PlotStyle -> {Directive[Black, Thick], Directive[GrayLevel[0.42], Thick, Dashed]},
  PlotLegends -> Placed[{"Classical: N oracle queries", "Quantum: sqrt(N) oracle queries"}, Above],
  FrameLabel -> {Style["Search domain size N", 17], Style["Oracle queries (asymptotic)", 17]},
  ImageSize -> 750,
  BaseStyle -> {FontFamily -> "Times", FontSize -> 15},
  ImagePadding -> All
];
Export["F15_1_grover_query_scaling.svg", fig, "SVG"];
