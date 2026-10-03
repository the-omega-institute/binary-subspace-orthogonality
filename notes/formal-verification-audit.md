# Formal verification source audit, 30 September 2026

The exact finite certificate proves `chi(O_6*) = 15`. Its standard-library
checker was rerun successfully during this review. The separate claim that
the archived chromatic Lean theorem has only the three standard axioms is
incorrect: the original machine log has now been recovered and contains four
additional native-evaluation axioms. The historical report is preserved with
the correction in `results/lean-verification-audit-20260930.json`.

## Fixed evidence

Reviewed research revision: `f34e58f46d4065e88cdfd209cbb17cff99aa89d8`.
The historical build report entered the repository at
`9db3c662d5bd9e4fd8ac705f512b41ee6556125a` and remains preserved in
`results/lean-verification.json`. It reports Lean 4.33.0 on Mac Studio,
452.28 seconds, and axioms `propext`, `Classical.choice`, `Quot.sound`.
All three recorded source hashes match the committed source:

| File in `formal/Chromatic/` | SHA-256 |
| --- | --- |
| `Certificate.lean` | `dd19f0ea5d3bc15b7ad48e2558bb2964ed9f4cc5e23b70b42641b2390c3a6b35` |
| `Data.lean` | `83837b0157268a5356d3b4265f0669da21878581aca348f07fc6f8b9384644db` |
| `Verify.lean` | `28938d5d5385397442720d9d5c8a4b15287a162bce100c65b97f42d3e34d9401` |

`Verify.lean` proves `catalogue_covers`, `catalogue_proper`, `clique_valid`
and `clique_adjacent` using `native_decide`. In the installed Lean 4.33.0
source, `Lean/Elab/Tactic/Decide.lean` implements that tactic by enabling
native evaluation and calling `Lean.Meta.nativeEqTrue`.
`Lean/Meta/Native.lean` explicitly constructs a `Declaration.axiomDecl`
named with the `_native.native_decide.ax` suffix after successful evaluation.
Upstream sources:

- <https://github.com/leanprover/lean4/blob/v4.33.0/src/Lean/Elab/Tactic/Decide.lean>
- <https://github.com/leanprover/lean4/blob/v4.33.0/src/Lean/Meta/Native.lean>

The recovered original log confirms successful compilation of these exact
source files, with the following final-theorem dependencies:

```
propext
Classical.choice
Quot.sound
catalogue_covers._native.native_decide.ax_1_1
catalogue_proper._native.native_decide.ax_1_1
clique_adjacent._native.native_decide.ax_1_1
clique_valid._native.native_decide.ax_1_1
```

The generic `Catalogue.complete` and `Catalogue.colorable` reports contain
only the three standard axioms. The historical summary omitted the four
additional axioms from the final chromatic theorem. The recovered log's SHA-256
is `c1af4a33c6e4ae20ffe12edda86c0d6a9295b1e242b77e589bd51d60e1faa3cb`.
The run exited successfully in 452.28 seconds, at 3,038,838,784 bytes maximum
resident set size. These are historical measurements, not a new kernel-only
verification.

## Mathematical and formal scope

The encoded vertices are nontrivial finite subsets of `Fin 64` containing
zero and closed under XOR. These are the binary subspaces under the usual
bit-coordinate identification. Distinct vertices are adjacent precisely when
all coordinate dot products vanish. This interpretation is explained in the
manuscript; an explicit Lean graph isomorphism to the upstream abstract
`Submodule` graph is not supplied by this module.

`Catalogue.complete` proves coverage by adjoining vectors, with 2,825
catalogue entries including zero and 180,800 extension witnesses.
`Catalogue.colorable` transfers a proper catalogue coloring to the encoded
graph. The final equality also uses the indexed 15-clique. These generic
arguments and the finite assertions must be distinguished when reporting
trust dependencies. The line lower bound and dimension-seven reduction are
written proofs, not statements of this chromatic Lean module.

The upstream all-dimensional clique snapshot has the recorded SHA-256
`7c96c81d37c525e3f47e6bdaacb69ff263770cb058d16f36d7babe899e62816a`.
It has no `native_decide`, `sorry` or explicit axiom declaration. Its historical
verification record is separate; this audit is not a new build of that file.

## Kernel-only repair

The user authorized local execution if resources permit, otherwise Mac Studio.
The local 16 GB machine had approximately 6.7 GB swap occupied; the selected
Mac Studio has 96 GB RAM. Available memory and actual `lean`/`lake` process
basenames were measured before execution. Validation uses Lean 4.33.0 and
Mathlib `db584cd6d46c92f209a44c0f1c829460d327499d` from a read-only dependency
cache, in an isolated directory. Shared CI is unchanged.

The repair replaces native assertions with `decide +kernel`. Decimal parsing
moves to a term elaborator that emits literal natural-number arrays, and the
tables use nested blocks of 64 entries. The numerical tables are identical
to the original witness. Finite coverage and properness checks are split into
bounded ranges and joined by ordinary proved lemmas. See
`formal/Chromatic/README.md` for the representation and reproducible commands.
