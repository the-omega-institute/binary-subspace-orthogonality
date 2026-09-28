"""Search the fixed-clique list instance; export candidates, never infer a proof from timeout."""
from itertools import combinations
from pathlib import Path
from threading import Timer
import argparse
import hashlib
import json
import time

from pysat.formula import CNF
from pysat.solvers import Solver

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seconds', type=float, default=120)
    args = parser.parse_args()
    start = time.monotonic()
    source = ROOT / 'develop/coloring-certificate.json'
    reduction_path = ROOT / 'develop/precoloring-reduction.json'
    data = json.loads(source.read_text())
    reduction = json.loads(reduction_path.read_text())
    assert reduction['input_sha256'] == digest(source)
    rows = [record['basis'] for record in data['subspace_colors']]
    spaces = []
    for basis in rows:
        vectors = {0}
        for row in basis:
            vectors |= {v ^ row for v in vectors}
        spaces.append(sum(1 << v for v in vectors))
    perps = [sum(1 << v for v in range(64) if all((v & r).bit_count() % 2 == 0 for r in b)) for b in rows]
    adj = [set() for _ in rows]
    for i, j in combinations(range(len(rows)), 2):
        if spaces[j] & ~perps[i] == 0:
            adj[i].add(j)
            adj[j].add(i)
    clique = reduction['clique_indices']
    core = reduction['core_indices']
    colors = {v: c for c, v in enumerate(clique)}
    palettes = {v: set(range(15)) - {c for w, c in colors.items() if w in adj[v]}
                for v in set(range(len(rows))) - set(clique)}
    variables = {(v, c): i + 1 for i, (v, c) in enumerate(
        (v, c) for v in core for c in sorted(palettes[v]))}
    cnf = CNF()
    for v in core:
        choices = [variables[v, c] for c in sorted(palettes[v])]
        cnf.append(choices)
        for a, b in combinations(choices, 2):
            cnf.append([-a, -b])
    core_set = set(core)
    for v in core:
        for w in sorted(adj[v] & core_set):
            if w < v:
                for c in sorted(palettes[v] & palettes[w]):
                    cnf.append([-variables[v, c], -variables[w, c]])
    cnf_path = ROOT / 'results/precolored-15.cnf'
    cnf.to_file(str(cnf_path))
    report = {'input_sha256': digest(source), 'reduction_sha256': digest(reduction_path),
              'search_sha256': digest(Path(__file__)), 'solver': 'Glucose4 via python-sat 1.8.dev24',
              'variables': cnf.nv, 'clauses': len(cnf.clauses), 'cnf_sha256': digest(cnf_path),
              'time_limit_seconds': args.seconds}
    print(json.dumps({'event': 'encoded', **report}), flush=True)
    with Solver(name='g4', bootstrap_with=cnf.clauses, with_proof=True) as solver:
        # Seed phases from the existing coloring, relabeled on the fixed clique.
        previous = [r['color'] for r in data['subspace_colors']]
        relabel = {previous[v]: c for v, c in colors.items()}
        solver.set_phases([variable if relabel.get(previous[v]) == c else -variable
                           for (v, c), variable in variables.items()])
        timer = Timer(args.seconds, solver.interrupt)
        timer.start()
        try:
            solved = solver.solve_limited(expect_interrupt=True)
        finally:
            timer.cancel()
        report['stats'] = solver.accum_stats()
        report['elapsed_seconds'] = time.monotonic() - start
        if solved is True:
            model = {x for x in solver.get_model() if x > 0}
            for v in core:
                picked = [c for c in palettes[v] if variables[v, c] in model]
                assert len(picked) == 1
                colors[v] = picked[0]
            for step in reversed(reduction['deletion_certificate']):
                v = step['vertex']
                available = palettes[v] - {colors[w] for w in adj[v] if w in colors}
                assert available
                colors[v] = min(available)
            assert len(colors) == len(rows)
            assert all(colors[v] != colors[w] for v in range(len(rows)) for w in adj[v])
            candidate = {'dimension': 6, 'colors': 15, 'encoding': data['encoding'],
                         'subspace_colors': [{'basis': basis, 'color': colors[v]} for v, basis in enumerate(rows)],
                         'source_sha256': digest(source), 'cnf_sha256': report['cnf_sha256']}
            path = ROOT / 'results/full-15-coloring.json'
            path.write_text(json.dumps(candidate, indent=2)+'\n')
            report.update(status='sat_candidate_extended_to_full_graph', candidate_sha256=digest(path))
        elif solved is False:
            proof = solver.get_proof()
            path = ROOT / 'results/precolored-15.drat'
            path.write_text('\n'.join(proof)+'\n')
            report.update(status='unsat_reported_proof_not_yet_checked', proof_sha256=digest(path), proof_lines=len(proof))
        else:
            report['status'] = 'unknown_time_limit'
    (ROOT / 'results/search-15.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()
