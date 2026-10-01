# Complete basis values encode the vertex

For the fixed complement S=span(1,4,16), write K=U intersect T,
P=pi_S(U) and f:P -> T/K. Reza's requested script is actually
`develop/lift_map_value.py` (singular), from commit
`d150bb51e3f689f3be2972ca3fb5c22009c4bdd2`. The diagnostic output is
`results/lift-map-values.json` (plural). The script's zero-vector skip is
removed so its projection cardinality gives the true dimension.

```sh
python3 develop/lift_map_value.py
python3 develop/check_lift_map_values.py
```

## Requested pattern versus full data

The requested tuple is (dim K,dim P,value list), omitting the exact K and
the domain basis. Its corrected output is 836 groups, 640 single-color,
196 multi-color. There are 267 patterns mixing distinct exact (K,P) groups;
the partition is not a refinement of the previous feature partition.

An immediate written obstruction explains why the list alone is insufficient:
span(e1) and span(e3) are distinct adjacent lines in S. Both maps are zero,
so both patterns are (0,1,(0)). Their respective canonical domain bases
are (1) and (4), which the tuple omits. The existing certificate colors
are 10 and 4, but the proper-coloring obstruction does not depend on those
choices. It is an omission of domain information, not insufficient precision
in f's values.

| Data retained | Groups | Single-color | Multi-color |
| --- | ---: | ---: | ---: |
| Exact (K,P) plus rank,image,kernel | 1662 | 1502 | 160 |
| Requested (dim K,dim P,value list) | 836 | 640 | 196 |
| Exact (K,P) plus complete basis values | 2809 | 2809 | 0 |

The [independent checker](../results/lift-map-values-check.json) compares every
pattern to the corrected author function, verifies the canonical basis using
an independent span-enumeration method, reproduces the entire requested JSON,
and reconstructs every one of the 2809 non-clique vertices from the full data.
All 160 previous mixed feature groups split into singleton vertices. These
finite statistics agree with the reconstruction proof below.

## Reconstruction proof

Fix K and P, choose a deterministic basis s1,...,sp of P, and retain the
quotient values f(si). Choose any representatives ti in T of these values.
Then

    U = K + span(t1+s1,...,tp+sp).

Each displayed lift lies in U, and their projections form a basis of P.
For any u in U, subtract the appropriate linear combination of these lifts
to obtain an element with zero projection, which lies in K. This proves
both inclusions. Changing ti by an element of K leaves the subspace unchanged.
Equivalently, linearity uniquely extends the basis values to all of P.
Thus K,P and the complete basis values determine U; no finer lift description
is needed to recover a vertex.

The canonical basis is deterministic in the chosen coordinates, and quotient
values are exported as their minimum integer representatives. These choices
give a reproducible representation. They do not supply a 15-label rule.
The meaningful next task is a proved assignment of colors using selected
relations among these lift values, satisfying the
[orthogonality criterion](lift-map-features.md#an-orthogonality-test-in-lift-coordinates).
Refining a complete representation further cannot advance that question.

The original certificate is unchanged. This round checks value encodings and
reconstruction, not all graph edges. No solver or Lean execution is involved;
the original final n6 Lean theorem retains four native-evaluation axioms.
Structural 15-coloring, the exact line chromatic number and n7 remain open.
