# Extended working draft — October 8, 2026

[Read the extended PDF](paper.pdf) · [LaTeX source](paper.tex) ·
[Collaboration PR #1](https://github.com/the-omega-institute/binary-subspace-orthogonality/pull/1)

This is a working draft for coauthor review. The manuscript snapshot
`28e27a82068a2f9129fdb5d168bd0fc179cf3e48` submitted to JAC, its PDF,
and the existing Zenodo record are preserved. Preparation of this draft
does not decide publication, submission, revision, or a separate paper.
The author and disclosure blocks retain the existing wording for joint review.

The new Section 6 gives a complete written proof that the dimension-seven
line and full-subspace graphs need at least 19 colors, while the full graph
has clique number 16. It combines independent-class capacity, quadratic
parity, and a universal eight-Lagrangian completion lemma. The exact
dimension-seven chromatic numbers remain open.

Section 7 derives common deficit, parity-count, projected-charge and hole
capacity constraints for nineteen colors, and states the precise scope of
the partial case analysis. Its six/seven-Lagrangian completion premises and
marked-form covering exclusions retain their separate finite dependencies;
they are not needed for the written lower bound 19. The original
six-dimensional Lean theorem still uses three standard axioms and four
native-evaluation axioms. No dimension-seven Lean formalization is claimed.

Build from this directory, using TeX Live:

```sh
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
```

The unchanged clique, line, dimension-six and geometry sections are imported
from `../sections/`. Reproduce the two bounded checks from the repository root:

```sh
python3 develop/check_dimension_seven_nineteen_obstruction.py --report /tmp/n7-lower19.json
python3 develop/check_dimension_seven_profile_scope.py --report /tmp/n7-scope.json
```

The resulting reports should match `results/dimension-7-nineteen-obstruction.json`
and `results/dimension-7-profile-scope.json`. These commands do not rerun the
separate spread-completion or covering enumerations. See
`notes/dimension-seven-six-holes.md`, `notes/dimension-seven-seven-holes.md`,
`notes/dimension-seven-five-four-D-cover.md`,
`notes/dimension-seven-five-four-H-cover.md`, and
`notes/dimension-seven-profile-scope.md` for their written arguments,
reproduction commands, and precise dependencies.
