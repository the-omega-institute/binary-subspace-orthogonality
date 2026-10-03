# An exact criterion for fifteen subspace labels

Reza proposes using the fifteen nonzero subspaces A of T=span(3,12,48) as
color labels. Fix S=span(1,4,16). A candidate may depend on the full lift data
(K,P,f), with coordinate choices stated explicitly. The following gives
necessary and sufficient conditions for a proper precolored rule.

## Conditions for a candidate

Normalize each clique vertex A <= T to carry its own label A. For a non-clique
vertex U=(K,P,f), choose bases k_a of K and p_i of P, and representatives
t_i in T of f(p_i). For W=(L,Q,g), choose bases l_b,q_j and representatives
u_j of g(q_j). Form three matrices over F_2:

    X(U,W)[a,j] = dot(k_a,q_j)
    Y(U,W)[i,b] = dot(p_i,l_b)
    Z(U,W)[i,j] = dot(p_i,q_j) + dot(t_i,q_j) + dot(p_i,u_j).

**Proposition.** A function assigning labels A(U) <= T is a proper
fifteen-coloring with the specified clique labels if and only if:

1. For each non-clique U, the pairing matrix between a basis of A(U) and
   a basis of P is nonzero.
2. For every pair of distinct non-clique vertices U,W with A(U)=A(W),
   at least one of X(U,W), Y(U,W), Z(U,W) is nonzero.

Empty matrices count as zero. These statements are independent of basis
choices. They impose no full-stabilizer equivariance assumption.

**Proof.** Distinct clique vertices have distinct labels. Since T is totally
isotropic, pairing a in A with k+t+s in U leaves dot(a,s). Therefore U is
adjacent to the clique vertex A exactly when the A--P pairing matrix is zero.
The first condition is precisely the requirement to avoid a monochromatic
edge meeting the clique.

For two non-clique vertices, the lift orthogonality criterion is exactly
X=0,Y=0,Z=0. Bilinearity reduces it to the displayed basis matrices. Thus
the second condition is precisely the requirement to avoid an edge inside
one non-clique label fiber. These two kinds of edges exhaust the cases.
Changing t_i by K or u_j by L changes Z by combinations of X or Y entries.
If either cross matrix is nonzero, the second condition already holds;
if both vanish, Z is unaffected. QED.

This is a proved equivalence for assessing a proposed rule. It supplies no
new choice of A(U). A structural construction must define A(U) without
reading the existing certificate and then prove these conditions.

## Label availability is determined by P

The first condition says A(U) is not contained in the annihilator of P in T.
The perfect T--S pairing gives

    dim annihilator_T(P) = 3 - dim P.

There are N(d) nonzero subspaces of a d-space, with N(0)=0,N(1)=1,N(2)=4.
Thus the available labels are exactly the existing lists of sizes15,14,11.
This condition depends on P alone; K and f must help separate non-clique
vertices inside the chosen label fibers.

## Reza's color analysis

The committed script is `develop/analyze_color_function`, with no file
extension, from `7d7fe67abac05191db6f0d104e9931c7a455f85e`.
It prints240 distinct K,P pairs,139 mixed K,P pairs,2809 distinct full
tuples and0 mixed full tuples. Per-color K,P diversity for colors0 through14
is

    78,35,21,96,39,70,90,6,5,38,37,8,20,14,9.

The zero-vector skip is removed when forming P; output counts are unchanged.
The requested statistics are saved in
[color-function-analysis.json](../results/color-function-analysis.json).

The [independent check](../results/color-function-check.json) verifies
every author lift tuple, dimension, reconstruction and statistic against
separately enumerated spans, coordinate projections and quotient cosets.
It exports the correspondence between numerical certificate colors and
subspace-label bases, checks label availability on all2809 non-clique
vertices, and checks condition2 on all710841 distinct same-label non-clique
pairs. At least one of the three matrices is nonzero for every such pair.
The label list sizes occur357,1435,1017 times for sizes11,14,15 respectively.

These checks explain how the existing certificate satisfies the proposition.
They do not discover a formula behind its choices or force a future rule to
reproduce the same numerical coloring.

## Reproduction and next step

```sh
python3 develop/analyze_color_function
python3 develop/check_color_function.py
```

A candidate can give A(K,P,f) by a case division or coordinate construction.
Checking the first condition and same-label fibers will either find an
explicit failed pair or verify the finite instance; a readable proof of the
conditions is the target structural argument. If a rule works with different
certificate colors, it still proves the desired result.

The manuscript and both existing coloring certificates are unchanged.
Exact chi(Gamma_6)=12 and chi(O_6*)=15 remain established. Structural15-coloring
and n7 remain open. No solver or Lean run was needed; the historical
full-subspace n6 Lean theorem retains three standard and four native-evaluation
axioms. The matrix proposition is a written proof, not a Lean theorem.
