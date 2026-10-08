# Distinct pure completion sources and kernel holes in the remaining row

**Theorem.** Every hypothetical nineteen-color line coloring with
characteristic size four and profile `(4,6,6;5,2,8)` has both pure-six
completion vectors in distinct pure even heptads. Each source avoids
the other completion. The two pure defects and their two sources
occupy precisely the four M-holes with functional value one. The
remaining three holes are the nonzero kernel plane. The row remains
open; the count lists stay **25/35**.

## Charge and all four functional patterns

Let D0 be the four-even/two-odd six-defect. Name its odd projections
a,b so that its even sum is a and its charge is b, as in the
[charge-member lemma](dimension-seven-two-six-profiles.md).
The two mixed heptads have odd projections and even sums c,d.
Let P1,P2 be the pure even sextets, with sums and unique even
completion vectors u,v. Their Gram matrices I+J are nonsingular,
so each sextet is a basis of E and its sum pairs to one with all
six members. Neither completion lies in its recipient sextet.

The eight pure odd heptads leave M by the written eight-spread
theorem. The characteristic projections are M minus {0,a,b,c,d},
and their sum is h=a+b+c+d. The partition and quadratic identities
give b+u+v=h and u dot v=1: A+B=7, and the three defect tau
terms are 0,1,1. Hence

```text
u+v=a+c+d in M minus {0},
ell=u dot(-)|M=v dot(-)|M,
ell(a)+ell(c)+ell(d)=1.
```

If either completion belonged to M, both would, contradicting
u dot v=1. Thus ell is nonzero and a,c,d form a basis. The full
ordered functional patterns are **100,010,001,111**. The earlier
paired mixed/mixed branch imposed 111 through its source locations;
that restriction must not be imported into the entire raw row.

## Every other source gives an excluded exact profile

An even completion cannot come from the characteristic or a pure
odd class. Its own recipient is also impossible. The full partition
therefore leaves the following alternatives for u; the same proof
applies to v.

| Source of u | Exact profile after u moves into P1 | Exclusion |
|---|---|---|
| D0 | `(3,6;6,2,8)` | [Three-even/pure-six theorem](dimension-seven-three-six-cover.md) |
| P2 | `(5,4;6,2,8)` | [All four D/H/G/Z forms](dimension-seven-five-four-Z-cover.md) |
| Either mixed heptad | `(4,5,6;6,1,8)` | [Complete twelve-branch theorem](dimension-seven-four-five-six-cover.md) |

Each move removes and adds the same vertex; subsets remain independent,
and the receiving sextet plus its unique completion is independent.
Thus every listed transfer is a proper coloring of the exact profile
shown. The three exclusions force u and v into pure even source
heptads H1,H2. If they shared one source, move both into their
recipients simultaneously. Since u dot v=1, the vectors differ;
the common source becomes a pure five-defect and both recipients
become pure heptads. The resulting profile is again `(5,4;6,2,8)`,
excluded using all four marked forms. Hence H1 and H2 differ,
and each avoids the other completion.

## Four positive holes leave exactly the kernel plane

Any class with an odd projection in M avoids M in its even part.
Only the five pure heptads and the two pure sextets can cover the
seven nonzero M-holes, each at most once. All seven classes therefore
have exactly one actual hole.

For a hole k in P1, k dot u=1 because u is the sum of its six
members, including k; the other five pair to one with k. The same
holds for P2 with v. A hole in H1 pairs to one with u in H1,
and a hole in H2 pairs to one with v. All four holes thus have
ell-value one. They are distinct by the partition and exhaust
the four positive points of the nonzero functional ell. The other
three holes are exactly ker ell minus {0}, a two-dimensional plane.

Single or simultaneous swaps P_i -> P_i plus its completion and
H_i -> H_i minus its completion are reversible proper recolorings.
The removed source sextet has the same sum u or v and retains its
actual hole; the completed target heptad retains the target hole.
The raw profile and the four-hole set stay unchanged. These moves
are not assumed to be geometric isometries exchanging the original
marked classes.

A complete necessary joint root selects D0, the two mixed even
sextets, P1,P2,H1,H2, with even sizes 4,6,6,6,6,7,7. Its complement
has **21 points and three kernel holes**. Its even sum is zero:
a+c+d+u+v=0. The three residual pure heptads must each meet one
kernel hole. The eligible catalog is therefore the **96 anchored
even heptads whose actual hole is in ker ell**, restricted by
containment in the remainder. This is a necessary three-heptad
covering problem, not an assertion that such roots exist or fail.

## Independent modular checks and scope

The [local auditor](../develop/check_dimension_seven_four_six_six_pure_sources.py)
compares independent array and bitmask catalogs of even cliques
of sizes four, six and seven against the original dot-product graph.
It checks unique pure completions, all ordered charge markings,
the exact transfer arithmetic and local source-removal/completion
controls with actual holes. Target/source pairs are modular controls;
they have not been assembled with the other roles into complete roots.

The 21,504 ordered fixed-M markings split into 5,376 for each of
100,010,001,111 and give 224 ordered completion pairs. All 2,016
pure sextets have their unique completion checked. Modular source
controls cover 2,688 removals from D0, 1,344 from each mixed role
and 1,344 from the other pure sextet. There are 1,344 common-source
two-removal controls and 4,032 each pure-source removals and pure-target
completions retaining actual holes. Every completion pair has 24
one-hole targets and 24 anchored sources, 18 each avoiding the other
completion, and 216 disjoint pairs of each kind (48,384 overall).
All 5,376 ordered allocations of four distinct positive holes leave
exactly the kernel plane. Each of the seven kernel planes occurs for
32 completion pairs, and each has the complete 96-row eligible catalog.

The [report](../results/dimension-7-four-six-six-pure-sources.json)
retains ten inherited theorem report/source/certificate/dependency
bindings, including the new entire four-five-six exclusion. The
written source theorem depends on those finite premises; these local
checks do not replace them. Historical covering and earlier source/root
audits are not rerun. No new raw row is excluded, and no complete joint
root construction, cover search, Lean or independent Pro review is run.
Exact n=7 remains open with lower bound 19. The original n=6 theorem
retains three standard plus four native-evaluation axioms. The submitted
snapshot and earlier evidence are preserved.

Next prove exhaustive marked normal forms and their full symmetry
groups, retaining all four functional patterns, two pure/mixed roles
and all four actual positive holes, before constructing complete joint
roots. Separate reversible recoloring from geometric role symmetry.

```sh
python3 develop/check_dimension_seven_four_six_six_pure_sources.py --report /tmp/dimension-7-four-six-six-pure-sources.json
```
