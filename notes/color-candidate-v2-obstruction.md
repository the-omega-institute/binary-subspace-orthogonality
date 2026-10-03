# Second candidate: the lift bit and the seven-line label obstruction

Reza's second candidate in `04d03c6ba8af23b1409f43801e1a8efda12c38b0`
passes label availability but still fails same-label separation. There is
also a written obstruction to every rule that uses only the seven line
labels of T, regardless of how much lift data it uses.

## What the second tie-breaker actually retains

The code chooses the first or second available line, using

    idx = dim({0,t1}) if t1 else 0,

where t1 is the first canonical lift representative. Thus idx is exactly
zero when t1=0 and one otherwise. It retains one zero/nonzero bit, rather
than the value of t1 or the rest of the lift map. Every non-clique P is
nonzero and has at least four available lines, so the modulo operation does
not alter the index and the plane fallback is unreachable.

The previous span(1),span(2) example is separated, with labels span(3),
span(15). But take U=span(2) and W=span(13). These are orthogonal because
dot(2,13)=0. Both have K=0, P=span(1), with first lift values 3 and 12:
2=3+1 and 13=12+1. Both lift values are nonzero, so both vertices receive
the second available label span(15).

Their X,Y matrices are empty, and the lift matrix is

    Z=[dot(1,1)+dot(3,1)+dot(1,12)]=[1+1+0]=[0].

Availability holds since dot(15,1)=1, but this is a monochromatic edge.
Any function retaining only (K,P,zero/nonzero of this first lift value)
also fails on this pair. This does not exclude use of full lift data.

## Fourteen distinct labels are necessary outside the fixed clique

**Proposition.** The graph induced by vertices U not contained in
T=span(3,12,48) contains a fourteen-vertex clique. Consequently any proper
coloring of these vertices uses at least fourteen distinct labels. In
particular no rule using only the seven nonzero line labels of T can work,
even with all lift values available.

**Proof.** Put T'=span(5,18,40). Its three generators have disjoint supports
of size two and are independent, so T' has dimension three and is totally
isotropic. Directly,

    T  = {0,3,12,15,48,51,60,63},
    T' = {0,5,18,23,40,45,58,63},
    T intersect T' = span(63).

There are seven lines, seven planes and T' itself among the fifteen nonzero
subspaces of T'. All are pairwise orthogonal. Exactly one is contained in
T, namely span(63), because any such subspace lies in T intersect T'.
The remaining fourteen therefore form a clique outside T. They need
fourteen distinct labels in every proper coloring. QED.

This is a coordinate instance of the existing totally-isotropic clique
construction, not a new full-graph chromatic theorem. It proves a lower
bound for the induced graph, not its exact chromatic number. A fifteen-label
construction remains possible in principle; it must actually use higher
dimensional labels as well as lines on the non-clique vertices.

The candidate's seven plane entries still represent only five distinct
planes, so its full declared inventory has only thirteen distinct labels.
That inventory is insufficient even if the currently unreachable entries
are enabled. Generate all fifteen nonzero subspaces of T for a future rule;
repairing the inventory alone does not prove a valid assignment.

## Replayed output and independent checks

The original unmodified script prints:

```text
Vertices outside the clique: 2809
Distinct labels used: 5
Condition 1 violations: 0
Condition 2 violations: 13945

Label distribution:
  Label size  2: 1735 vertices
  Label size  2: 575 vertices
  Label size  2: 394 vertices
  Label size  2: 70 vertices
  Label size  2: 35 vertices
```

The [independent checker](../develop/check_color_candidate_v2.py) verifies
all 2809 lift tuples and labels and checks original coordinate adjacency
on every same-label pair, independently of the author's matrix predicate:

| Label basis | Vertices | Same-label pairs | Monochromatic edges |
| --- | ---: | ---: | ---: |
| 3 | 575 | 165025 | 638 |
| 12 | 1735 | 1504245 | 10936 |
| 15 | 70 | 2415 | 289 |
| 48 | 394 | 77421 | 2016 |
| 51 | 35 | 595 | 66 |
| Total | 2809 | 1749701 | 13945 |

It checks the explicit counterexample against the author's predicate and
verifies the fourteen outside-clique vertices and all 91 pairs. Their
bases are exported in [the JSON report](../results/color-candidate-v2-check.json).
Adjoining the missing zero to 1016 author projections changes no labels.
The author candidate source remains byte-for-byte unchanged.

```sh
python3 develop/color_function_candidate_v2.py
python3 develop/check_color_candidate_v2.py
```

The next candidate needs more than a zero/nonzero lift bit and an inventory
large enough for the fourteen-clique, followed by proofs of availability and
same-label separation. The existing finite chi(O_6*)=15 and chi(Gamma_6)=12
results, manuscript and certificates are unchanged. Structural coloring
and n=7 remain open. No solver or Lean run is involved; the historical
full-subspace six-dimensional Lean theorem retains three standard plus
four native-evaluation axioms.
