# Three marked forms for the remaining eight-odd five-plus-six profile

**Theorem.** A nineteen-coloring of Gamma_7 with characteristic class
size four and profile (m5,m6;A,B,C)=(3,6;6,2,8), if one exists,
admits one of the three marked forms below. Its three-even sum is
nonzero and outside the hole Lagrangian. Its pure-six defect contains
exactly one hole point. The marked stabilizers have orders 32,32,16.

This is a necessary geometric reduction, not a covering exclusion.
The previously excluded (5,4;6,2,8) profile is separate: its four-form
covering certificates do not apply to this profile. The current totals
remain 26 five-plus-six and 39 three-six count candidates. Exact
dimension-seven chromatic numbers remain open with lower bound 19.

## Charge and hole constraints

By the [written eight-spread completion theorem](dimension-seven-nineteen-obstruction.md),
the eight pure odd heptads leave the seven nonzero points of a
Lagrangian M in E=z-perp. Let the five-point defect have even members
u,v,w and odd projections a,d. Let b,c be the mixed odd projections,
and let e,f,g be the characteristic projections. These seven points
partition M minus zero. Write

~~~text
r=u+v+w, q=sum of the six pure-even defect members,
s=b+c, h=e+f+g=a+d+b+c.
~~~

Each of u,v,w pairs to one with a and d, so r dot a=r dot d=1.
In particular r is nonzero and outside M. The even triple has Gram
matrix I+J of rank two, its sum r is its radical vector, and r is
nonzero; thus its three members are linearly independent.
The projected five-defect charge is r+a+d and the pure-six charge
is q. The [partition charge and quadratic formulas](dimension-seven-size-four.md)
give

~~~text
q+r=b+c, (r+a+d) dot q=0.
~~~

The second formula uses A+B=8 and defect quadratic terms
binom(5,2)+binom(2,2)=1 and binom(6,2)=1 modulo two.
Substituting q=r+b+c and isotropy of M gives r dot(b+c)=0.
Therefore the nonzero functional ell(x)=r dot x on M satisfies

~~~text
ell(a)=ell(d)=1, ell(b)=ell(c)=eta in {0,1}.
~~~

The six pure even heptads and the pure-even defect are the seven
available labels on the even clique M minus zero. Each meets M at
most once, so all seven meet it exactly once. Let t be the pure-six
defect's actual hole. The even six-class has invertible Gram matrix
I+J and spans E. Its sum q pairs to one with each member and is
its unique even heptad completion. Hence ell(t)=q dot t=1, since
q+r lies in M. All odd-containing classes avoid the even hole clique.

## Three exhaustive normalizations

If eta=1, the four points a,d,b,c exhaust ell=1, an affine plane.
Its sum is zero, giving a+d=b+c and h=0. If eta=0, b,c span
ker(ell). The nonzero point a+d belongs to this kernel. It is
either b+c, giving h=0, or one of b,c, giving h equal to the other
mixed projection. Thus exactly the following three role patterns
are necessary. Use z=127 and M={0,3,12,15,48,51,60,63}.

| Case | eta | Five-defect odd projections {a,d} | Mixed projections {b,c} | r | q | Characteristic projections | h | Possible t |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| I | 0 | {48,63} | {3,12} | 95 | 80 | {15,51,60} | 0 | {48,51,60,63} |
| II | 1 | {3,51} | {12,60} | 6 | 54 | {15,48,63} | 0 | {3,12,51,60} |
| III | 0 | {48,51} | {3,12} | 95 | 80 | {15,60,63} | 12 | {48,51,60,63} |

For I choose the basis (b,c,a) of M; then d=a+b+c. For III
exchange b,c if necessary so that a+d=b and use the same basis.
Send this basis to (3,12,48). For II choose (a,b,a+d), again a
basis, and send it to (3,12,48). Extend each basis to a symplectic
basis of E and fix z. These written isometries normalize the odd roles
and the functional ell, without assuming transitivity on colorings.

