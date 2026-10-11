(* F2.1 — Polynomial-time many-one reduction translator and target solver.
Source-authoritative Wolfram vector diagram, not an NP-completeness proof.
Reproduce from repository root:
wolframscript -file figures/src/F2_1_translator_solver.wl *)
figure = Module[{box,fig},box[a_,b_]:=Framed[Column[{Style[a,22,Bold,FontFamily->"Times"],Style[b,18,FontFamily->"Times"]},Alignment->Center,Spacings->0.35],FrameStyle->GrayLevel[.25],Background->White,FrameMargins->{{13,13},{9,9}}];fig=Graphics[{Directive[Black,Thickness[.003],Arrowheads[.023]],Arrow[{{-4.7,0},{-3.1,0}}],Arrow[{{-1.5,0},{.2,0}}],Arrow[{{2.0,0},{3.6,0}}],Inset[box["Problem A","Encoded input x"],{-5.7,0}],Inset[box["Translator f","Polynomial time"],{-2.28,0}],Inset[box["Problem B","Instance f(x)"],{1.11,0}],Inset[box["B solver","Yes or no"],{4.65,0}],Inset[Style["A reduces to B; a B-solver can decide A",22,FontFamily->"Times"],{0,-1.25}]},PlotRange->{{-7,6.9},{-1.95,1.4}},ImageSize->1000,Background->White];fig];
Export["figures/generated/F2_1_translator_solver.svg",figure,"SVG"];
