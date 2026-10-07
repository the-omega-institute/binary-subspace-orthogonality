# Two forced completions reduce (4,5,5;7,0,8) to a two-hole branch

**Theorem.** Every hypothetical nineteen-coloring of Gamma_7 with
characteristic size four and profile (4,5,5;7,0,8) can be recolored
to profile (4,6,6;5,2,8). In the resulting coloring both pure even
six-defects have nonzero sums outside the hole Lagrangian M and
contain one actual hole each; these holes are distinct. Their
sum-completion vectors belong to the two saturated mixed classes.

The source profile is not excluded: the resulting two-hole branch
is still open. The complete count lists remain 25 five-plus-six
and 37 three-six candidates. This is a written reduction using
three earlier exact-profile exclusions and their historical finite
covering premises, with new finite local controls. There is no
new covering search, finite cover certificate or Lean result.

## The even charge uniquely completes a (5,1) six-class

Put E=z-perp. The [written eight-spread completion theorem](dimension-seven-nineteen-obstruction.md)
leaves M minus {0} as the seven remaining odd projections.
Write D0 for the four-even/two-odd six-defect and D1,D2 for the
two five-even/one-odd six-defects. Name D0's odd projections a,b,
with charge b. Its even sum is a by the
[charge-member lemma](dimension-seven-two-six-profiles.md).
Name the odd projections of D1,D2 as c,d and their even sums r,s.
All four odd projections a,b,c,d are distinct nonzero points of M.

For any five-even/one-odd six-class with odd member z+c and
even sum r, every even member p satisfies p dot r=0 and
p dot c=1. Also r dot c=1. Thus

```text
t=r+c is even, outside M, absent from the class,
p dot t=1 for every even member p,
(z+c) dot t=1.
```

Appending t produces a mixed (6,1) heptad. This completion is
unique. The completed six even vectors have nonsingular Gram
matrix I+J, form a basis of E and sum to c. Any other possible
even completion would also make the even sum c, so it would
equal r+c. The odd projections are in M, but the even completion
is outside M; confusing those two locations would invalidate the
transfer.

## Partition identities fix the common functional

The characteristic projections are the three unused points of M,
so h=a+b+c+d. The projected charges are b,r+c,s+d, and the
partition-charge identity gives

```text
b+(r+c)+(s+d)=a+b+c+d, hence r+s=a.
```

Consequently r and s restrict to the same nonzero functional
ell on M. Since r dot c=s dot d=1, ell(c)=ell(d)=1.
The quadratic charge identity has right side one: A+B=7,
D0 has tau=0 and D1,D2 each have tau=1. Its left side is

```text
b dot((r+c)+(s+d)) + (r+c) dot(s+d)
 = r dot a + ell(c)+ell(d) = ell(a).
```

Therefore ell(a)=1 as well. Put

```text
t1=r+c, t2=s+d, v=t1+t2=a+c+d in M minus {0}.
t1|M=t2|M=ell,  t1 dot t2=ell(v)=1.
```

The last identities include v nonzero: ell(a+c+d)=1.
They do not assume ell(b)=1 or h=0. If v=b, h=0;
otherwise v is one of the characteristic projections.

All three original defects have odd members projected into M,
so they contain no even hole. All seven even holes therefore
belong to the seven pure even heptads, each exactly once.

## Earlier exclusions force distinct source heptads

For i=1,2, move ti into Di. Each ti is an existing even vertex
outside M. It is absent from its own defect and cannot belong
to the characteristic or pure odd classes. Its possible sources
are the other defects or a pure even heptad.

1. If ti comes from D0, D0 becomes a size-five defect with
   three even/two odd members. The other five-even/one-odd
   six-defect remains, and the saturated counts become (7,1,8).
   This is precisely the five-plus-six profile (3,5;7,1,8),
   excluded by the [three-plus-five theorem](dimension-seven-three-five-cover.md).
