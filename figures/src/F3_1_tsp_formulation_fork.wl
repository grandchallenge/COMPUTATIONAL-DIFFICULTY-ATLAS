(* C01 F3.1: TSP problem-formulation fork. Reproducible vector figure.
   Four task definitions, not statements about their complexity classes.
   Wolfram production; labels are mathematical typesetting, not AI raster text.
   Reproduction: wolframscript -file figures/src/F3_1_tsp_formulation_fork.wl
*)
Module[{node,ys,labels,fig},
node[t_,sub_]:=Framed[Column[{Style[t,Bold,22,FontFamily->"Times"],Style[sub,20,FontFamily->"Times"]},Alignment->Center,Spacings->0.3],FrameStyle->GrayLevel[.3],RoundingRadius->5,Background->White,FrameMargins->{{12,12},{9,9}}];
ys={2.7,.9,-.9,-2.7};
labels={{"DECISION","Is there a tour costing at most B?"},{"SEARCH","Produce a tour costing at most B"},{"OPTIMIZATION","Produce a minimum-cost tour"},{"COUNTING","How many tours cost at most B?"}};
fig=Graphics[{Directive[Black,Thickness[.003],Arrowheads[.018]],Table[Arrow[{{.22,0},{1.0,ys[[i]]}}],{i,4}],Inset[node["TRAVELING SALESPERSON","Weighted graph; budget B where applicable"],{-2.25,0}],Table[Inset[node[labels[[i,1]],labels[[i,2]]],{3.1,ys[[i]]}],{i,4}]},PlotRange->{{-5,6.2},{-3.8,3.8}},ImageSize->950,Background->White];
Export["figures/generated/F3_1_tsp_formulation_fork.svg",fig,"SVG"];
];
