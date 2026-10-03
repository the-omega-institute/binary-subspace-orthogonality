# Reproduce the submitted paper's finite checks

The complete paper and current witnesses are at revision
`28e27a82068a2f9129fdb5d168bd0fc179cf3e48`.
The default branch's research files are an earlier snapshot.

Use a separate directory to inspect that revision:

```sh
git clone https://github.com/the-omega-institute/binary-subspace-orthogonality.git orthogonality-check
cd orthogonality-check
git checkout --detach 28e27a82068a2f9129fdb5d168bd0fc179cf3e48
python3 develop/check_full_coloring.py results/full-15-coloring.json
python3 develop/check_line_coloring.py
python3 develop/check_line_chromatic_exact.py
python3 develop/check_checker_controls.py
```

These independent checkers require Python 3.10 or later and its standard
library. They replay existing certificates; a solver search is unnecessary.

The full graph check covers 2,824 vertices, 3,986,076 distinct pairs and
44,968 orthogonality edges, and verifies the 15-clique. The exact line check
verifies the 12-color witness; the lower bound is a written weighted argument.
Compare the outputs with the revision's `results/full-15-check.json`,
`results/line-coloring-12-check.json` and associated records.

To build the paper, use a LaTeX installation providing the packages named
in `manuscript/paper.tex`:

```sh
cd manuscript
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
```

The committed PDF was previously built and reviewed; this documentation
update does not report a fresh certificate check or LaTeX build.

## Formal verification

The all-dimensional clique source is an attributed upstream snapshot, with
its dependency pin and recorded scope in `formal/UPSTREAM.json`.
The chromatic sources are in `formal/Chromatic/`. They are not a standalone
Lake project.

Read `notes/formal-verification-audit.md` before reporting formal verification.
The historical final six-dimensional theorem has three standard axioms and
four native-evaluation axioms. No completed pure-kernel replacement is
included in the submitted revision. These modules do not formalize the line
lower bound or solve dimension seven.

For any new Lean run, first select the execution machine, measure memory and
check active Lean/Lake processes; retain the toolchain and dependency pins.
A one-off verification does not require changing shared CI.

[Return to the project entrance](../README.md).
