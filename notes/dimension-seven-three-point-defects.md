# Quadratic parity restricts three-point characteristic classes

**Theorem.** Suppose Gamma_7 has a nineteen-coloring whose
characteristic class C_z has size three. If its outside deficit is
concentrated in one five-point class D, only the following three
count profiles are possible:

| D (even,odd) | A pure even heptads | B mixed (6,1) | C pure odd heptads |
| --- | --- | --- | --- |
| (0,5) | 3 | 7 | 7 |
| (1,4) | 2 | 8 | 7 |
| (2,3) | 7 | 2 | 8 |

These are necessary profiles, not constructed colorings. The alternative
outside deficit of two six-point classes remains open, subject to a
new charge-pairing identity below. The exact line and full-subspace
chromatic numbers remain open with lower bound nineteen. There is no
nineteen-color witness or new numerical lower bound.

The [preceding projection argument](dimension-seven-characteristic-three.md)
proved 3<=|C_z|<=8 and showed that every saturated seven-point
class avoiding z has zero projected sum. The present argument adds
quadratic parity to that vector constraint.

## The quadratic identity for a color class

Write E=z-perp, p(v)=v dot z and pi(v)=v+p(v)z. For a class D,
write k=|D|, o for its odd count, and w_D=sum pi(v). Let q be any
quadratic refinement of the alternating form on E, for example
q(x,y)=x dot y in symplectic coordinates. Direct expansion gives

```text
pi(v) dot pi(u) = v dot u + p(v)p(u).
```

Distinct members of an independent class have dot product one.
Polarizing q over the class therefore gives the identity in F_2

```text
sum_{v in D} q(pi(v)) = q(w_D) + binom(k,2) + binom(o,2).
```

For a saturated seven-point class, w_D=0. Its quadratic sum is one
for a pure even heptad or mixed (6,1) class, and zero for a pure
odd heptad. Over all 127 line generators the quadratic sum is zero,
because every nonzero point of E occurs twice under pi.

This is a parity identity for an actual common partition. It does
not permit assembling independently chosen classes as though they
were disjoint or simultaneously realizable.

## One five-point defect: ten profiles reduce to three

Write C_z={z,z+e,z+f}. Its three lines are independent, so the
distinct nonzero e,f satisfy e dot f=0. Put h=e+f. Then h is
nonzero and the quadratic sum of C_z is q(h).

If D is the unique five-point class, the other seventeen classes
are saturated. The global projection sum forces w_D=h. The
quadratic sums of C_z and D cancel their q(h) terms, leaving

```text
A+B = binom(o,2) mod 2.
```

If D has m even lines and o=5-m odd lines, capacities allow
m=0,1,2,3,4,5. Counting all even and odd lines gives

```text
7A+6B+m=63,       B+7C+5-m+3=64,       A+B+C=17.
```

Equivalently B=m+7t, A=9-m-6t, C=8-t. Nonnegativity leaves ten
profiles. The quadratic identity excludes six:

| D (even,odd) | (A,B,C) | A+B mod 2 | binom(o,2) mod 2 |
| --- | --- | --- | --- |
| (0,5) | (9,0,8) | 1 | 0 |
| (1,4) | (8,1,8) | 1 | 0 |
| (2,3) | (1,9,7) | 0 | 1 |
| (3,2) | (0,10,7) | 0 | 1 |
| (4,1) | (5,4,8) | 1 | 0 |
| (5,0) | (4,5,8) | 1 | 0 |

The remaining profile (D=(3,2); A,B,C=6,3,8) is also impossible.
Its eight pure odd classes provide eight disjoint Lagrangians.
The universal completion theorem makes their seven holes exactly
M minus {0}. Both e,f and the two odd projections g_1,g_2 in D
belong to M. If its even vectors are u_1,u_2,u_3, then

```text
u_1+u_2+u_3 = h+g_1+g_2 in M.
```

But each u_i pairs to one with g_1, since its line shares D with
z+g_1. Their sum pairs to three, or one in F_2, with g_1. Two
points of M pair to zero, a contradiction. The three rows in the
theorem are the only remaining necessary profiles.

## Two six-point defects: a prescribed pairing of their charges

If the outside deficit consists of two six-point classes D_1,D_2,
the remaining sixteen classes are saturated. Let their projected
charges be w_1,w_2, odd counts o_1,o_2, and put

```text
tau_i = 1 + binom(o_i,2) mod 2.
```

The vector identity gives w_1+w_2=h. Summing quadratic values over
C_z,D_1,D_2 and the saturated classes then gives

```text
w_1 dot w_2 = A+B+tau_1+tau_2 mod 2.
```

For the six-point even counts m=0,2,4,5,6, the corresponding tau
values are respectively 0,1,0,1,1. This condition must be checked
on two classes in the same coloring. No coupled pair enumeration,
realizable partition or exclusion of this entire branch is claimed.

## Verification and scope

The [coordinate checker](../develop/check_dimension_seven_three_point_defects.py)
checks the projection pairing identity on all 16,384 ordered binary
vector pairs and quadratic polarization on all 4,096 pairs in E.
It directly enumerates all 179,739 independent five-point classes
and 60,417 independent six-point classes avoiding z, verifying the
class quadratic identity for each. It checks all ten count profiles
and records the six parity exclusions, one completion exclusion and
three necessary survivors. Its normalized local controls use
e=3,f=12; they are individual classes, not colorings.

An independent enumeration by even parts and isotropic odd
projections agrees with the entire five-point class set. The
six-point set agrees with the preceding independently checked
certificate. The [report](../results/dimension-7-three-point-defects.json)
binds the note, checker and prior certificate. No SAT solve,
checked UNSAT proof or Lean run is involved. The submitted
manuscript at 28e27a8 is unchanged; the original dimension-six
Lean theorem retains three standard and four native-evaluation axioms.

```sh
python3 develop/check_dimension_seven_three_point_defects.py --report /tmp/dimension-7-three-point-defects.json
```
