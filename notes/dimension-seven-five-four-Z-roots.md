# Complete necessary roots and marked stabilizer for the zero-sum form Z

**Theorem.** In normal form Z of a nineteen-coloring of Gamma_7 with
characteristic class size four and profile (m5,m6;A,B,C)=(5,4;6,2,8),
the necessary six-heptad covering problem is invariant under a marked
symplectic stabilizer of order 128. The group includes the 64-element
pointwise-hole stabilizer and the exchange of the two mixed classes.
The actual pure-five hole is transported with the root, not discarded.
The complete necessary family has 1,284,736 ordered partial partitions
and 1,271,424 distinct 42-point remaining sets. The marked group reduces
these sets to 10,837 representatives, all retained in the report.

This is a reduction of the remaining covering problem. No root is solved
or excluded here. Z, the raw profile and the exact dimension-seven
chromatic numbers remain open, with lower bound 19. The other three
marked forms D, H and G have their separate covering exclusions.

## Necessary roots retain both mixed classes

Use the [four-form normalization](dimension-seven-five-four-charge.md):

~~~text
z=127, M={0,3,12,15,48,51,60,63}, p=0, q=15,
D6 odd projections={15,48}, mixed projections={3,12},
characteristic projections={51,60,63}, h=48.
~~~

In E=z-perp, let F be the pure-five block, Q the four-even D6 block,
and B,C the even sextets of the two mixed classes. Their catalogs are
defined by the original dot product: pairwise dot products within
each even block are one; sum(F)=0; sum(Q)=15 and its members pair to
one with both 15 and 48; B and C pair to one with 3 and 12 respectively.
Adding the odd members z+15,z+48 to Q, z+3 to B and z+12 to C gives
the required original color classes. No parity count alone asserts
that these blocks are disjoint or completable.

The hole-capacity argument forces F to contain exactly one point
t of M minus zero. Q,B,C avoid M. Each ordered disjoint choice
(F,Q,B,C) occupies 21 even points and leaves a 42-point set R
containing exactly the six holes other than t. Every full coloring
therefore supplies one such necessary root R. Its six pure even
heptads must partition R and each meet M once. A covering solution
would still need the remaining odd partial spread and all class
conditions checked before it could be a full coloring witness.

## Written marked group, before any covering search

Take the symplectic basis (3,12,48,65,71,95) of E and write a point
as (x,y) in F_2^3 plus F_2^3. The form is x dot y' + y dot x',
and M is y=0. For a symmetric binary matrix S, define

~~~text
g_S(x,y)=(x+Sy,y).
~~~

Symmetry of S cancels the two extra bilinear terms, so g_S preserves
the form and fixes M pointwise. There are 2^6=64 such maps. Let A
exchange the first two coordinates and fix the third, and define

~~~text
k(x,y)=(Ax,Ay).
~~~

Since A^T A=I, k is symplectic. It fixes 15 and 48, exchanges 3
and 12, and permutes {51,60,63}, preserving characteristic charge
48. It exchanges the two mixed catalogs while preserving F and Q.
Moreover k g_S k=g_(A S A), and k^2=1. Thus the maps g_S k^epsilon,
epsilon in {0,1}, form a group of order 128. The two halves are
distinct by their restriction to M.

This is the full symplectic stabilizer of these marked roles:
q=15 and h=48 are fixed and the mixed projections {3,12} are
preserved as an unordered pair. Hence the restriction to M is
either the identity or A. After composing with k if necessary, a
map fixes M pointwise. Such a symplectic map has block form
[[I,S],[0,I]], with S symmetric, so belongs to the stated group.
The extension fixing z preserves the original dot form.

Every group element permutes the pure-five and D6 catalogs and
either preserves or exchanges the two mixed catalogs. If it exchanges
them, reorder their images to restore the ordered roles B,C.
It preserves disjointness and maps a necessary root R to another
necessary root, with the same ordered-root multiplicity. It also
permutes the complete catalog of even heptads meeting M once.
Consequently R has a six-heptad cover if and only if its image does.
This proves the orbit reduction without a covering search.

Under k the actual hole t may change: 3 exchanges with 12, and 51
with 60, while 15,48,63 remain fixed. A root determines t uniquely
as the missing M point. There is no transitivity assumption across
these five hole orbits. In particular, no normalization silently
replaces the actual hole by a preferred one.

## Exact audit and remaining scope

The checker independently constructs the block catalogs by array and
bitmask clique recursion. It constructs the ordered-root multiset
in two ways: successive bitmask disjointness tests and a set-based
join of independently enumerated disjoint mixed pairs with defect
pairs. It verifies the original color-class dot products, all 128
maps, their closure and catalog actions, then partitions every
necessary root into an orbit. Representatives retain their actual
hole and ordered-root multiplicity. The report binds this note,
the checker and the preceding written normalization by SHA-256.

The [checker](../develop/check_dimension_seven_five_four_Z_roots.py) and
[complete report](../results/dimension-7-five-four-Z-roots.json) give the
following accounting. Equal complements may arise from different ordered
partial partitions, so their multiplicities are retained separately.

| Orbit of the actual pure-five hole t | Disjoint defect pairs | Ordered roots | Remaining-set orbits |
| --- | --- | --- | --- |
| {3,12} | 3,904 | 273,024 | 2,405 |
| {15} | 1,616 | 162,240 | 1,373 |
| {48} | 1,600 | 161,408 | 1,366 |
| {51,60} | 3,904 | 416,192 | 3,438 |
| {63} | 2,560 | 271,872 | 2,255 |
| Total | 13,584 | 1,284,736 | 10,837 |

There are 576 ordered disjoint mixed-sextet pairs. The remaining-set
orbit sizes are 16,32,64,128, with multiplicities 8,140,1,584,9,105.
Their weighted sum is exactly 1,271,424. Thus the action is not free;
dividing the number of sets by 128 would give an incorrect workload.
The average reduction is about 117.3 sets per representative, measuring
the number of covering inputs rather than predicting search time.
The checker verifies 524,288 symplectic pair comparisons and 1,048,576
composition point comparisons, all catalog actions, and the complete
disjoint orbit partition. Its explicit bounds are 90 seconds and two
million distinct roots; an exhausted bound writes no complete report.

No covering search or failed-state certificate, SAT, Lean, or new
independent Pro review is claimed. This work leaves the submitted
manuscript and the extended working PDF unchanged. The six-dimensional
formal theorem retains three standard and four native-evaluation
axioms. Publication and submission decisions remain separate.

~~~sh
python3 develop/check_dimension_seven_five_four_Z_roots.py --report /tmp/dimension-7-five-four-Z-roots.json
~~~
