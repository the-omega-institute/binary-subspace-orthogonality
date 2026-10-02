# v6: stabilizer obstruction verified, requested screens fail

Reza's commit `9a96fad30b00c3c7e22ec52f5a31239fd5649658` asks for two cheap
screens before a full replay and for a direct check of a stabilizer-orbit
claim. The independent record is
[color-candidate-v6-check.json](../results/color-candidate-v6-check.json).

## The stabilizer claim

The orbit claim is true, but one displayed target equation needs correction.
Use the ordered bases

    T=(a_1,a_2,a_3)=(3,12,48),   S=(e_1,e_3,e_5)=(1,4,16)

and define (B:S\to T) by

    B(1)=3,  B(4)=12,  B(16)=0.

The matrix of (B) in these paired bases is (operatorname{diag}(1,1,0)),
which is self-adjoint. Therefore

    g_B(t+s) = t+B(s)+s

preserves the standard dot form and fixes (T) pointwise. Direct enumeration
gives (g_B(13)=14) and (g_B(6)=9), so

    g_B(span(13,6)) = span(14,9) = span(9,14).

The suggested equation (g_B(13)=7) cannot hold for a map of this form:
such a shear fixes the (S)-projection, while 13 and 7 have different
(S)-projections. The corrected images still prove that the two adjacent
planes lie in one Stab(T) orbit. Their cross dot products are all zero, so
every coloring invariant under Stab(T) assigns them one color.

## v6 screens

The requested candidate separates the pair:

    span(13,6) -> span(3,12,15,48,51,60,63),
    span(9,14) -> span(3,12,15,48).

It fails the second screen: the fourteen-clique receives **7** distinct
labels, whereas the requested threshold is 14. The author script also prints
8,908 same-label orthogonal pairs in the full replay; because screen 2 already
fails, the full replay was not rerun independently. The first screen passes,
the second fails, so v6 is rejected under the author's stated criterion.

The independent checker reconstructs all 2,809 outside vertices and verifies
the two labels, the seven-label clique count, the self-adjoint matrix, and the
explicit isometry witness. No solver, Lean or n=7 computation was needed.
The manuscript and established certificates are unchanged. The structural
15-coloring formula and n=7 remain open; the historical full-subspace n=6
Lean theorem retains its four native-evaluation axioms.
