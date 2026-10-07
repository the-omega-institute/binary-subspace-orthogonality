# Three marked forms for the transferred two-hole branch

**Theorem.** The two-hole (4,6,6;5,2,8) branch obtained by the
[two-completion recoloring](dimension-seven-four-five-five-charge.md)
has three exhaustive marked symplectic forms. Their full marked
stabilizers have orders 8,16,16. Both actual pure-defect holes and
the pairing between each pure-six sum and its mixed class are
retained. This is a geometric reduction of that subbranch, not an
exclusion of it or of the entire raw profile.

The 25 five-plus-six and 37 three-six count candidates remain open.
No complete jointly compatible five-block root family or covering
proof is constructed here. The next finite problem has now been
specified, but no covering search is run.

## A basis gives three exhaustive forms

Use the markings inherited from the preceding written reduction.
The four-even/two-odd defect has even sum a and odd projections
a,b, with charge b. The two mixed heptads have odd projections
c,d and contain the even vectors u,v, respectively. The two pure
six-defects have sums u,v outside M and distinct actual holes.
Their even heptad completions are the vectors u,v already present
in the mixed classes. The characteristic projections are the other
three nonzero points of M. The preceding reduction proves

```text
u+v=a+c+d in M minus {0},
ell=u dot(-)|M=v dot(-)|M,
ell(a)=ell(c)=ell(d)=1,  u dot v=1.
```

The three points a,c,d are independent: a dependence between
distinct nonzero binary vectors would make a+c+d=0, contradicting
its ell-value one. Set

```text
e1=a+c,  e2=a+d,  e3=a.
```

Then e1,e2 span ker ell, (e1,e2,e3) is a basis of M and
u pairs with it as (0,0,1). The plane spanned by e3,u is
nondegenerate. Its perpendicular complement contains e1,e2 as a
Lagrangian; choose a symplectic dual pair f1,f2 in that complement.
Sending this symplectic basis to

```text
(e1,e2,e3,f1,f2,u) -> (3,12,48,65,71,95)
```

defines a symplectic isometry of E, extended to the original dot
space by fixing z=127. Consequently

```text
M minus {0}={3,12,15,48,51,60,63},
a=48, c=51, d=60, u=95, v=96, u+v=63.
```

The remaining distinct point b is one of e1,e2,e1+e2,e1+e2+e3.
Exchanging the paired roles (c,u) and (d,v) interchanges e1,e2
and permits the first two choices to share a representative.
There are exactly three forms:

| b | Characteristic projections | h | Intrinsic charge description |
| --- | --- | --- | --- |
| 3 | 12,15,63 | 60 | h is one of c,d |
| 15 | 3,12,63 | 48 | h=a |
| 63 | 3,12,15 | 0 | h=0 |

The normalization transports the actual holes as well as all
classes. It does not assume that full colorings, actual-hole pairs
or jointly compatible block choices form one orbit.

## The complete marked groups have orders 8,16,16

In symplectic coordinates (x,y) relative to this basis, every
isometry preserving M has form

```text
(x,y) -> (Lx+B L^(-transpose)y, L^(-transpose)y),
L in GL(3,2), B symmetric.
```

There are 168 possible L and 64 symmetric B. A marked isometry
must fix a and b and preserve the paired roles {(c,u),(d,v)}.
Its restriction to M is therefore either the identity or the
exchange S of e1,e2, fixing e3. No other restriction is possible:
a,c,d are a basis and the ordered or exchanged images determine it.

For the identity restriction, u must be fixed, so B e3=0. The
upper left symmetric two-by-two block is arbitrary, giving eight
lifts. For restriction S, c,d and u,v must both be exchanged.
Since the linear part fixes u, its image must acquire e1+e2+e3,
so B e3=e1+e2+e3. Again there are eight lifts. S preserves b
exactly when b=15 or b=63; it does not fix b=3.
Thus the full marked orders are 8,16,16. The proof gives all
lifts, rather than proposing a convenient subgroup as the full group.

