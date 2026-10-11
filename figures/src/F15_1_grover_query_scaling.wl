(* C15 / Figure F15.1 — unstructured search query scaling.
   Source-only candidate; requires Wolfram export, visual inspection and editorial acceptance.
   Curves are asymptotic query functions, not measured hardware timings. *)
ClearAll[n];
curves = {n, Sqrt[n]};
figure = LogLogPlot[
  Evaluate[curves], {n, 10^2, 10^8},
  PlotLegends -> Placed[{"Classical: N queries", "Quantum: sqrt(N) queries"}, Below],
  AxesLabel -> {"Search domain size N", "Oracle queries (asymptotic)"},
  PlotRange -> All, Frame -> True, FrameLabel ->
    {"Search domain size N", "Oracle-query scaling"},
  ImageSize -> 900, BaseStyle -> {FontFamily -> "STIX Two Text", FontSize -> 17},
  PlotTheme -> "Scientific",
  Epilog -> {}
];
Export["F15_1_grover_query_scaling.svg", figure, "SVG"];
