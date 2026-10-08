# Eight ordered marked forms for (4,5,6;6,1,8)

**Theorem.** The [completion-source geometry](dimension-seven-four-five-six-charge.md)
of `(4,5,6;6,1,8)` has eight exhaustive ordered marked forms.
Every full ordered marked stabilizer has order eight and fixes
every point of the hole Lagrangian M. The eta=0 forms have one
possible completion-source case each; the eta=1 forms have two,
giving twelve source-case branches. This establishes the legal
symmetries for later joint-root construction, while retaining all
actual holes. The row stays open and the count lists stay **25/36**.

## Ordered roles and exhaustive normal forms

Retain D0, D1, P, J from the preceding theorem. Their even/odd
sizes are respectively (4,2), (5,1), (6,0), (6,1). Thus each role
is distinguished by the original coloring. The charge identifies
b within D0, so its other odd projection a is distinguished too.
The source theorem gives a basis (a,c,d) of M and two completions
t,q outside M satisfying

```text
t+q=a+c+d,     t dot q=1,
t dot(a,c,d)=(eta,1,eta),     eta in {0,1}.
```

The reversible t-transfer between D1 and J is a recoloring.
It exchanges which class is undersized. It is not an isometry
preserving the original ordered class roles; those classes have
different sizes. It therefore does not justify the paired-role
exchange used in the earlier two-hole normalization.

Choose a symplectic dual basis to (a,c,d). In its coordinates,
write t=(x,y) with y=(eta,1,eta), which is nonzero. First send
the ordered basis of M and its dual to

```text
(a,c,d,f1,f2,f3)=(3,12,48,65,71,95).
```

These are symplectic coordinates for E=z-perp, z=127. A
pointwise-M symplectic shear (x,y)->(x+B y,y), with B symmetric,
can remove the first coordinate of t: for any fixed nonzero y,
the map from symmetric B to B y is onto M. To see this, change
dual coordinates so that y is a coordinate vector; its image is
an unrestricted column of a symmetric matrix. This is a coordinate
argument, not an exchange of the coloring's marked roles.

We can consequently take t=sum y_i f_i and q=t+63. The remaining
distinct point b has the four positions a+c, a+d, c+d, a+c+d.
They cannot be identified by an isometry preserving a,c,d in order.
The eight forms are therefore

| eta | a,c,d | t | q | b | Characteristic charge h=b+63 |
| --- | --- | --- | --- | --- | --- |
| 0 | 3,12,48 | 71 | 120 | 15,51,60,63 | 48,12,3,0 respectively |
| 1 | 3,12,48 | 89 | 102 | 15,51,60,63 | 48,12,3,0 respectively |

Each symplectic isometry of E extends to the original binary dot
space by fixing z. Normalization therefore transports original
class conditions and actual holes. It does not identify compatible
component choices or hole allocations merely because their charges
have the same form.

## The full ordered marked stabilizer has order eight

Every symplectic map preserving M has coordinate form

```text
(x,y)->(Lx+B L^(-transpose)y, L^(-transpose)y),
```

where L is invertible and B is symmetric. Fixing a,c,d in order
forces L=I. Fixing the normalized t=(0,y) then requires B y=0;
q=t+a+c+d is automatically fixed. The space of symmetric 3 by 3
matrices has dimension six. The surjectivity just proved gives
three independent conditions, leaving dimension three and exactly
eight maps. They also fix b and every characteristic projection.
Conversely every such shear preserves every marking, so these
are the full groups, independent of b. There are no additional
role-exchange maps. In particular every actual hole is fixed
pointwise: different ordered actual-hole allocations cannot be
collapsed by these groups.

There are 168 invertible L and 64 symmetric B, giving 10,752
maps in the full M-preserving symplectic group. Each of the
eight forms has 1,344 ordered marked images and eight maps
giving each image. Their image sets are disjoint and together
give all 10,752 markings from the preceding charge theorem.
This finite control agrees with the written exhaustiveness proof;
group size alone is not used to infer orbit completeness.

## Complete local component catalogs for both sources

