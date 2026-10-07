# Thirty-two ternary special-line patterns for the sufficient eighteen-color route

The auxiliary graph on 127 lines and 315 totally isotropic planes admits
an exact restriction to 32 patterns on its seven special odd lines.
The restriction preserves seventeen-colorability of this 442-vertex graph.
It supplies no coloring: the full dimension-seven chromatic number remains
open with the written lower bound eighteen.

## Orthogonal lifts and normalized colors

Put T=span(3,12,48), z=127 and D=span(65,71,95). In the ordered basis
formed by these triples followed by z, the Gram matrix is

```text
[ 0 I 0 ]
[ I 0 0 ]
[ 0 0 1 ].
```

For every A in GL(3,2), the map g_A(x,y,a)=(Ax,A^{-T}y,a) preserves
this form, fixes z and maps T to itself. It therefore preserves the
lines-and-isotropic-planes graph. It sends the special line [z+t] to
[z+At]. Every action on the seven nonzero T-vectors is realized in the
whole graph; arbitrary permutations of seven points are not justified.

The fixed clique here has fifteen vertices: the fourteen nonzero proper
T-subspaces W_i, colored i=0,...,13, and [z], colored 14. T itself is
absent. Write g_A(W_i)=W_{pi_A(i)}. Define rho_A on labels 0,...,13 by
rho_A(i)=pi_A(i), fix label 14 and either fix or globally interchange
labels 15 and 16. For any normalized proper coloring c, define

```text
c'(g_A U) = rho_A(c(U)).
```

This preserves properness and restores every fixed label, since
c'(g_A W_i)=pi_A(i). Both extra labels are unused by the fixed clique
and occur in every residual palette, so their global interchange is
valid. Interchanging label 14 with an extra label does not preserve
this normalization. The old full-graph seventeen-color binary forcing
argument is not used.

Consequently an assignment f(t) in {14,15,16} to the seven special
lines transforms by f'(At)=sigma(f(t)), where sigma fixes 14 and
optionally interchanges 15 and 16. Every auxiliary coloring can be
normalized to one representative under this group of order 336.

## Exhaustive orbit classification

Coordinate indices 1,...,7 are binary coefficients in the ordered
basis (3,12,48). The corresponding special-line generators are
124,115,112,79,76,67,64. A pattern is a seven-entry tuple in this order.
Representatives are lexicographic minima using 14<15<16.

There are 60 orbits under GL(3,2) alone and 32 after the extra-label
interchange. The following table retains every orbit type.

| Representative in coordinate order | Orbit size |
| --- | ---: |
| 14 14 14 14 14 14 14 | 1 |
| 14 14 14 14 14 14 15 | 14 |
| 14 14 14 14 14 15 15 | 42 |
| 14 14 14 14 14 15 16 | 42 |
| 14 14 14 14 15 15 15 | 56 |
| 14 14 14 14 15 15 16 | 168 |
| 14 14 14 15 15 15 15 | 14 |
| 14 14 14 15 15 15 16 | 56 |
| 14 14 14 15 15 16 16 | 42 |
| 14 14 15 14 15 15 14 | 14 |
| 14 14 15 14 15 15 15 | 56 |
| 14 14 15 14 15 15 16 | 56 |
| 14 14 15 14 15 16 14 | 42 |
| 14 14 15 14 15 16 15 | 168 |
| 14 14 15 14 15 16 16 | 168 |
| 14 14 15 15 15 15 15 | 42 |
| 14 14 15 15 15 15 16 | 168 |
| 14 14 15 15 15 16 16 | 168 |
| 14 14 15 15 16 16 15 | 84 |
| 14 14 15 15 16 16 16 | 168 |
| 14 14 15 16 16 16 16 | 42 |
| 14 15 15 15 15 15 15 | 14 |
| 14 15 15 15 15 15 16 | 84 |
| 14 15 15 15 15 16 16 | 42 |
| 14 15 15 15 16 15 16 | 168 |
| 14 15 15 15 16 16 16 | 84 |
| 14 15 16 15 16 15 16 | 56 |
| 15 15 15 15 15 15 15 | 2 |
| 15 15 15 15 15 15 16 | 14 |
| 15 15 15 15 15 16 16 | 42 |
| 15 15 15 15 16 16 16 | 56 |
| 15 15 15 16 16 16 16 | 14 |

The sizes sum to 3^7=2187. The [checker](../develop/check_ternary_line_symmetry.py)
compares exhaustive matrix images with breadth-first orbits generated
by the two elementary actions with columns (2,4,1) and (1,3,4), together
with the extra-label interchange. Their permutation closure is exactly
all 168 linear actions.

Burnside gives an additional check. A permutation with r cycles fixes
3^r assignments without a label swap. With the swap, an odd cycle must
be entirely label 14; each even cycle has three possible alternating
assignments. Thus the fixed-point sums are 10080 without the swap and
672 with it. The orbit count is (10080+672)/336=32. None of the reduction
uses a pattern's color cardinalities as a substitute for its Fano geometry.

## Checked clause restriction

For every nonrepresentative pattern p append

```text
not x_(1,p_1) or ... or not x_(7,p_7),
```

where x_(i,k) is the existing one-hot variable assigning color k to
special line i. Each clause excludes exactly that pattern on valid
one-hot assignments. All 32 representatives remain. Any normalized
auxiliary coloring has a group image with a retained representative,
so the restricted and base formulas are satisfiable together or
unsatisfiable together. This equivalence concerns the auxiliary
seventeen-color problem only.

