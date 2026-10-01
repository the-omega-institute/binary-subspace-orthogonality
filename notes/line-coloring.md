# The line graph in dimension six has chromatic number 12

**Theorem.** chi(Gamma_6)=12. The weighted lower bound below and the
[checked 12-color certificate](../results/line-coloring-12.json) prove equality.
Reza's normalized direct SAT instance from `72dc173` returns SAT, and the
[independent standard-library checker](../develop/check_line_chromatic_exact.py)
checks the resulting coloring against the original graph. Earlier bounded
searches were inconclusive; the old 13-color certificate is retained as history.

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

The twelve classes in results/line-coloring-12.json supply the matching upper
bound, recorded in results/line-coloring-12-check.json. Their sizes are
5,5,5,6,5,5,5,6,5,5,5,6, summing to 63. The independent checker verifies the
partition and all 1953 distinct vertex pairs, including every one of the
961 orthogonality edges. Thus no solver trust is needed for the upper bound.
The full-subspace result chi(O_6*)=15 consequently exceeds the line chromatic
number by exactly three.

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

Reza's direct encoding gives each of the 57 remaining vertices exactly one of
11 colors and forbids equal colors on each of the 780 remaining edges. It has
627 variables and 11772 clauses. Its satisfying assignment extends to a
12-coloring by adjoining the fixed class. The checker independently re-encodes
all clauses using coordinate arithmetic, reproduces the CNF SHA-256 digest,
and verifies the certificate satisfies every clause. This direct encoding
does not depend on completeness of a maximal-independent-set catalogue.

## Reproduction and validation scope

Checking the committed certificate needs only the Python standard library:

```sh
python3 develop/check_line_chromatic_exact.py
```

To repeat the discovery using python-sat, run:

```sh
.venv/bin/python develop/line_chromatic_exact.py --seconds 60
python3 develop/check_line_chromatic_exact.py
```

The author script is preserved with a finite time limit and exports both the
candidate and search record. SAT candidates require the independent check;
UNSAT reports require a checked proof; time limits yield UNKNOWN. The executed
original script and the witness-exporting version both returned SAT in about
seven seconds locally. Exact timings, hashes and the PDF review are in
results/line-chromatic-exact-review-20261001.json. Three invalid controls
(duplicate vertex, zero vector and monochromatic edge) are rejected.

This is a written lower-bound proof and an independently checked finite
upper-bound certificate. No new Lean execution or formalization is claimed;
the historical full-subspace n6 theorem retains its four native-evaluation
axioms. Structural 15-coloring and n7 remain open.
