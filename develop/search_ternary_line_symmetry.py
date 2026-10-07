"""Run one bounded solve after auditing the complete ternary symmetry formula."""
from importlib.metadata import version
from itertools import product
from pathlib import Path
from threading import TIMEOUT_MAX, Timer
import argparse
import hashlib
import json
import os
import time

from pysat.formula import CNF
from pysat.solvers import Solver

from check_ternary_line_symmetry import COLORS, audit_restriction, check
from encode_lines_planes_seventeen import build_encoding, encode_bytes
from solver_lifetime import deferred_interrupt


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_instance(contents):
    if not __debug__:
        raise RuntimeError('Run this loader without -O or PYTHONOPTIMIZE.')
    symmetry = check()
    rows, spaces, adjacency, fixed, palettes, variables, base_clauses, construction = build_encoding()
    identifiers = [{color: variables[next(vertex for vertex, row in enumerate(rows) if row == (generator,)), color]
                    for color in COLORS} for generator in symmetry['special_line_generators_in_coordinate_order']]
    representatives = {tuple(orbit['representative']) for orbit in symmetry['orbits']}
    suffix = [[-identifiers[index][color] for index, color in enumerate(pattern)]
              for pattern in product(COLORS, repeat=7) if pattern not in representatives]
    clauses = base_clauses + suffix
    audit = audit_restriction(contents, representatives, identifiers)
    assert len(suffix) == 2155 and len(clauses) == 199499
    assert contents == encode_bytes(variables, clauses)
    cnf = CNF(from_string=contents.decode('ascii'))
    assert cnf.nv == 5789 and cnf.clauses == clauses
    return cnf, rows, adjacency, fixed, palettes, variables, construction, symmetry, audit


def main():
    if not __debug__:
        raise RuntimeError('Run this search without -O or PYTHONOPTIMIZE.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('cnf', type=Path)
    parser.add_argument('--seconds', type=float, default=120)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    if not 0 < args.seconds <= TIMEOUT_MAX:
        parser.error('--seconds must be positive and at most threading.TIMEOUT_MAX')
    stem = 'dimension-7-ternary-line-symmetry'
    if any(os.path.lexists(args.output_dir / (stem + suffix)) for suffix in ('-search.json', '-candidate.json', '.drat')):
        parser.error('output directory contains a previous same-stem attempt; use a fresh directory')
    contents = args.cnf.read_bytes()
    cnf, rows, adjacency, fixed, palettes, variables, construction, symmetry, audit = load_instance(contents)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    report = {'dimension': 7, 'target_colors': 17, 'retained_vertices': 442,
              'variables': cnf.nv, 'clauses': len(cnf.clauses), 'added_symmetry_clauses': 2155,
              'cnf_sha256': hashlib.sha256(contents).hexdigest(),
              'base_cnf_sha256': hashlib.sha256(encode_bytes(variables, cnf.clauses[:-2155])).hexdigest(),
              'base_clause_audit': audit, 'symmetry': symmetry, 'construction': construction,
              'search_sha256': digest(Path(__file__)),
              'solver_lifetime_sha256': digest(Path(__file__).with_name('solver_lifetime.py')),
              'clause_auditor_sha256': digest(Path(__file__).with_name('check_lines_planes_encoding.py')),
              'python_sat_version': version('python-sat'), 'solver': 'Glucose4',
              'time_limit_seconds': args.seconds, 'timeout_scope': 'cooperative_solver_call_only',
              'timer_joined_before_solver_teardown': True, 'solver_run': True, 'lean_run': False}
    print(json.dumps({'event': 'complete_ternary_formula_audited', 'variables': cnf.nv, 'clauses': len(cnf.clauses)}), flush=True)
    with deferred_interrupt() as interruption, Solver(name='g4', bootstrap_with=cnf.clauses, with_proof=True) as solver:
        started = time.monotonic()
        timer = Timer(args.seconds, solver.interrupt)
        interruption['callback'] = solver.interrupt
        try:
            if interruption['pending']:
                raise KeyboardInterrupt
            timer.start()
            solved = solver.solve_limited(expect_interrupt=True)
        finally:
            interruption['callback'] = None
            timer.cancel()
            if timer.ident is not None:
                timer.join()
        report.update(solver_seconds=time.monotonic() - started, stats=solver.accum_stats())
        if solved is True:
            model = {literal for literal in solver.get_model() if literal > 0}
            assert all(any(literal in model if literal > 0 else -literal not in model for literal in clause)
                       for clause in cnf.clauses)
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
    report['scope'] = 'One bounded solve on the fully audited auxiliary442vertex symmetry formula, preserving everyternaryorbit. SAT requires independent442coloring,135tripleextension and original29211vertex/all1160206edge lift verification. CheckedUNSAT excludes onlythissufficientroute, notfull18colorability. Unknown gives nobound; exactn7open>=18. No Lean.'
    (args.output_dir / (stem + '-search.json')).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()
