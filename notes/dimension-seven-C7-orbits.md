# Complete C7 marking orbits with actual defect holes

**Finite theorem.** For the necessary C7 profile `(4,4,4;3,5,7)`, the
4,200 odd markings augmented by all distinct actual defect-hole
allocations give **29,232 markings and 176 orbits** under the full
168-element ordered-hole-pair group. Case 0 has **7,056 markings and
44 orbits**; case 1 has **22,176 markings and 132 orbits**. Three
case-0 orbits have size 56 and stabilizer order three. Every other
orbit has size 168 and trivial stabilizer. This supplies a complete
legal marked normalization for the next joint-component problem.
The candidate row and exact n=7 remain open; the lower bound is 19.

## The full group, proved before orbit reduction

The [capacity-equality reduction](dimension-seven-C7-equality.md)
orders the transverse hole pair M,N so that the number y of defects
with odd projections in M is zero or one. Exchanging M,N in a full
coloring replaces y by 3-y, so exactly one of the two orientations
satisfies y<=1. We retain that orientation. An exchange is therefore
not an additional symmetry of the oriented marking family.

Choose a basis of M and its symplectic dual basis in N. Relative to
E=M direct-sum N, the form is

```text
<(x,y),(x',y')> = x^T y' + (x')^T y.
```

Every isometry preserving M and N individually is block diagonal.
If its restrictions are A and D, form preservation requires A^T D=I,
hence D=A^{-T}. Conversely every invertible A gives such an isometry.
Thus the full ordered-pair group is GL(3,2), of order
`(8-1)(8-2)(8-4)=168`. There is no shear freedom while both hole sides
are fixed. The map extends to the original seven-dimensional dot
space by fixing z=127: z has norm one and E=z-perp, so the orthogonal
direct-sum extension preserves the original dot form.

Normalize M's basis to (3,12,48) and N's dual basis to (65,71,95).
The [builder](../develop/build_dimension_seven_C7_orbits.py) constructs
the group from every ordered basis image in M and its unique dual
in N. The [independent auditor](../develop/check_dimension_seven_C7_orbits.py)
instead starts with every ordered basis image in N and derives its
dual in M. Expansion in the original seven-vector basis gives the
full maps on all 128 original vectors. The two exact group sets agree.

## What the markings retain

A marking records the unordered characteristic triple and three
triples `(g_i,s_i,k_i)`. Here g_i is the defect's projected charge,
s_i its other odd projection and even sum, and k_i its actual even
hole on the opposite side. Every k_i pairs to one with both g_i,s_i;
the three actual holes are distinct. The five mixed odd projections
are the unused points of M* union N*.

The three defects have the same size and parity type, so their class
labels can be permuted. We therefore store the three triples as an
unordered set. This keeps each charge, partner and actual hole together:
it permits no independent exchange of g_i and s_i, no interchange of
an odd charge with an even hole and no permutation of unequal roles.
This is relabeling of equal defect classes, not a recoloring operation.

The earlier two independent odd-marking constructions give 1,176
case-0 and 3,024 case-1 markings. All possible distinct actual-hole
allocations are retained. Their totals are respectively
`196*2+588*6+392*8=7056` and `1008*6+2016*8=22176`.
Every hypothetical coloring yields one of these augmented markings
after the justified ordered-pair normalization.

## Complete orbits and nontrivial stabilizers

For each unassigned marking, take the least record and transport it
under every full group map. The [artifact](../results/dimension-7-C7-orbits.json)
stores the representative, every orbit member, orbit size and the
number of full group maps fixing that representative. Exhaustive
coverage is checked against the separately reconstructed augmented
marking set. The counts are:

| Case | Augmented markings | Orbits of size 56 | Orbits of size 168 | Total orbits |
| --- | --- | --- | --- | --- |
| 0, characteristic charge zero | 7,056 | 3 | 41 | 44 |
| 1, characteristic charge nonzero | 22,176 | 0 | 132 | 132 |
| Total | **29,232** | **3** | **173** | **176** |

The three size-56 orbits have stabilizer order three; the other
stabilizers have order one. Each orbit satisfies
`orbit_size * stabilizer_order = 168`. In particular the complete
augmented action is not free, and dividing 29,232 by 168 would lose
the three exceptional orbits. No transitivity assumption is used.

The full group preserves original class independence, charge/partner
roles and actual-hole membership. The auditor reconstructs all 672
one-hole local defects with array four-clique enumeration, checks their
actual holes and checks all 112,896 local defect actions. Thus component
catalogs and future joint compatibility conditions transport under
the very maps used in the marking reduction.

## Verification and remaining problem

The [report](../results/dimension-7-C7-orbits-check.json) records
2,752,512 original-dot-product pair controls, all 28,224 full group
compositions, complete marking coverage and every orbit/stabilizer
identity. Four invalid artifacts are rejected: a missing orbit, an
incorrect actual hole, a missing group map and a false stabilizer order.
The preceding equality/local audit is rerun and matched exactly;
its five inherited report/source/dependency bindings remain checked.
Historical spread-completion and covering audits are not rerun.

This classifies necessary marked odd data and defect holes. Complete
joint roots still require disjoint choices of the three four-even
defect blocks and five six-even mixed blocks, with all mixed actual
holes retained. These eight components occupy 42 even points; the
21-point remainder would require three pure heptads, each meeting both
hole sides. No joint-root construction or covering search is run here.
There is no raw exclusion: lists stay25/34, with57 C6/7 and2 C5, and
no size-four C8 row. Characteristic sizes4..8 and exact n=7 remain open.
No new Lean or independent Pro review is claimed; the original n=6
theorem retains three standard plus four native-evaluation axioms.

```sh
python3 develop/build_dimension_seven_C7_orbits.py --orbits /tmp/n7-C7-orbits.json --seconds 20
python3 develop/check_dimension_seven_C7_orbits.py --orbits /tmp/n7-C7-orbits.json --report /tmp/n7-C7-orbits-check.json
```
