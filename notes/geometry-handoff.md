# Geometry of the archived 15-coloring

This is a data handoff for the geometric analysis in the joint paper. Every
color is labeled by its unique nonzero subspace W of T = span(3,12,48).
For U outside T, its forbidden colors are exactly the labels W contained in
H(U)=U-perp intersect T.

`results/coloring-geometry.json` contains the 15 labels as explicit vector
sets, color-class dimension counts, and profiles by the triple of dimensions
dim(U), dim(H(U)), dim(U intersect T). It also counts the finer profiles
(dim(U), H(U), U intersect T), retaining the actual intersection subspaces:
240 occur outside the clique, and 139 contain more than one chosen color.

Thus the current solver certificate does not already encode a single color
per exact geometric profile. This is a feature of this particular witness,
not a nonexistence theorem for a profile-based construction. A useful next
question is whether recoloring within the allowed lists can make some or all
of those profiles monochromatic while preserving the edges between profiles.

The [profile audit](geometry-profile-audit.md) now gives a written obstruction
to making every exact profile monochromatic: adjacent lines span(1) and span(2)
have identical exact profiles and isometric quotients. Numerical dimension
partitions must not be compared directly to the 240 exact profiles. The audit
report supplies correctly refined groups and their members for further analysis.

Reproduce with `python3 develop/analyze_geometry.py`. The analyzer independently
reconstructs spans and verifies each assigned color against its geometric list.
The full graph check remains `python3 develop/check_full_coloring.py
results/full-15-coloring.json`.
