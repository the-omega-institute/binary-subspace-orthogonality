# Binary subspace orthogonality graphs

Public research workspace for Haobo Ma, Reza Nikandish and Wenlin Zhang.
Working paper direction: *Clique and chromatic numbers of binary subspace
orthogonality graphs*. Author order and the final manuscript are to be agreed.

For the standard dot form on F_2^n, O_n* has all nonzero subspaces as vertices;
distinct subspaces are adjacent when they are orthogonal. Gamma_n is its induced
graph on one-dimensional subspaces, identified with the nonzero vectors.

## Current results

- The all-dimensional clique formula is
  `omega(O_n*) = max(n, N(floor(n/2)) + (n mod 2))`, where N(r) counts nonzero
  subspaces of F_2^r. The radical/quotient proof solves Nikandish's Problem 4.2
  and has an existing Lean formalization.
- **chi(O_6*) = 15.** A new 15-coloring of all 2,824 subspaces matches the known
  15-clique. The independent checker verifies all 3,986,076 vertex pairs,
  including all 44,968 orthogonality edges. See [the result](notes/dimension-six.md),
  [certificate](results/full-15-coloring.json) and [check record](results/full-15-check.json).
- **12 <= chi(Gamma_6) <= 13 < 15.** A weighted independent-set argument gives
  the lower bound, and a new checked 13-coloring gives the upper bound. See
  [the proof](notes/line-coloring.md) and [the certificate](results/line-coloring.json).
  The line-versus-full-subspace separation is therefore at least two colors.

The dimension-six coloring is an exact finite certificate result; it has not
yet been formalized in Lean. Problem 4.3 for arbitrary n >= 7 remains open here.

## Check the new result

The independent checker needs only Python 3.10 or later and its standard library:

```sh
python3 develop/check_full_coloring.py results/full-15-coloring.json
python3 develop/check_line_coloring.py
python3 develop/check_checker_controls.py
```

It reconstructs all subspaces from their bases, checks their distinctness and
Gaussian dimension counts, tests orthogonality for every vertex pair directly
from coordinates, and checks the known 15-clique. It imports neither the search
program nor a SAT library. A satisfying solver assignment is not trusted as a
substitute for these checks.

To replay preprocessing and regenerate the search:

```sh
python3 develop/precoloring_reduction.py
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python -r requirements-search.txt
.venv/bin/python develop/search_coloring.py --seconds 120
python3 develop/check_full_coloring.py results/full-15-coloring.json
```

The search uses the fixed 15-clique, geometric color lists, and reversible degree
deletion. It encodes the 2,080-vertex core in 28,600 Boolean variables and 627,510
clauses. Generated CNF files are ignored; their hashes and exact reconstruction
are retained. A different satisfying coloring is valid if it passes the checker.

## Files and collaboration

- `develop/`: exact search, preprocessing and independent verification programs;
  includes the archived earlier 14/16-color witnesses and their checker.
- `results/`: current certificates and execution records.
- `notes/`: current mathematics and the historical September 28 note. The latter
  reports the earlier interval {15,16}; it is preserved as a dated starting point.
- `formal/`: the exact upstream clique proof, source pin and original license.

Reza has proposed drafting the introduction and clique section and developing
geometric arguments. Wenlin develops written arguments and computational
exploration; Haobo leads formal verification. The next shared task is to explain
the dimension-six coloring structurally, integrate the result into the joint
paper, and select a formalization target. Larger dimensions and other parameters
can be developed alongside that work.

The source problem is Reza Nikandish, *Annihilating-Ideal Graphs and Orthogonality
Graphs over F_2*, [arXiv:2609.22769v1](https://arxiv.org/abs/2609.22769v1).
His coordinate and isotropic constructions supply lower bounds; the new clique
upper proof and finite coloring certificates are identified separately above.
See [provenance and rights](RIGHTS.md). No DOI or versioned release is configured.
