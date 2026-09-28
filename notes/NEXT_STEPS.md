# Next research steps

1. Review and explain the full-graph 15-coloring with Reza. Group the choices
   by dim(U), U intersect T and H(U)=U-perp intersect T, and seek a small
   structural coloring rule rather than relying indefinitely on a large table.
2. Settle whether Gamma_6 is 12- or 13-chromatic. The weighted bound rules out
   at most eleven colors, and the checked certificate uses thirteen. The
   12-color solver timeouts do not strengthen the lower bound. The six-class
   normalization in line-coloring.md removes a substantial geometric symmetry.
3. Agree a Lean formalization target for the finite 15-color result: verify a
   complete subspace enumeration and graph coloring certificate with an exact
   reflection/checker theorem, preserving the original graph definition. The
   user must select the validation machine in the current session before work.
4. Integrate these results with Reza's proposed introduction and clique section
   in the joint manuscript. Keep the September 28 two-author note historical.
5. Investigate larger dimensions and other parameters where there is a
   substantive theorem. The arbitrary-dimension chromatic problem stays open.

The fixed 15-clique is Nikandish's construction. Its ability to extend to all
vertices is now certified in dimension six. The known radical/quotient proof
settles the clique number for all dimensions; these are separate contributions.
