# The full dimension-six chromatic number is 15

29 September 2026. This result answers the n=6 case of Nikandish's Problem 4.3.

**Theorem.** For the orthogonality graph on all nonzero subspaces of F_2^6,

    chi(O_6*) = 15.

**Lower bound.** Let T = span(3,12,48) in binary integer coordinates. The three
generators have disjoint supports of even size, so the standard dot form vanishes
on T. Its seven lines, seven planes and T itself are fifteen distinct, pairwise
orthogonal nonzero subspaces. They form Nikandish's known 15-clique.

**Upper bound.** The file results/full-15-coloring.json specifies a basis and one
color in {0,...,14} for each of the 2,824 nonzero subspaces. The independent
standard-library checker develop/check_full_coloring.py verifies:

1. Each basis is independent and represents a distinct nonzero subspace.
2. Dimension counts are 63, 651, 1395, 651, 63, 1. These are the Gaussian
   coefficients for dimensions 1,...,6, so every subspace occurs exactly once.
3. For every pair of vertices, orthogonality is tested by the coordinate dot
   product on all pairs of basis vectors. Every orthogonal pair has different
   colors. Bilinearity makes this exactly the graph adjacency condition.

The exhaustive check passes all 3,986,076 pairs, containing 44,968 edges. This
certifies the upper bound 15 and proves equality with the displayed clique.
The result does not require trusting the SAT solver's internals.

## How the certificate was found

Fix distinct colors on the fifteen subspaces of T. Every 15-coloring can be
relabeled to agree with this precoloring. For U not contained in T, define
H(U)=U-perp intersect T. The color of W <= T is forbidden precisely when
W <= H(U). Since T-perp=T, dim H(U) is 0, 1 or 2, giving 15, 14 or 11 allowed
colors respectively. See ../develop/precoloring-reduction.md for the proof.

Reversible deletion removes 729 of the 2,809 uncolored vertices, leaving 2,080
vertices and 39,400 edges. Each remaining vertex gets exactly one variable per
allowed color. Clauses require one color per vertex and forbid equal colors on
each edge. The encoding has 28,600 variables and 627,510 clauses.

Glucose4 found a satisfying assignment, which was extended in reverse deletion
order to all vertices. The archived report is results/search-15.json. The
independent verification record is results/full-15-check.json; its SHA256 values
bind the checker and the supplied certificate.

## Scope and next questions

The all-dimensional clique formula already has a Lean proof in the upstream
project. The new chromatic equality also has the formal statement
`BinaryOrthogonality.chromatic_number_six` in `formal/Chromatic/Verify.lean`.
The historical Mac Studio build report in `results/lean-verification.json`
omits four native-evaluation axioms found in the recovered original log; the
[audit](formal-verification-audit.md) documents the correction and kernel-only
repair. The exhaustive integer checker independently establishes the
JSON witness and the chromatic equality.

The line-graph proof in line-coloring.md now gives chi(Gamma_6)=12<15,
so the chromatic separation is exactly three. Extracting a geometric description
of the 15-coloring remains a useful follow-up. In that direction, group color classes
by H(U), U intersect T and dimension, then ask which choices are essential and
which can be replaced by a uniform construction. Higher-dimensional cases need
new arguments or certificates; no general chromatic formula is claimed.
