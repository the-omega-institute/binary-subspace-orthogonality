# Complete necessary roots and a legal stabilizer reduction for G

A nineteen-coloring in normal form G of the profile
(m5,m6;A,B,C)=(5,4;6,2,8) must produce one of the finite
42-point remaining sets constructed below. The subsequent six-heptad
covering question is unchanged when these sets are replaced by
representatives under a pointwise-hole symplectic group of order 64.
The complete catalog has 129,280 ordered roots and 127,984 distinct
remaining sets; the group reduces the latter to 2,306 representatives.
This is a necessary reduction, not an exclusion of G or a coloring witness.

## Marked geometry and the actual five-class hole

The [written four-form reduction](dimension-seven-five-four-charge.md)
gives a universal G normalization, by extending the ordered basis
(a,p,d) of the hole Lagrangian to a symplectic basis:

~~~text
z=127, M={0,3,12,15,48,51,60,63},
five-even sum p=12, four-even sum q=3,
D6 odd projections={3,48}, mixed projections={51,60},
characteristic projections={12,15,63}, h=60.
~~~

The pure-five class contains exactly one nonzero M point t. Its sum
p pairs to zero with every member, so t differs from p=12. D6
and both mixed classes have no even M point: each has an odd
projection in M, perpendicular to all even M points. The six pure
even heptads consequently contain the six other holes, one per class.
No permutation or orbit on t is assumed.

For a mixed sextet its Gram matrix is I+J and is nonsingular.
Its even members span E=z-perp. Both their sum and the odd
member's projection pair to one with every member, so they agree.
Thus the mixed-even sextets have sums 51 and 60, respectively.

Choose all four even blocks pairwise disjointly: the pure-five block,
the four even members of D6, and both mixed sextets. Their sizes
sum to 21; their complement has 42 even points and exactly
M minus {0,t}. A necessary completion partitions this complement
into six even heptads, each meeting M once. Keeping all 224
anchored heptads as candidate rows is correct: the 32 rows using
t cannot be contained in this complement or any successor.

## A written group preserving every marked role

Use the symplectic basis (3,12,48;65,71,95) and identify E with
pairs (x,y) in F_2^3 x F_2^3, with M={(x,0)} and pairing
x dot y' + y dot x'. For every symmetric 3-by-3 binary matrix S,
define

~~~text
g_S(x,y)=(x+Sy,y).
~~~

Symmetry gives (Sy) dot y' = y dot Sy', so g_S preserves the
alternating pairing. Also g_S g_T=g_(S+T), and g_S fixes M
pointwise. The six free entries of S give 64 distinct maps;
distinctness follows by applying them to the three dual basis vectors.
Extend each map to the original seven-dimensional dot space by
fixing z. This extension preserves both parity and the dot product.

Conversely, a symplectic map fixing M pointwise must preserve the
dual coordinates y, by pairing with the three basis vectors of M.
Linearity and pointwise fixation then give (x,y) -> (x+Sy,y);
preservation of the pairing makes S symmetric. Thus the displayed
group is the full pointwise stabilizer of M in the symplectic group.

Every named odd projection, p, q, h, and the actual t is fixed.
The maps therefore preserve each of the four block catalogs, their
disjointness, and the full family of remaining sets. They preserve
the anchored heptad catalog as well. A six-heptad cover of a
remaining set maps to such a cover of its image, and the inverse
map recovers the original cover. Thus cover existence is constant
on each orbit. This argument proves the reduction before any
covering search and does not infer symmetry from matching counts.

## Exact checks and scope

The [checker](../develop/check_dimension_seven_five_four_G_roots.py)
reconstructs all five catalogs and the entire ordered-root multiset
twice: once with bitmask clique recursion and disjointness, and once
with array recursion and direct set disjointness. It verifies the
original coordinate dot products, all 64 maps, their full composition
table, catalog invariance, and a complete disjoint orbit partition.
The [report](../results/dimension-7-five-four-G-roots.json) retains
every representative, its actual t, orbit size and ordered-root
multiplicity. Equal complements can come from different partial
partitions, so ordered roots and distinct remaining sets are recorded
separately.

| Actual pure-five hole t | Disjoint defect pairs | Ordered roots | Remaining-set orbits |
| --- | --- | --- | --- |
| 3 | 144 | 21,248 | 362 |
| 15 | 144 | 21,376 | 364 |
| 48 | 144 | 14,208 | 274 |
| 51 | 256 | 29,568 | 518 |
| 60 | 144 | 14,848 | 276 |
| 63 | 256 | 28,032 | 512 |
| Total | 1,088 | 129,280 | 2,306 |

The orbit-size distribution is six orbits of size 8, sixty-two
of size 16, 509 of size 32 and 1,729 of size 64. Their weighted
sum is 127,984. The action is not free, so simply dividing the
root count by 64 would give an incorrect covering workload.
Every representative records the missing hole t explicitly.
The average reduction is about 55.5 distinct remaining sets per
representative; this measures the input reduction, not a runtime
prediction or an exclusion of any remaining set.

No covering search or failed-state certificate is produced. G and
Z remain open; D and H retain their separate existing exclusions.
The raw profile remains open, with 27 five-plus-six and 39 three-six
count candidates overall. The exact dimension-seven chromatic numbers
remain open with lower bound 19. No new Lean or independent Pro
review is claimed. The original six-dimensional theorem retains
three standard and four native-evaluation axioms. The submitted
manuscript, extended working PDF and Zenodo record are preserved.

~~~sh
python3 develop/check_dimension_seven_five_four_G_roots.py --report /tmp/dimension-7-five-four-G-roots.json
~~~
