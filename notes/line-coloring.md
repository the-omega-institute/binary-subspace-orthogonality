# Chromatic bounds for the line graph in dimension six

The current result is 12 <= chi(Gamma_6) <= 13. The lower bound is proved
below, and the 13-color certificate passes the independent integer checker.
The bounded 12-color searches did not decide feasibility.

Let Gamma_6 have the nonzero vectors of F_2^6 as vertices, with distinct vectors
adjacent when their dot product is zero. A color class is therefore a set of
vectors with pairwise dot products one.

## A weighted lower bound

**Lemma.** If an independent set contains t even-weight vectors and o odd-weight
vectors, then 3t+4o <= 19. It has at most six vertices, and equality in cardinality
can occur only for t=5 and o=1.

**Proof.** Write j=(1,1,1,1,1,1). The even vectors lie in E=j-perp. The restriction
of the form to E has radical span(j) and rank four. If o=0, the Gram matrix of
the t selected vectors is J_t+I_t, whose rank is t when t is even and t-1 when
t is odd. Its rank is at most four, so t<=5.

Suppose o>0 and fix an odd selected vector a. For each even selected vector e,
put z_e=e+a. These t vectors lie in a-perp and are orthonormal: each has norm
one, and distinct ones have dot product zero. Their span A is nondegenerate
of dimension t. The space a-perp is nondegenerate of dimension five.

Let D be spanned by u+a over all selected odd vectors u. Pairwise dot products
one imply that D is totally isotropic and orthogonal to a and every z_e.
Hence D is a totally isotropic subspace of the nondegenerate (5-t)-dimensional
space A-perp intersect a-perp, so 2 dim(D) <= 5-t. Distinct selected odd vectors
lie in the affine space a+D, giving o<=2^dim(D). Consequently:

| t | Bound on o |
| --- | --- |
| 0 or 1 | 4 |
| 2 or 3 | 2 |
| 4 or 5 | 1 |

These cases prove the weighted bound and the cardinality statement. QED.

There are 31 nonzero even-weight vectors and 32 odd-weight vectors. Giving them
weights three and four yields total weight 221, whereas a color class has weight
at most 19. Therefore

    chi(Gamma_6) >= ceil(221/19) = 12.

The explicit checked coloring in results/line-coloring.json supplies the current
upper bound, recorded in results/line-coloring-check.json.

## A justified symmetry reduction for testing 12 colors

A hypothetical 12-coloring of 63 vertices has a class of size at least six,
since 12*5<63. By the lemma this class consists of one odd vector a and five
even vectors e. The six vectors a and z_e=e+a form an orthonormal basis of F_2^6.
An isometry sends them to the coordinate basis and sends the color class to

    {1,3,5,9,17,33}.

Thus 12-colorability is equivalent to coloring the 57 remaining vectors with
11 colors, with this particular six-element set used as one color class.

The set-cover search uses maximal independent sets: a coloring gives a cover
by maximal independent sets after extending its classes, and a cover gives a
coloring by assigning each vertex to one chosen set containing it. Covering
does not require disjoint sets. Full-graph maximal sets, intersected with the
57 remaining vertices and made inclusion-maximal, give every maximal independent
set of that induced graph. See develop/search_line_cover.py.

A solver timeout leaves the 12-versus-13 question unresolved. An UNSAT proof
must be checked, and completeness of the independent-set catalog and the
cardinality encoding must also be verified, before claiming an exact value.
