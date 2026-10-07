# Complete necessary roots for the three-even/pure-six profile

**Proposition.** In each of the three marked forms of the
[(3,6;6,2,8) charge reduction](dimension-seven-three-six-charge.md),
every putative nineteen-coloring with characteristic class size four
determines one of the necessary roots constructed below. The full
marked stabilizer acts on these roots, transporting their actual
pure-six hole and preserving existence of an anchored six-heptad cover.

This step constructs and reduces the complete necessary family. It
does not solve any cover, exclude a form or construct a full coloring.
The current count totals remain 26 five-plus-six and 39 three-six;
exact dimension-seven chromatic numbers remain open with lower bound 19.

## Necessary remaining sets

Use z=127, E=z-perp and M={0,3,12,15,48,51,60,63}.
In a fixed marked form, let T be the three even members of the
five-class, D the pure-even six-class, and L,R the even sextets of
the two mixed classes in their specified roles. The charge reduction
fixes the odd projections, sum(T)=r and sum(D)=q, and requires D
to contain exactly one actual hole t in M minus zero.

Construct the complete local catalogs directly from the original
coordinate dot product. Select every ordered quadruple (T,D,L,R)
of pairwise disjoint even blocks from these catalogs and set

~~~text
U = (E minus zero) minus (T union D union L union R).
~~~

Every such U has 63-3-6-6-6=42 points and contains precisely the
six holes M minus {0,t}. Its sum is zero, since the full even set
has sum zero and r+q+b+c=0. A putative coloring must partition U
into its six pure-even heptads. Each such heptad meets M at most
once, and there are six remaining holes and six labels, so each
meets M exactly once. Thus a cover can use only the 224 even
heptads anchored at exactly one of the seven holes; rows containing
t are automatically unavailable. There are 192 rows avoiding t.

This is a necessary family. The completed odd partial spread is
not reconstructed here, and existence of an even cover alone would
still require a full original-coloring extension check. The tuple
(T,D,L,R) retains both mixed roles; duplicate remaining sets are
counted with their ordered-root multiplicity. The actual t is
recoverable uniquely from U, so taking distinct U does not lose it.

## Legal symmetry reduction

The previous written proof establishes full marked stabilizer orders
32,32,16 for forms I,II,III. In coordinates relative to
(3,12,48;65,71,95), these are g_S k_A, where
k_A(x,y)=(Ax,A^(-T)y), A preserves the unordered five-odd pair
and mixed pair, S is symmetric, and Sy_r=0. There are 4,4,2
allowed restrictions A and eight allowed S in each form.

Each map fixes z, preserves the coordinate dot product, transports
M and the four local catalogs, and may exchange the two mixed
catalogs. In that case reorder the image tuple to restore the mixed
roles. Hence it bijects the complete ordered-root family, preserves
remaining-set multiplicity, and sends a root with hole t to one
with hole g(t). It also bijects anchored heptads. A six-heptad cover
of U is therefore carried to a six-heptad cover of g(U), in either
direction. This proves the orbit reduction before any search.

Retain both actual-hole orbits in every form: I has {48,63} and
{51,60}, II has {3,51} and {12,60}, III has {48,51} and {60,63}.
No transitivity between these orbits is assumed. For each orbit of
remaining sets, retain the least bitmask representative, its actual
hole, hole orbit, orbit size and ordered-root multiplicity. Orbit
sizes need not equal the group order.

## Finite audit and scope

The complete counts, retaining the form labels, are:

| Form | Ordered roots | Distinct remaining sets | Marked group order | Orbit representatives | Orbits by actual-hole orbit |
| --- | ---: | ---: | ---: | ---: | --- |
| I | 7,424 | 7,408 | 32 | 248 | {48,63}:124; {51,60}:124 |
| II | 12,688 | 12,688 | 32 | 474 | {3,51}:287; {12,60}:187 |
| III | 8,160 | 8,112 | 16 | 557 | {48,51}:172; {60,63}:385 |

The orbit-size histograms are I: 8/16/32 with multiplicities
2/30/216; II: 8/16/32 with multiplicities 18/128/328;
III: 4/8/16 with multiplicities 4/94/459. These weighted sums
recover 7,408,12,688,8,112 distinct sets respectively. The group
actions are not free. No cross-form identification is assumed.
Each form has 576 disjoint ordered mixed-sextet pairs, before
testing disjointness from the defects. All four permitted actual
pure-six holes occur in each complete root family.

The checker constructs all local catalogs twice, with independent
bitmask and array clique recursion. It constructs the full ordered
root multiset twice, using bitmask intersections and set membership,
and requires exact equality. It checks each local original color
class, every root's 42-point size, zero sum and actual missing hole.
The complete group is checked for identity, closure, dot preservation,
catalog and mixed-role actions. The orbit partition covers every
required distinct root exactly once, preserves multiplicity and
hole orbit, and includes all actual holes admitted by the roots.

The [checker](../develop/check_dimension_seven_three_six_roots.py)
and [complete representative report](../results/dimension-7-three-six-roots.json)
record the finite counts, input hashes and complete scope.
The full bounded audit takes about two seconds locally with less
than 35 MB maximum RSS and zero swaps.

No covering search, failed-state certificate or full coloring is
produced. Historical covering certificates are not proof inputs to
this new root reduction. No old spread enumeration, Lean or independent
Pro review is rerun. The original six-dimensional formal theorem
retains three standard and four native-evaluation axioms. Both
manuscript PDFs are preserved; publication and submission remain
separate joint decisions.

~~~sh
python3 develop/check_dimension_seven_three_six_roots.py --report /tmp/dimension-7-three-six-roots.json
~~~
