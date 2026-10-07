# Complete necessary roots for the transferred two-hole branch

This note constructs all jointly disjoint choices of the five even
components in the transferred two-hole `(4,6,6;5,2,8)` branch.
The [preceding written normalization](dimension-seven-four-six-six-two-hole.md)
gives three exhaustive marked forms and their full groups of orders
8,16,16. Its paired pure/mixed roles and actual holes remain part
of the data. The result concerns that transferred subbranch.

## Why five components give the complete necessary roots

Fix `a,c,d,u,v=(48,51,60,95,96)` and `b=3,15,63`.
Let `D,P_u,P_v,J_c,J_d` denote the even components of the
four-even/two-odd defect, two pure six-defects and two mixed heptads.
The complete local catalogs in the preceding argument give:

- `D`: four even points, sum a, pairing one with a and b;
- `P_u,P_v`: six even points with sums u,v, one actual hole each,
  avoiding the other completion v,u respectively;
- `J_c,J_d`: six even points with sums c,d and containing u,v
  respectively.

Every component is a clique for the original dot definition, with
the prescribed odd members appended for D and the mixed classes.
There are 16,18,18,6,6 local choices. Retaining exactly the choices
that are pairwise disjoint exhausts every possible five-component
family in a normalized coloring. Conversely each retained family
is a valid partial collection of these five classes.

These components use 28 of the 63 nonzero even points. Their
complement R has 35 points. Only the two pure defects meet the
hole Lagrangian M, each once, so R contains exactly five of its
seven nonzero points. The two actual holes are distinct. The sum
of the used points is a+u+v+c+d=0, hence the sum of R is also zero.
Each completed coloring must partition R into five pure even
heptads. A heptad meets M at most once, so each must meet one of
these five holes. The 224 anchored heptads are the complete
admissible catalog for that later covering problem.

The group acts on the entire five-component tuple. An exchanged
lift transports both `(P_u,P_v)` and `(J_c,J_d)`, and maps the
actual ordered-hole pair `(k_u,k_v)` to `(S(k_v),S(k_u))`.
Taking the even complement commutes with this action. Thus every
coloring yields a root in the complete finite family, and one
representative of each group orbit suffices for a future cover
test. No assertion of a free action is needed.

## Complete families and their orbits

The independent enumeration gives the following exact counts.
Each remaining set determines a unique five-component decomposition
within its marked form.

| b | Joint families and distinct remaining sets | Full group | Remaining-set orbits | Orbit sizes and multiplicities |
| --- | --- | --- | --- | --- |
| 3 | 1,708 | 8 | 224 | 21 of size 4; 203 of size 8 |
| 15 | 1,648 | 16 | 112 | 18 of size 8; 94 of size 16 |
| 63 | 304 | 16 | 21 | 4 of size 8; 17 of size 16 |

These are now complete remaining-set orbits, obtained after joint
disjointness of all five components. Each stabilizer has order one
or two; the actions remain nonfree. The 357 representatives exhaust
the three forms, without identifying their different charges.

Joint disjointness also restricts the actual ordered-hole pairs to
seven of the twelve locally possible pairs. In the fixed roles the
surviving pairs are `(48,51)`, `(48,63)`, `(60,48)`, `(60,51)`,
`(60,63)`, `(63,48)`, `(63,51)`. Their family counts are:

| Actual holes `(k_u,k_v)` | b=3 | b=15 | b=63 |
| --- | --- | --- | --- |
| (48,51) | 96 | 56 | 16 |
| (48,63) | 176 | 240 | 24 |
| (60,48) | 80 | 56 | 16 |
| (60,51) | 288 | 96 | 64 |
| (60,63) | 432 | 480 | 80 |
| (63,48) | 160 | 240 | 24 |
| (63,51) | 476 | 480 | 80 |

The paired exchange preserves this list by transporting both
roles and points. In particular it exchanges `(48,51)` with
`(60,48)`, and `(60,63)` with `(63,51)`. A different arbitrary
choice of ordered-hole allocation cannot replace these roots.

## Independent finite reconstruction

The bitmask builder enumerates the complete Cartesian product
and tests disjointness. The independent auditor reconstructs
all cliques using arrays and joins components in a different
order. It checks every original-graph component, actual hole,
35-point complement and reversed source-heptad completion.
It constructs the full groups directly from their basis images,
checks dot preservation and closure, and transports all five
component roles and both actual holes for every root action.
There are 318,420 original-graph component pair checks, 7,320
reversed source-heptad controls, 655,360 full dot-product checks,
73,728 composition point checks and 44,896 complete root actions.

The [root artifact](../results/dimension-7-four-six-six-roots.json)
contains the five ordered component catalogs, every complete
joint choice, the full group basis images and all orbit members.
The [audit report](../results/dimension-7-four-six-six-roots-check.json)
binds the artifact, source and inherited geometric proof.
Missing roots, changed components, wrong actual holes and omitted
orbit members are rejected by explicit invalid controls.

## Scope and next step

These are complete necessary even covering roots, not complete
nineteen-colorings or a cover exclusion. The original `(4,5,5)`
row, the transferred `(4,6,6)` subbranch, other branches and exact
n=7 remain open with lower bound 19. The 25/37 raw candidate
lists are retained. The next bounded target is a five-anchored-
heptad cover test on the independently checked orbit representatives,
with a checked witness or an independently audited failed-state
certificate. A cover witness alone would still need the original
graph and odd-class extension checks. No cover search runs here.

Historical finite covering premises and their report identities
are retained without rerunning their audits. No new Lean or
independent Pro review is claimed. The original n=6 theorem
retains three standard plus four native-evaluation axioms.
The submitted snapshot is preserved; these results enter the
authorized extended working draft for coauthor review.

```sh
python3 develop/build_dimension_seven_four_six_six_roots.py --roots /tmp/n7-four-six-six-roots.json
python3 develop/check_dimension_seven_four_six_six_roots.py --roots /tmp/n7-four-six-six-roots.json --report /tmp/n7-four-six-six-roots-check.json
```