The CNF keeps 5789 variables and adds 2155 seven-literal clauses to the
197344 base clauses, for 199499 total. Its SHA256 is
`515031623b1f90f1d26f28a499dc088d0bb27cf4217bd66d1bd4bda892c36ea6`.
The base hash remains
`f3c9d0d2df5217baad87c93ca6a3e8dcd33d53182c5aa5249962f2187a89d116`.

The geometric auditor checks every base clause independently of the
builder, sharing only RREF/span helpers. The emitted suffix is decoded
back to its excluded assignments and tested on all 2187 valid patterns:
every nonrepresentative fails exactly one clause and every representative
passes. Missing, duplicate and representative-excluding clause mutations
are rejected. The source base bytes are recovered exactly from readback.
The finite [report](../results/dimension-7-ternary-line-symmetry.json)
also records all 2752512 vector-pair isometry checks, 74256 vertex images,
2783592 edge images and 143472 normalized palette images. An arbitrary
point transposition fails linearity; swapping 14 with 15 fails a palette.

```sh
python3 develop/encode_lines_planes_seventeen.py --output-dir /tmp/lines-planes
python3 develop/check_ternary_line_symmetry.py --cnf /tmp/lines-planes/dimension-7-lines-planes-17.cnf --output-cnf /tmp/lines-planes/dimension-7-ternary-symmetry.cnf --report /tmp/ternary-symmetry.json
```

No solver or Lean runs form part of the orbit proof itself. The dedicated
[symmetry runner](../develop/search_ternary_line_symmetry.py) now audits this
extended formula from one immutable input snapshot before solving. A SAT candidate
still needs independent auxiliary coloring verification, a fresh color
on all 135 independent three-spaces, and a checked lift to every original
vertex and edge. Even checked auxiliary UNSAT would only reject this
sufficient construction, leaving full eighteen-colorability open.

## Search provenance repair

An independent Pro review approved the prior base encoding and identified
two search-wrapper defects. Separate path reads could record different
bytes from those parsed for the solver; an accepted extreme finite timeout
could overflow in the timer thread. Both failures were reproduced locally
using the real PySAT parser with an explicitly identified solver double,
and a real standard-library timer. The runner now reads a single immutable
byte snapshot for the audit, canonical comparison, parser and all CNF hashes,
and rejects values outside (0,threading.TIMEOUT_MAX]. Path replacement after
parsing no longer changes the recorded instance identity. Five invalid
timeouts and the six original clause mutations are rejected.

The historical 120-second unknown report is preserved. Its nested and outer
CNF hashes agree, its timeout is within range, and no evidence shows either
defect affected that run. Local regression checks here do not repeat a solve
or independently witness the historical execution. Reviewer reconstruction
claims are recorded separately from the local checks. The submitted paper
remains at 28e27a8; the dimension-six formal theorem retains its three
standard and four native-evaluation axioms.

The next independent Pro review approved the proof, all 32 representatives
and the complete CNF restriction. It identified two further implementation
points: the reported breadth-first loops actually used stacks, and cancelling
a timer did not wait for an interrupt callback already in progress. The
traversals now use deque.popleft(); the orbit partition and both CNF byte
streams remain unchanged. Both search runners cancel and join their timer
inside the solver context. A local test with a real timer and a deliberately
delayed solver double reproduced the callback surviving an unjoined context
and verified completion before teardown with the join. This is a lifecycle
test, not evidence of a historical native-solver failure.

The dedicated runner separately audits every base clause and decodes the
complete symmetry suffix, checks canonical bytes, parses the same snapshot
with PySAT and compares all 199499 parsed clauses. Local controls reject
missing, duplicate, representative-excluding and changed-base clauses.
A semantically valid permutation of base clauses passes the geometric audit
and is rejected by the runner's canonical identity check. A path replacement
after real parsing does not change its recorded CNF hashes. The low-level
loader and CLI also reject optimized Python. Its timeout covers the solver
call cooperatively; it is not an end-to-end deadline for auditing and output.

```sh
python develop/search_ternary_line_symmetry.py /tmp/lines-planes/dimension-7-ternary-symmetry.cnf --seconds 120 --output-dir /tmp/lines-planes
```

One Glucose4 attempt on the fully audited 199499-clause formula returned
**unknown** after 120.01907758400193 seconds of measured solver time.
It recorded 6262 restarts, 1235097 conflicts, 2833661 decisions and
212816856 propagations, without a coloring or UNSAT proof. The
[search report](../results/dimension-7-ternary-line-symmetry-search.json)
binds the exact unchanged symmetry CNF, current checker/runner/auditor,
construction and python-sat 1.8.dev24. The local 16 GiB machine had 74%
available memory before the attempt; observed process RSS at 110 seconds
was 247168 KiB. No Lean/Lake process or Lean run was involved.

This is one new bounded attempt on a structurally changed formula; the
earlier base-formula unknown report is preserved. It supplies no upper
bound or evidence of nonexistence. Further continuation should extract a
specific branch restriction or resolve an independent review finding,
rather than repeat this unchanged solve.

The subsequent [all14 branch proof](all14-special-line-branch.md) isolates
one retained orbit as an exact 434-vertex sixteen-color problem. It also
derives the omitted-pair lists on its 56 odd lines and checks the branch
formula by direct substitution; no new solve or branch exclusion is claimed.

The next Pro review approved the complete formula and input identity,
but found that an exception during timer startup could bypass cleanup,
and an existing output directory could retain stale same-stem evidence.
Both local runners now start the timer inside the cleanup-protected block,
cancel even after startup failure, and join a launched timer. They reject
pre-existing report, candidate or proof collisions before reading the
input. Real-timer startup interruption tests and six collision controls
verify these paths without native solver calls or deleting historical files.
The recorded 120-second unknown report retains its original source hashes;
there is no evidence that these exceptional-path defects affected it.