The source theorem forces t,q out of D0, q out of D1 and J,
t out of P and Hq, and q out of Ht when that source exists.
For each marked form, retain precisely these necessary restrictions.
P is a one-hole sextet of sum q; Hq is an anchored heptad
containing q and avoiding t. For a pure t-source, Ht is an
anchored heptad containing t and avoiding q, and J avoids t,q.
For a mixed t-source, eta=1 and J contains t while avoiding q.

| Component | eta=0 | eta=1 |
| --- | --- | --- |
| D0 even block | 16 for each b | 16,16,16,8 for b=15,51,60,63 |
| D1 even block | 4 | 4 |
| P, Hq, Ht separately | 18 each | 18 each |
| J even block, pure t-source | 32 | 22 |
| J even block, mixed t-source | Impossible | 4 |

The last b=63 D0 restriction is a local catalog restriction, not
a profile exclusion. These catalogs contain every component of
a hypothetical coloring in its specified source branch. All
joint disjointness constraints must still be imposed before
they give a complete necessary root family.

There are 144 disjoint ordered local pairs (P,Hq) in each form.
Their actual holes give twelve ordered allocations, twelve pairs
per allocation; both holes have ell-value one and are distinct.
Every group element preserves each allocation. The auditor records
the full pair and component orbit partitions, with stabilizers
and orbit--stabilizer checks. The 144 pairs have 48 orbits: 24 of
size two and 24 of size four, so the actions are not free.
The pairs alone are not jointly compatible roots with D0,D1,J,Ht.

## Necessary remainders differ between the two source cases

For a pure t-source, fix the mutually disjoint even components
D0,D1,P,J,Hq,Ht of a hypothetical coloring. Their sizes are
4,5,6,6,7,7, totaling 35. Their complement in the 63 nonzero
even points has size 28. The distinct actual holes of P,Hq,Ht
use three of M's seven points, leaving four holes and precisely
four residual pure even heptads.

For a mixed t-source, fix D0,D1,P,J,Hq. Their even sizes are
4,5,6,6,7, totaling 28. The remainder has size 35; P,Hq use two
distinct holes, leaving five holes and five residual pure heptads.
These are necessary specifications for complete joint roots,
not assertions that any compatible root or coloring exists.

Each residual heptad can meet M at most once, so in either case
every residual heptad must meet a remaining hole. The complete
eligible catalog for a later necessary cover test is therefore
the 224 anchored even heptads, filtered by containment in the
specific remainder. The previous five-heptad certificate concerns
different fixed components and completion locations and is not
a proof for either of these new necessary problems.

## Verification and next bounded problem

The [auditor](../develop/check_dimension_seven_four_five_six_symmetry.py)
constructs every M-preserving map from all L and symmetric B,
checks the original basis Gram entries and matches the eight full
normal-form image sets to all charge markings. It checks full
original-dot-product preservation and group closure for both
eight-element stabilizers. Independent array and bitmask catalogs
agree for sizes 4,5,6,7. Every role catalog, local pair orbit and
actual-hole transport is checked without role exchange or a
free-action assumption.

The [report](../results/dimension-7-four-five-six-symmetry.json)
binds the source theorem and nine inherited covering reports with
their exact source/certificate/dependency identities. The previous
charge/source auditor and historical covering audits are not rerun.
No complete joint roots, covering search, new cover certificate,
Lean or independent Pro review is produced here. Exact n7 remains
open with lower bound 19; the original n6 theorem retains three
standard and four native-evaluation axioms. The submitted snapshot
and all historical records are preserved.

Next construct complete jointly disjoint component families for
the twelve marked source branches, retaining P/Hq/Ht actual holes
and original D0/D1/P/J roles. Use the proved 28-point/four-hole
pure-source or 35-point/five-hole mixed-source specification and
the full eight-element marked groups. Both eta patterns and all
four b positions must remain represented.

```sh
python3 develop/check_dimension_seven_four_five_six_symmetry.py --report /tmp/dimension-7-four-five-six-symmetry.json
```