2. If ti comes from the other five-even/one-odd defect, the
   source becomes size five with four even/one odd members.
   D0 remains a (4,2) six-defect and the counts again become
   (7,1,8). This is precisely (4,4;7,1,8), excluded by the
   [four-even-pair theorem](dimension-seven-four-even-pairs.md).

Thus both t1,t2 lie in pure even heptads. They cannot lie in the
same heptad: moving both into D1,D2 would leave a pure even
five-defect, preserve D0 and give counts (6,2,8), precisely the
profile (5,4;6,2,8) excluded by the
[complete D/H/G/Z theorem](dimension-seven-five-four-Z-cover.md).
This step invokes all four marked-form exclusions, not just Z's
certificate.

Let H1,H2 be their distinct source heptads. Move both t1,t2
simultaneously into D1,D2. The sources become pure even sextets
P1=H1 minus {t1}, P2=H2 minus {t2}; D1,D2 become mixed heptads;
D0 remains a (4,2) six-defect. Removing and adding these existing
vertices preserves the exact partition and all class independence.
No class becomes empty and the characteristic class stays size four.
The new profile is (4,6,6;5,2,8).

Every even heptad has vector sum zero, so sum Pi=ti is outside M.
Since ti is not a hole, Pi retains the unique actual hole ki of Hi.
The holes k1,k2 are distinct, and ell(k1)=ell(k2)=1 because
ki dot ti=1. Each ti is now an even member of its corresponding
mixed heptad with odd projection c or d; the other five even
members sum to ti+c or ti+d. The two pure-six roles and their
actual holes must be retained in any subsequent normalization.

## Evidence and remaining scope

The [local auditor](../develop/check_dimension_seven_four_five_five_charge.py)
compares independent array and bitmask clique catalogs. It checks
the unique completion of every fixed-M (5,1) class, all qualifying
odd-role/radical markings and compatible disjoint defect triples.
It separately checks every same-source anchored heptad and every
pair of disjoint distinct source heptads for the admissible charge
pairs. These are modular local controls, not complete nineteen-colorings
or a complete covering-root family.

There are 1,344 unique mixed-heptad completion controls, 5,376
odd-role/radical markings (1,344 with h=0) and 1,214,976 compatible
disjoint defect triples. The two possible transfers in each triple
give 150,528 D0-source controls, 580,608 other-(5,1)-defect-source
controls and 1,698,816 sources outside all defects. These counts
include partial configurations that cannot extend to a coloring;
the written theorem uses the earlier exclusions to rule out the
first two locations in a full coloring. The 224 distinct ordered
completion pairs give 1,344 same-source anchored-heptad controls
and 48,384 disjoint distinct-source heptad-pair controls. These
last controls are separate from the defect triples and are not
claimed to form complete jointly compatible roots.

The [report](../results/dimension-7-four-five-five-charge.json) records
the controls and current complete count lists. The auditor verifies
the source, certificate and recorded dependency hash bindings of
the three-plus-five and four-even-pair theorems, the size-three
two-six theorem inherited by the latter, and all D/H/G/Z exclusions.
It does not rerun historical covering audits or partial-spread
enumerations. These finite premises exclude the specified source
locations; they do not prove that the final two-hole branch is
impossible.

The next bounded target is the resulting marked two-hole branch
of (4,6,6;5,2,8), including t1+t2=a+c+d, ell(a)=ell(c)=ell(d)=1
and distinct actual holes. Establish exhaustive geometry and legal
symmetries before constructing a covering problem. The original
(4,5,5) row, the resulting (4,6,6) row, characteristic sizes four
through eight and exact n7 remain open, with lower bound nineteen.
The original n6 formal theorem retains three standard and four
native-evaluation axioms. The submitted snapshot is preserved.

```sh
python3 develop/check_dimension_seven_four_five_five_charge.py --report /tmp/dimension-7-four-five-five-charge.json
```
