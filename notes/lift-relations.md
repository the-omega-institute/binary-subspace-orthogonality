# Lift relations reproduce every orthogonality edge

For T=span(3,12,48) and S=span(1,4,16), the lift data of U are
K=U intersect T, P=pi_S(U), and the map f:P -> T/K.
The diagnostic `develop/lift_relations.py` reads the colors from the
existing full 15-color certificate. It tests its first twenty non-clique
vertices, rather than all pairs.

## Requested output

The original script from `f1544ce58c4e71495759b11b52840ae854459e11` prints:

```text
Total groups: 836
Multi-color groups: 196
Full-data groups: 2809
Full-data multi-color groups: 0
Orthogonal pairs in sample: 87
Monochromatic orthogonal pairs in sample: 0
```

The sample has 190 distinct pairs. The literal tuple still omits exact K and
the domain basis; its 196 mixed groups are the same partition as the previous
value-pattern diagnostic. The full K,P and basis values encode the vertex,
so a fixed certificate color is recovered by looking up that vertex.

We include zero when forming P so every projection is actually a subspace.
The omission previously affected zero inclusion and reported dimensions for
K=0. The printed counts above are unchanged. The script now exports its
sample identities and counts in [lift-relations.json](../results/lift-relations.json).

## Exhaustive comparison with the original graph

The [independent checker](../develop/check_lift_relations.py) verifies the
author's K,P and basis values against coefficient-tuple span enumeration,
coordinate projection and quotient cosets, and checks every linear extension
and reconstructed vertex. Its pair comparison calls the author's unchanged
`are_orthogonal` function. Only the deterministic basis and extension functions
are memoized; no pair is sampled or skipped.

The comparison covers every distinct pair of all 2824 vertices, including
the fifteen clique vertices, using independently computed coordinate
orthogonal-complement masks. The [executed record](../results/lift-relations-check.json)
gives:

| Scope | Distinct pairs | Orthogonality edges | Criterion disagreements | Monochromatic edges |
| --- | ---: | ---: | ---: | ---: |
| Outside the clique | 3943836 | 42000 | 0 | 0 |
| Full graph | 3986076 | 44968 | 0 | 0 |

This validates the lift-coordinate adjacency implementation on this finite
graph and rechecks its existing assigned colors.

## Why basis tests suffice

For U=(K,P,f) and W=(L,Q,g), the existing
[lift-coordinate criterion](lift-map-features.md#an-orthogonality-test-in-lift-coordinates)
requires K perpendicular to Q and L perpendicular to P, followed by

    B(s,r) = dot(s,r) + dot(f(s),r) + dot(s,g(r)) = 0.

Choose bases of P,Q and representatives in T for their lift values.
Extend those representatives linearly to maps F:P -> T and G:Q -> T.
The form

    B(s,r) = dot(s,r) + dot(F(s),r) + dot(s,G(r))

is bilinear. Thus testing the basis pairs of P and Q suffices; the two
cross-kernel orthogonality conditions can likewise be tested on bases.
Any other representative differs by K or L, whose additional pairings
vanish by those cross-kernel conditions. This justifies both the original
all-domain test and a future implementation that tests bases.

The term dot(s,r) is essential: S is a complement, not a totally isotropic
subspace. For instance span(1) and span(1,4) have zero lift maps but are not
orthogonal. Cross-kernel conditions are also essential: span(3) and span(1)
would pass the lift-value expression alone, but their dot product is one.

## Next mathematical step and reproduction

A structural rule must supply a function c(K,P,f) in fifteen labels, specify
its auxiliary coordinate choices, and prove the same label cannot occur for
two distinct vertices satisfying the criterion. Reading colors from
`full-15-coloring.json` supplies an existing certificate lookup. No new
15-label formula is supplied by these diagnostics.

```sh
python3 develop/lift_relations.py
python3 develop/check_lift_relations.py
```

The full certificate and manuscript PDF are unchanged. The manuscript
already includes reconstruction and the structural question; this diagnostic
adds supporting verification, not a new manuscript theorem.
The exact line result chi(Gamma_6)=12 remains proved by its written lower
bound and finite certificate. Structural full-subspace coloring and n7 remain
open. No solver or Lean run was needed; the historical full-subspace n6 Lean
theorem retains three standard plus four native-evaluation axioms.
