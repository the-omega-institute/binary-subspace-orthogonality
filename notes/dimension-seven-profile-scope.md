# Uniform bookkeeping and the scope of the nineteen-color case analysis

The completed theorem chi(Gamma_7)>=19, hence chi(O_7*)>=19,
is independent of the subsequent nineteen-color profile analysis.
The current 27 five-plus-six and 39 three-six count candidates
all concern characteristic class size four. They are necessary
count profiles, not 66 complete geometric cases or coloring witnesses.
The D and H exclusions for (5,4;6,2,8) leave its Z and G forms
open and do not change these counts. Characteristic sizes five
through eight also remain open. No completion estimate follows
from the number of remaining profiles or two local cover searches.

## A common formulation for every characteristic size

Let a hypothetical nineteen-coloring have characteristic class C_z
of size s, containing z. Every other class avoids z and has size
at most seven. There are eighteen such classes, with 127-s vertices,
so their total deficit from capacity is

```text
sum_i (7-k_i)=s-1.
```

Here k_i are the sizes of its r undersized outside classes; let
m_i and o_i=k_i-m_i be their even and odd counts, and m=sum_i m_i.
Let A,B,C count saturated pure even, mixed (6,1), and pure odd
heptads. The characteristic class contains only odd vertices.
Since sum_i k_i=7r-(s-1), the parity counts give

```text
7A+6B+m=63,
B+7C+sum_i o_i+s=64,
A+B+C=18-r.
```

Consequently the same formulas apply for every s:

```text
B=m+7t,       A=9-m-6t,       C=9-r-t,
```

for an integer t with nonnegative counts. The size s enters through
the deficit condition and allowable defect types, not through new
A,B,C formulas. At s=4, deficit three has exactly the patterns
4, 5+6 and 6+6+6. At s=5,...,8, deficits four through seven
require additional patterns. This common formulation organizes
the search but does not establish disjointness or realizability.

The charge identity also has the same form for all s. Write pi(v)
for the projection to E=z-perp, h=sum_{v in C_z}pi(v), and
w_i=sum_{v in D_i}pi(v). Saturated classes have projected sum zero,
so sum_i w_i=h. The characteristic projections are pairwise
orthogonal, even when h=0. For a quadratic refinement q of E,
polarization gives

```text
sum_{i<j} w_i dot w_j
    = A+B+sum_i [binom(k_i,2)+binom(o_i,2)] modulo two.
```

Indeed the full projected quadratic sum is zero, the characteristic
class contributes q(h), and a defect contributes q(w_i) plus the
displayed binomial terms. Each pure even or mixed heptad contributes
one, and each pure odd heptad contributes zero. Polarizing sum_i w_i=h
then gives the formula. These are the common charge constraints
behind the existing individual reductions; they do not force every
defect charge into a hole Lagrangian.

## Uniform hole capacities and their present limit

If C=8, the existing written eight-spread completion theorem leaves
one hole Lagrangian M. Every remaining odd projection lies in M.
The seven even hole points require seven different labels. Mixed
classes and defects with any odd member are forbidden there, while
each pure even class meets M at most once. Thus, for every s,

```text
7 <= A + number of pure even defects.
```

If C=7, the existing finitely proved seven-spread completion lemma
leaves two transverse hole Lagrangians M,N. Pure even heptads
contribute at most two of their fourteen even points; mixed classes
at most one. A pure odd defect contributes zero, a pure even defect
at most two, and a defect with both parities at most one: an odd
projection forbids one whole side, and pairwise-one even members
meet the other isotropic side at most once. Therefore

```text
14 <= 2A+B+sum_i b(k_i,m_i),
b(k,m)=0 if m=0, 2 if m=k, and 1 otherwise.
```

The existing finite six-spread completion lemma gives three disjoint
hole Lagrangians when C=6. The same reasoning gives
21<=3A+2B+sum_i b_3(k_i,m_i), with b_3 equal to zero for a pure
odd defect, three for a pure even defect, and two otherwise.
All three inequalities have one common form, writing d=9-C:

```text
7d <= dA+(d-1)B+sum_i b_d(k_i,m_i),
b_d(k,m)=0 if m=0, d if m=k, and d-1 otherwise.
```

For C=6,7 the finite completion dependencies remain essential;
C=8 uses the written completion theorem. This bound is not asserted
for C=5, where twenty-eight holes remain. The charge-member lemma
likewise applies to its stated six-point class types, not every small defect.

The [small accounting auditor](../develop/check_dimension_seven_profile_scope.py)
independently reconstructs the 9/46/48 original size-four count rows,
checks the common formulas and charge-parity metadata, and applies
this common capacity inequality to the currently unexcluded rows.
The [report](../results/dimension-7-profile-scope.json) records:

| Pure odd heptads C | Five-plus-six candidates | Three-six candidates |
| --- | --- | --- |
| 5 | 0 | 2 |
| 6 | 6 | 14 |
| 7 | 19 | 18 |
| 8 | 2 | 5 |
| Total | 27 | 39 |

All 64 applicable C=6/7/8 candidates already satisfy their respective
capacity inequality. The other two have C=5. Reapplying these
uniform necessary tests gives no new raw-profile exclusion.
This does not prove that no stronger uniform argument exists;
none that closes the remaining family is established here.

Closing these 66 count candidates would still leave the separate
characteristic-size-five-through-eight branches. Excluding every
nineteen-color line coloring would prove chi(Gamma_7)>=20, hence
chi(O_7*)>=20; it would supply no matching upper bound. A nineteen-color
line witness, if found, would require an additional extension check
before it could prove a nineteen-color upper bound for the full graph.

The evidence therefore supports slower convergence than treating
each of the 66 rows as one bounded check, with no justified forecast
of total time or branch count. Any research stopping point or
submission scope is a separate joint decision. This note sets none.
No cover search, spread enumeration, SAT, DRAT, Lean or independent
Pro review is run. The original six-dimensional formal theorem
retains three standard and four native-evaluation axioms; the
submitted manuscript and Zenodo PDF are preserved.

```sh
python3 develop/check_dimension_seven_profile_scope.py --report /tmp/dimension-7-profile-scope.json
```
