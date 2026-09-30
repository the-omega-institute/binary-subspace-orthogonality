# Complement projection retains the exact profile

For T=span(e1+e2,e3+e4,e5+e6), let S be any linear complement to T
and let pi_S be projection along T. Write K=U intersect T and P=pi_S(U).

**Proposition.** The pair (K,P) and the exact profile (dim U,H(U),K(U))
determine each other. Consequently no proper coloring of O_6* can depend
solely on this pair, even for the chosen complement.

**Proof.** Since T is totally isotropic, pairing a vector of T with u=t+s
depends only on s. Thus H(U) is the annihilator of P in T. The pairing
between T and S is perfect: a vector of T orthogonal to S is orthogonal
to both summands of V6, hence zero by nondegeneracy, and both spaces have
dimension three. Therefore P is also the annihilator of H(U) in S.
Finally, the projection restricted to U has kernel K and image P, so
dim U=dim K+dim P. This gives both directions of determination.
Proposition 5.2 then excludes a proper coloring based only on this pair.

For the explicit S=span(e1,e3,e5), the obstruction is visible directly:
pi_S(e1)=pi_S(e2)=e1 because e2=(e1+e2)+e1. The adjacent lines span(e1)
and span(e2) have K={0} and P=span(e1), but their fixed certificate colors
are respectively 10 and 9. This written contradiction applies to any coloring
rule based on these data, independently of the fixed witness.

Projection and intersection with S differ. In the earlier complement example,
span(e1) intersect S has dimension 1 while span(e2) intersect S has dimension 0.
Both projection images nevertheless have dimension 1 and are the same line.

## Requested finite diagnostic

Reza's unchanged script from main commit
`b9131435a10e54cce754de406d84c3a168c7e93d` is actually named
`develop/Complement_projection.py`, with a capital C. Run:

```sh
python3 develop/Complement_projection.py
python3 develop/check_complement_projection.py
```

The [requested output](../results/complement-projection.json) has 240 profiles,
101 single-color and 139 multi-color. The
[independent check](../results/complement-projection-check.json) reproduces the
entire JSON, checks all 2809 vertices outside the clique using an explicit
coordinate projection, and verifies that each new group equals one old exact
group and conversely. Identical counts are explained by identical partitions.
This is a targeted diagnostic of the existing coloring, not a new full-edge
certificate check or a Lean theorem.

## The missing placement datum

For fixed K and P, the remaining choice of U is a linear lift map
f:P -> T/K. For s in P, choose t+s in U and set f(s)=t+K. The value is
well-defined because two choices of t differ by an element of K; closure
of U makes f linear. Conversely,

    U = {t+s : s in P, t+K=f(s)}.

Every linear map gives exactly one such subspace. Thus a profile with
dim K=k and dim P=p has 2^(p*(3-k)) lifts; the checker verifies this
cardinality for all 240 profiles. Also U intersect S=ker f, as subspaces of S.
For span(e1), f(e1)=0; for span(e2), f(e1)=e1+e2 modulo K={0}.
This explains precisely what the projection pair forgets and why the earlier
intersection datum separates these lines.

The complete lift map encodes U, so it is not itself a 15-color rule.
The next structural question is which features of f, together with K and P,
permit a 15-label assignment separating every orthogonal pair. That remains
open, as do the exact line chromatic number and n7. No new solver or Lean
run is involved; the historical six-dimensional Lean theorem retains its
four native-evaluation axioms.
