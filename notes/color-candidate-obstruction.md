# The first available line label does not give a proper coloring

Reza's candidate in `53428f67566d1cf305a90bd91dc873c645126b19` chooses the
first subspace label A having a nonzero pairing with P. For
T=span(3,12,48) and S=span(1,4,16), its line order starts with 3,12,48.
The rule passes label availability but fails same-label separation.

## A two-line counterexample

Let U=span(1) and W=span(2), the first two coordinate lines. They are distinct
and orthogonal: dot(1,2)=0. Both have K={0} and P=span(1). Their lift values
on the basis vector 1 are respectively 0 and 3, since 2=3+1 with 3 in T.

The candidate gives both vertices A=span(3), because dot(3,1)=1. Thus both
pass the label/P condition but form a monochromatic edge. The three matrices
in the [label criterion](subspace-label-criterion.md) are

    X and Y empty, Z=[dot(1,1)+dot(0,1)+dot(1,3)]=[1+0+1]=[0].

All arithmetic is over F2. This is a direct written disproof of the candidate.
It also shows that changing the order of labels while retaining dependence
on P alone cannot work: U and W have the same P. Even adding K alone does
not separate them, as already proved in the complement-projection obstruction.
The different lift values must affect these vertices' labels in any proper
rule. Equivalent examples use the paired coordinates (3,4) and (5,6).

## Why only three labels are used

Every non-clique vertex has P nonzero: P=0 would imply U is contained in T.
The pairing T--S is perfect, and 3,12,48 form a basis of T. Therefore at
least one of these three vectors pairs nontrivially with any nonzero P.
The first-available rule always returns one of these three line labels;
the remaining four lines, plane labels and fallback T are never reached.

There are also two duplicate plane entries in the hard-coded label list:
span(3,15)=span(3,12) and span(12,60)=span(12,48). Hence the fifteen entries
describe only thirteen distinct subspaces, including five distinct planes.
The two missing planes are span(3,60) and span(15,51). This is secondary to
the counterexample: repairing the list alone does not change this rule's
choices. A later rule can enumerate all subspaces of T directly.

## Reproduced and independently checked counts

The original unmodified script prints 2809 non-clique vertices, three labels,
zero condition-1 violations and 25496 condition-2 violations. The label fibers
have sizes 2451,307,51.

The [independent checker](../develop/check_color_candidate.py) verifies all
lift data against coordinate projection and quotient cosets and all candidate
labels against the first-nonzero-pairing description. It checks adjacency
directly from the original coordinate dot product for every same-label pair,
independently of the author's three-matrix implementation:

| Label basis | Vertices | Distinct same-label pairs | Monochromatic edges |
| --- | ---: | ---: | ---: |
| 3 | 2451 | 3002475 | 24006 |
| 12 | 307 | 46971 | 1369 |
| 48 | 51 | 1275 | 121 |
| Total | 2809 | 3050721 | 25496 |

The original lift routine omits zero from P for 1016 vertices with K=0.
The checker normalizes P by adjoining zero and verifies that all labels stay
unchanged; this omission does not cause the failed separation. The original
candidate file is preserved without edits. The explicit two-line example
is also checked against the author's matrix test.

```sh
python3 develop/color_function_candidate.py
python3 develop/check_color_candidate.py
```

The [JSON report](../results/color-candidate-check.json) binds source,
checker and certificate hashes. The checked outcome rejects this candidate;
it does not reject a rule using full (K,P,f). A next candidate must use the
lift values to distinguish the displayed pairs and must prove separation
of every same-label fiber as well as availability.

The manuscript and existing 15-color and 12-color certificates are unchanged.
Exact chi(O_6*)=15 and chi(Gamma_6)=12 remain established. Structural coloring
and n=7 remain open. No solver, Lean or dimension-seven computation was run;
the historical full-subspace six-dimensional Lean theorem retains three
standard plus four native-evaluation axioms.
