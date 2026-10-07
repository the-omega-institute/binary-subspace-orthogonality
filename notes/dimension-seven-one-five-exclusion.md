# A three-point characteristic class requires two six-point defects

**Theorem.** In a nineteen-coloring of Gamma_7 with a three-point
characteristic class, the outside size deficit cannot be concentrated
in a single five-point class. It must consist of two six-point classes.

The [quadratic profile analysis](dimension-seven-three-point-defects.md),
[completed-hole exclusion](dimension-seven-hole-cover.md), and
[seven-Lagrangian analysis](dimension-seven-seven-holes.md) left only
the profile (D even,odd; A,B,C)=(1,4;2,8,7) in the one-five branch.
The argument below excludes that final profile by a seven-clique
color budget. It uses the previously finitely proved seven-Lagrangian
completion lemma; that dependency remains part of the theorem.

The two-six branch is still open, as are larger characteristic classes,
the exact line and full-subspace chromatic numbers, and nineteen-color
witnesses. The numerical lower bound stays nineteen. This does not
exclude every coloring with a three-point characteristic class.

## The final profile has too few labels on a hole Lagrangian

Write C_z={z,z+e,z+f}, E=z-perp, and D={u,z+g_1,...,z+g_4}.
There are two pure even heptads, eight mixed (6,1) classes and
seven pure odd heptads. The latter give seven disjoint Lagrangians.
By the preceding completion lemma, their fourteen odd-projection
holes are M minus {0} and N minus {0}, with E=M direct-sum N.

All four g_i lie in one hole Lagrangian, say M. Indeed, if they
met both sides, the dimensions a,b of the two orthogonal spans
satisfy a+b<=3. Four distinct points then require a distribution
of three points spanning a two-space on one side and one on the
other. The three points of that two-space sum to zero. Each must
pair to one with u, which would make their sum pair to one rather
than zero, a contradiction.

At most three mixed classes have their odd projection in M,
because four of its seven nonzero points are occupied by D.
The characteristic projections e,f may remove additional points.

Now take the seven even points of N. They form a clique, hence
require seven distinct labels. The characteristic label is forbidden
by z. Every pure odd label is forbidden: a linear functional on
its three-dimensional Lagrangian has at most four value-one points,
so no even vector can pair to one with all seven odd members.
Every mixed label whose odd projection lies in N is forbidden
on all seven points, since N is totally isotropic.

Only two pure even labels, at most three mixed labels from M,
and the single defect label remain. Thus the entire clique has
at most 2+3+1=6 labels, contradicting its size seven. This upper
bound allows the defect label even when it is actually unavailable,
so it needs no search for the six-point parts of mixed classes.

## Exact coordinate controls for the two preceding local forms

The preceding note normalized M,N to the spans of (3,12,48) and
(65,71,95). Its two necessary local forms give stronger concrete
color budgets:

| Characteristic projections (e,f) | Even defect u | Mixed odd projections in M | Labels available on N |
| --- | --- | --- | --- |
| (65,71) | 6 | {15,48,63} | two pure even, three mixed, defect: six total |
| (3,71) | 68 | {48,51} | two pure even, two mixed: four total |

In the first case the defect label is available only at the even
point u=6 of N. In the second case it is unavailable throughout N.
The [checker](../develop/check_dimension_seven_one_five_exclusion.py)
verifies the original dot-product adjacency and necessary label
lists on this seven-clique, allowing both pure even labels everywhere
and ignoring further mixed-even constraints. These are supersets
of actual available labels. Their union already has fewer than
seven elements. A separate finite matching calculation reaches
maximum sizes six and four respectively.

For the fixed hole pair, the checker also reconstructs all 42 local
characteristic/defect configurations. Twenty-one have a six-label
union and twenty-one have a four-label union. These are local
coordinate controls; the uniform 2+3+1 argument above is the
written exclusion. No complete coloring is enumerated.

## The remaining three-point branch

The other eighteen classes have total size deficit two. Since
every class avoiding z has size at most seven, the only choices
were one five-point class or two six-point classes. The first is
now entirely excluded. Therefore a nineteen-coloring with |C_z|=3
must have exactly two six-point classes D_1,D_2 and sixteen
saturated seven-point classes. Their projected charges still obey

```text
w_1+w_2=e+f,
w_1 dot w_2=A+B+tau_1+tau_2,
tau_i=1+binom(o_i,2) modulo 2.
```

The feasibility of these coupled defects remains a separate problem.
No exclusion of that branch, new numerical bound or upper witness
is asserted.

## Verification and scope

The [report](../results/dimension-7-one-five-exclusion.json) binds
this note, the checker and the prior profile/completion reports.
The previous seven-spread enumeration is reused at its verified
revision, rather than rerun here. The new computation only checks
the necessary local color budgets and small matching problems.
No SAT, exact-cover search, DRAT, Lean or independent Pro review
is involved. The submitted manuscript at 28e27a8 is unchanged;
the original dimension-six Lean theorem retains three standard
and four native-evaluation axioms.

```sh
python3 develop/check_dimension_seven_one_five_exclusion.py --report /tmp/dimension-7-one-five-exclusion.json
```
