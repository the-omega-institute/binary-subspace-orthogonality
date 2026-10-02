# Fifth candidate: taking the lift span forgets the map

The fifth candidate at `3e9f649dcf8107fe86f2d330b1553b558300c8c7`
separates span(11) and span(52), but still fails same-label separation.
The failure is explained by the existing planes in Proposition 5.5 of the
joint manuscript, rather than by a new search.

## Requested diagnostics

| Diagnostic | Result |
| --- | --- |
| Distinct labels on 2809 outside vertices | 15 |
| Distinct labels on the fourteen-clique | 7, with 17 monochromatic edges |
| Label of span(11) | span(15) |
| Label of span(52) | span(12,48) |
| Label of span(5) | span(3,48) |
| Label of span(21) | T |
| Condition 1 violations | 0 |
| Condition 2 violations | 2636 |

The independent checker tests all 706262 same-label pairs using original
coordinate dot products, verifies all lift tuples and labels, and checks
all 91 pairs of the fourteen-clique. The complete distribution is in
[the check report](../results/color-candidate-v5-check.json).

For span(52), the implemented lexicographic tie order selects span(12,48),
not span(3,48). Their vector lists are [0,12,48,60] and [0,3,48,51], but
the latter is unavailable for P=span(4): both 3 and 48 pair to zero with 4.
The former is available since dot(12,4)=1.

## The span is exactly the other coordinate projection

Write V=T direct-sum S, with T=span(3,12,48) and S=span(1,4,16).
For U, let K=U intersect T, P=pi_S(U), and f:P -> T/K. Choose a basis
s_i of P and representatives t_i of f(s_i). Then

    U = K + span(t_i+s_i),
    A0 = K + span(t_i) = pi_T(U).

The first identity follows by subtracting the chosen lifts from any vector
of U to obtain an element of K; the second follows by applying pi_T.
Thus A0 is independent of the basis and representative choices. Taking this
span retains the T-projection R, but loses which T-component corresponds to
each S-component. V5 depends solely on P and R, including its containment
and fallback branches. The identity is also checked on all 2809 vertices.

## Existing Proposition 5.5 directly rejects v5

Take U=span(13,6) and W=span(9,14). Their vector lists are {0,6,11,13}
and {0,7,9,14}. All four cross dot products of the displayed bases vanish,
so these distinct planes are adjacent. Both have

    K=0, P=span(1,4), R=span(3,12).

Their maps differ: on arguments 1,4, the values are respectively 12,15
for U and 15,3 for W. Both maps are isomorphisms with the same image.
Since dot(3,1)=1, the common A0=R is available. Both planes therefore
return span(3,12) immediately, before any tie order or fallback is used.

This is an application of [the existing lift-feature obstruction](lift-map-features.md)
and manuscript Proposition 5.5. It proves that no proper coloring can depend
solely on P and R. Changing an ordering, a preferred containing label or
the zero fallback cannot repair this loss of the map. A future construction
must retain enough of the correspondence f(s), and explain how it separates
this pair and the fourteen-clique before a full replay.

## Reproduction and scope

The author committed the file at the repository root. Its original ROOT
setting pointed one directory too high and could not find the certificate.
The sole repair is `Path(__file__).resolve().parent`; the mathematical rule
is unchanged. Run from the repository root:

```sh
python3 color_function_candidate_v5.py
python3 develop/check_color_candidate_v5.py
```

This round checks the requested finite candidate and supplies the written
projection argument. The TeX, ten-page PDF and established certificates are
unchanged. Exact chi(O_6*)=15 and chi(Gamma_6)=12 remain established;
the structural fifteen-color formula and n=7 remain open. The outside
fourteen-clique supplies a lower bound, not an exact chromatic number.
No solver or Lean run was needed. The historical full-subspace n6 Lean
theorem retains three standard plus four native-evaluation axioms.
