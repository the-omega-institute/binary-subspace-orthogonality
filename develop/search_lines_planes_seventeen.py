"""Run one bounded solve of the sufficient lines/planes seventeen-color encoding."""
from importlib.metadata import version
from pathlib import Path
from threading import Timer
import argparse
import hashlib
import json
import time

from pysat.formula import CNF
from pysat.solvers import Solver

from check_lines_planes_encoding import check
from encode_lines_planes_seventeen import build_encoding, encode_bytes


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if not __debug__:
        raise RuntimeError('Run this search without -O or PYTHONOPTIMIZE.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('cnf', type=Path)
    parser.add_argument('--seconds', type=float, default=120)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    assert 0 < args.seconds < float('inf')
    audit = check(args.cnf)
    rows, spaces, adjacency, fixed, palettes, variables, clauses, construction = build_encoding()
    assert args.cnf.read_bytes() == encode_bytes(variables, clauses)
    cnf = CNF(from_file=str(args.cnf))
    assert cnf.nv == 5789 and cnf.clauses == clauses
    args.output_dir.mkdir(parents=True, exist_ok=True)
    stem = 'dimension-7-lines-planes-17'
    report = {'dimension': 7, 'target_colors': 17, 'retained_vertices': 442,
              'variables': cnf.nv, 'clauses': len(cnf.clauses), 'cnf_sha256': digest(args.cnf),
              'audit': audit, 'construction': construction, 'search_sha256': digest(Path(__file__)),
              'python_sat_version': version('python-sat'), 'solver': 'Glucose4',
              'time_limit_seconds': args.seconds, 'solver_run': True, 'lean_run': False}
    print(json.dumps({'event': 'audited_sufficient_construction_loaded', 'variables': cnf.nv, 'clauses': len(cnf.clauses)}), flush=True)
    with Solver(name='g4', bootstrap_with=cnf.clauses, with_proof=True) as solver:
        started = time.monotonic()
        timer = Timer(args.seconds, solver.interrupt)
        timer.start()
        try:
            solved = solver.solve_limited(expect_interrupt=True)
        finally:
            timer.cancel()
        report.update(solver_seconds=time.monotonic() - started, stats=solver.accum_stats())
        if solved is True:
            model = {literal for literal in solver.get_model() if literal > 0}
            assert all(any(literal in model if literal > 0 else -literal not in model for literal in clause) for clause in cnf.clauses)
            coloring = dict(fixed)
            for vertex, palette in palettes.items():
                chosen = [color for color in palette if variables[vertex, color] in model]
                assert len(chosen) == 1
                coloring[vertex] = chosen[0]
            assert len(coloring) == 442 and all(coloring[vertex] != coloring[neighbor]
                                               for vertex in coloring for neighbor in adjacency[vertex])
            candidate = {'dimension': 7, 'colors': 17,
                         'subspace_colors': [{'basis': rows[vertex], 'color': coloring[vertex]} for vertex in sorted(coloring)],
                         'cnf_sha256': report['cnf_sha256']}
            path = args.output_dir / (stem + '-candidate.json')
            path.write_text(json.dumps(candidate, indent=2) + '\n')
            report.update(status='sat_lines_planes_candidate_requires_independent_check_and_full_lift', candidate_sha256=digest(path))
        elif solved is False:
            proof = solver.get_proof()
            path = args.output_dir / (stem + '.drat')
            path.write_text('\n'.join(proof) + '\n')
            report.update(status='unsat_sufficient_construction_reported_proof_not_checked', proof_sha256=digest(path), proof_lines=len(proof))
        else:
            report['status'] = 'unknown_time_limit'
    report['scope'] = 'One bounded solve on the audited 442-vertex sufficient construction. SAT candidates require independent coloring, three-space extension and original-graph lift checks. UNSAT only rejects this sufficient construction and requires a checked proof; it cannot exclude all eighteen-colorings. Unknown supplies no bound. No Lean.'
    (args.output_dir / (stem + '-search.json')).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()
