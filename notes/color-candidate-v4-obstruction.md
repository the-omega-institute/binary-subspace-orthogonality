# Fourth candidate: a common-palette residue collision

The fourth candidate from `22aee3de1c2e7460ae00a5c5fbe26be5e3d3dfcc`
is committed as `develop/color_function_candidate_v4`, without a .py extension.
The inventory now contains all fifteen distinct nonzero subspaces of T.
The rule separates the preceding zero-lift example, but is still improper.

## Answers to the four requested diagnostics

| Diagnostic | Result |
| --- | --- |
| Different labels on all 2809 outside vertices | 15 |
| Different labels on the fourteen-clique | 8, with 7 monochromatic edges |
| Label of span(5) | span(12) |
| Label of span(21) | span(48) |
| Condition 1 violations | 0 |
| Condition 2 violations | 2873 |

The original script gives these results. The independent checker verifies
all lift data and labels, tests all 346362 same-label pairs from original
coordinate dot products, and verifies all 91 pairs of the fourteen-clique.
The complete label distribution and fixture labels are exported in
[the check report](../results/color-candidate-v4-check.json).

## Two adjacent lines with the same projection

Let U=span(11) and W=span(52). In coordinates these generators have disjoint
supports {1,2,4} and {3,5,6}, so their dot product is zero. Both have K=0
and P=span(4). Their lifts on the basis vector 4 are 15 and 48:

    11 = 15 + 4, 52 = 48 + 4.

The common projection has eleven available labels. The keys are

    4*64+15 = 271, 4*64+48 = 304,
    271 mod 11 = 304 mod 11 = 7.

Both therefore receive the same label span(12,51). Availability holds, but
the pair is orthogonal. Its X,Y matrices are empty and

    Z=[dot(4,4)+dot(15,4)+dot(4,48)]=[1+1+0]=[0].

The pair directly rejects v4. It is not an instance of the old zero-lift
failure: the projection and kernel agree, while the lift values differ.

## An obstruction to an entire affine-residue family

**Proposition.** In the fixed integer coordinates and lift representatives
above, no rule which chooses from a common ordered palette by

    index = (c(K,P)*t + b(K,P)) mod |palette(P)|

on one-dimensional projection domains can give a proper coloring on all
vertices. Here b,c are arbitrary integer-valued functions, t is the sole
canonical lift value, and the ordered palette may depend on K,P but is the
same for vertices with the same K,P.

**Proof.** Apply the rule to U,W above. Their K,P and eleven-entry palette
agree. The lift values differ by 48-15=33, divisible by eleven. The two
indices differ by 33*c(K,P), hence agree modulo eleven. The labels are equal
for any common palette ordering, but U,W are adjacent. QED.

Changing a common projection-dependent seed, a multiplier, or the common
label order cannot repair this example within the displayed family.
This does not rule out nonlinear selection, lift-dependent palette ordering,
or a geometric construction using the full (K,P,f). It is not a claim that
every numeric encoding must fail.

The next candidate should use separation constraints to choose labels,
rather than only changing parameters in this affine index. The fourteen-clique
and this same-projection pair are small necessary tests before a full replay;
passing them is not a proof of the full coloring.

## Reproduction and scope

```sh
python3 develop/color_function_candidate_v4
python3 develop/check_color_candidate_v4.py
```

The [independent checker](../develop/check_color_candidate_v4.py) reconstructs
projections and quotient lift values independently and matches all author
labels against the displayed base64 construction. Adjoining omitted zero in
1016 original projections changes no labels. The author file is preserved
unchanged; no repaired variant or new solver search is involved in this round.

The manuscript TeX, ten-page PDF and existing coloring certificates are
unchanged. Exact chi(O_6*)=15 and chi(Gamma_6)=12 remain established.
Structural coloring and n=7 remain open. No Lean run is involved; the
historical full-subspace n6 Lean theorem retains three standard plus four
native-evaluation axioms. The previous fourteen-clique still provides an
induced-graph lower bound, not its exact chromatic number.
