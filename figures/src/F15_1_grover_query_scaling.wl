(* F15.1: unstructured search, classical N versus Grover Sqrt[N] oracle-query scaling.
   Asymptotic black-box comparisons only; NOT wall-clock, gate-count, or hardware benchmarks.
   Solid versus dashed lines also work without color. Wolfram typography is vector outlined.
   Reproduction: wolframscript -file figures/src/F15_1_grover_query_scaling.wl
*)
ClearAll[n, fig];
fig = LogLogPlot[{n,Sqrt[n]},{n,10^2,10^8},PlotRange->All,Frame->True,Axes->False,PlotStyle->{Directive[Black,Thick],Directive[GrayLevel[0.42],Thick,Dashed]},PlotLegends->Placed[{Style[Row[{"Classical: ",TraditionalForm[N]," oracle queries"}],17],Style[Row[{"Quantum: ",TraditionalForm[Sqrt[N]]," oracle queries"}],17]},Above],FrameLabel->{Style[Row[{"Search domain size ",TraditionalForm[N]}],19],Style["Oracle queries (asymptotic)",19]},ImageSize->750,BaseStyle->{FontFamily->"Times",FontSize->17},ImagePadding->All];
Export["figures/generated/F15_1_grover_query_scaling.svg", fig, "SVG"];