All groups act on the possible holes {48,51,60,63}. The eight
identity-restriction lifts fix M pointwise. The exchanged lifts
swap 51,60 and fix 48,63 while exchanging the two pure-defect roles.
An ordered actual-hole pair (k1,k2) therefore maps under an
exchanged lift to (S(k2),S(k1)). Of the twelve distinct ordered
hole pairs, (51,60) and (60,51) are fixed; the other ten form
five pairs. The hole-pair orbit counts are consequently 12,7,7.
For b=15 or b=63 a fixed pair has marked group order 16, while the
stabilizer of each other ordered pair has order 8. All ordered
pairs have order 8 for b=3. These pair stabilizers are not assertions
about the stabilizers of complete block choices.

## Complete local catalogs retain the hole information

Every form has sixteen four-even blocks with sum 48 and pairings
one with 48 and b. The two mixed even sextets have sums 51 and 60,
contain 95 and 96 respectively, and have six choices each. Both
original mixed classes and the four-even defect are checked against
the original dot-product definition.

The pure sextet with sum 95 must have one actual hole and avoid 96;
the sextet with sum 96 must have one actual hole and avoid 95,
because both completion vectors already occur in mixed classes.
Each has eighteen choices: four with each hole 48,51,60 and six
with hole 63. There are 216 ordered disjoint pure-defect pairs.
The ordered hole pairs among 48,51,60 have twelve choices each;
the six ordered pairs involving 63 have twenty-four choices each.
All twelve ordered hole pairs occur locally. These pure-pair
choices have not been required to avoid the other three even blocks.

The full groups give 72,38,38 orbits of these local pure-defect
pairs. For b=3 there are 36 orbits of size two and 36 of size four.
For b=15 or b=63 there are four of size two, sixteen of size four
and eighteen of size eight. Thus the actions are not free; dividing
216 by the group order would give incorrect orbit counts.

The seven even holes are covered by the two pure defects and
five pure even heptads. Each class can meet M at most once, so
the five heptads must all be anchored at the other five holes.
A later covering problem may therefore use the 224 anchored
heptads, retaining the two actual defect holes. This written
capacity step justifies that catalog for this branch; it does not
assert that the resulting covering problem has no solution.

## Audit and scope

The [local auditor](../develop/check_dimension_seven_four_six_six_two_hole.py)
compares independent array and bitmask clique catalogs, constructs
all parabolic isometries and independently reconstructs all 5,376
fixed-M ordered markings. Three forms, allowing the paired role
exchange in the b=3 form, cover every marking with eight explicit
image controls. The Gram matrices are checked on a
basis for every map. Full pointwise dot preservation, closure,
component-catalog actions, pure-pair actions and transport of
actual holes are checked for each marked stabilizer.

The [report](../results/dimension-7-four-six-six-two-hole.json)
records all three forms, component catalogs, pure-pair orbit
statistics and actual-hole-pair orbits. These are local geometry
orbits, not complete remaining-set orbits. The inherited recoloring
report, source and seven historical theorem bindings are checked
without rerunning their audits or any spread enumeration.

The next bounded step is to construct complete necessary even
remaining sets from jointly disjoint choices of all five components:
the four-even defect, two pure sextets and two mixed even sextets.
The complement has 35 even points and exactly five holes. Retain
the paired pure/mixed roles and actual holes under the full legal
groups; do not assume free actions or merge the three charge forms.
Only after that family is complete is a covering proof meaningful.

No covering search, certificate, new numerical bound, Lean or
independent Pro review is claimed. The original (4,5,5) row,
this transferred subbranch, the other (4,6,6) branches and exact n7
remain open with lower bound 19. The original n6 theorem retains
three standard plus four native-evaluation axioms. The submitted
snapshot is preserved; the authorized extended working draft is
updated for coauthor review.

```sh
python3 develop/check_dimension_seven_four_six_six_two_hole.py --report /tmp/dimension-7-four-six-six-two-hole.json
```