In the symplectic basis (3,12,48;65,71,95), a point is (x,y), with
y recording its pairings with M. Once the roles are normalized,
r has y=(0,0,1) in I/III or y=(1,1,0) in II. The pointwise-M
shears g_S(x,y)=(x+Sy,y), S symmetric, can set x=0: the linear
map S -> Sy is surjective for every nonzero y. To see this, change
basis to y=(1,0,0); the first column of a symmetric matrix can be
arbitrary. This completes the normalization r=95 or r=6, and
q=r+b+c is then fixed. No assumption that q belongs to M is made.

## Full marked stabilizers transport the actual hole

For a linear map A on M, its symplectic extension is
k_A(x,y)=(Ax,A^(-T)y). In each normalized case the allowed A
preserve the unordered five-defect pair {a,d} and the unordered
mixed pair {b,c}. In I and II there are four such A, obtained by
independently exchanging the members of those pairs. In III, h=c
distinguishes the mixed members, so only the exchange of a,d remains;
there are two such A. The four marked points span M and therefore
determine A uniquely; these lists are exhaustive.

All these A preserve ell, so their extensions fix normalized r,
whose x coordinate is zero. The pointwise-M shears fixing r satisfy
Sy=0. Surjectivity of S -> Sy makes this kernel dimension three,
hence it has eight elements. Every marked stabilizer element is
g_S k_A with Sy=0: after removing its restriction A to M, a
symplectic map fixing M pointwise has exactly the shear form.
This proves the full stabilizer orders 4*8=32,4*8=32,2*8=16.

The maps preserve the even-triple and pure-six catalogs and either
preserve or exchange the mixed catalogs. They preserve disjointness
and all anchored heptads. If a mixed pair is exchanged, reorder its
images to restore the two mixed roles. Consequently existence of a
cover for a necessary remaining set is invariant under the group.
The actual t is transported with its partial partition. Its two
orbits in I are {48,63} and {51,60}; in II they are {3,51} and
{12,60}; in III they are {48,51} and {60,63}. No exchange between
these two hole orbits is assumed.

## Local audits and scope

The exact catalogs have the following sizes. Defect pairs in this table
are disjoint even parts of the five-class and pure-six class; they do
not yet include both mixed sextets.

| Case | Five-class even triples | Pure-six defects | Mixed sextets for each role | Disjoint defect pairs | Full marked stabilizer |
| --- | ---: | ---: | --- | ---: | ---: |
| I | 4 | 24 | 32,32 | 96 | 32 |
| II | 4 | 24 | 32,32 | 96 | 32 |
| III | 4 | 24 | 32,32 | 72 | 16 |

Each of the four eligible pure-six holes occurs in six of its 24
blocks. The checker constructs all 5,376 even triples, 2,016 even
sextets and 288 even heptads; 224 heptads have exactly one M-hole.
The local constraints are applied to these complete catalogs.

The checker independently constructs the even triple, anchored
pure-six defect and both mixed sextet catalogs by array recursion
and bitmask recursion. It checks each original five-, six- and
seven-point color class by the coordinate dot product. It controls
every fixed-M assignment of odd roles and nonzero ell satisfying
the derived constraints, and all possible r in each ell fiber,
checking their explicit normalization isometries. It also constructs
every marked stabilizer and verifies its group and catalog actions.
There are 42,42,84 admissible fixed-M role/functional assignments
in I/II/III and eight possible r values for each: 1,344 explicit
normalization controls in total. Their source-basis Gram checks cover
8,232 entries; inverse images are checked in 123,648 original color
classes. The stabilizer audits check 1,310,720 coordinate dot-product
pairs and 294,912 composition points, including closure and identity.
All local catalog actions and disjoint-defect-pair actions agree.

The [checker](../develop/check_dimension_seven_three_six_charge.py)
and [report](../results/dimension-7-three-six-charge.json) record
the complete local scope and dependency hashes. The final bounded
audit takes about one second locally, using under 30 MB maximum RSS.

No complete necessary root family, covering search, failed-state
certificate or full coloring is produced here. The (5,4) covering
certificates are not inputs to this geometric reduction. Both
manuscript PDFs and all historical certificates are preserved.
No new Lean or independent Pro review is claimed. The original
six-dimensional formal theorem retains three standard and four
native-evaluation axioms. Publication and submission remain separate.

~~~sh
python3 develop/check_dimension_seven_three_six_charge.py --report /tmp/dimension-7-three-six-charge.json
~~~
