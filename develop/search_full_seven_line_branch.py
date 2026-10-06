"""Run one bounded solve on the audited saturated mask127 branch."""
from importlib.metadata import version
from pathlib import Path
from threading import Timer
import argparse
import hashlib
import json
import time

from pysat.formula import CNF
from pysat.solvers import Solver

from check_full_seven_line_encoding import check
from check_nonradical_retraction import nonradical_target
from dimension_seven_feasibility import bases, span
from encode_full_seven_line_branch import build_encoding, encode_bytes


ROOT = Path(__file__).resolve().parents[1]


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
    reference_path = ROOT / 'results/dimension-7-full-seven-line-branch-encoding-check.json'
    reference = json.loads(reference_path.read_text())
    audit = check(args.cnf)
    assert all(audit[key] == reference[key] for key in ('cnf_sha256', 'checker_sha256', 'basis_enumerator_sha256', 'variables', 'clauses'))
    rows, spaces, adjacency, fixed, palettes, variables, clauses, construction = build_encoding()
    assert args.cnf.read_bytes() == encode_bytes(variables, clauses)
    cnf = CNF(from_file=str(args.cnf))
    assert cnf.nv == 6286 and cnf.clauses == clauses
    args.output_dir.mkdir(parents=True, exist_ok=True)
    stem = 'dimension-7-full-seven-line-branch'
    report = {'dimension': 7, 'target_colors': 17, 'pattern_mask': 127,
              'variables': cnf.nv, 'clauses': len(cnf.clauses), 'cnf_sha256': digest(args.cnf),
              'audit_report_sha256': digest(reference_path), 'audit_checker_sha256': audit['checker_sha256'],
              'branch_checker_sha256': digest(ROOT / 'develop/check_full_seven_line_branch.py'),
              'branch_report_sha256': digest(ROOT / 'results/dimension-7-full-seven-line-branch.json'),
              'retraction_sha256': digest(ROOT / 'develop/check_nonradical_retraction.py'),
              'search_sha256': digest(Path(__file__)), 'construction': construction,
              'python_sat_version': version('python-sat'), 'solver': 'Glucose4',
              'time_limit_seconds': args.seconds, 'solver_run': True, 'lean_run': False}
    print(json.dumps({'event': 'audited_mask127_input_loaded', **report}), flush=True)
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
            assert all(any(literal in model if literal > 0 else -literal not in model for literal in clause)
                       for clause in cnf.clauses)
            coloring = dict(fixed)
            for vertex, palette in palettes.items():
                picked = [color for color in palette if variables[vertex, color] in model]
                assert len(picked) == 1
                coloring[vertex] = picked[0]
            assert len(coloring) == 577
            assert all(coloring[vertex] != coloring[neighbor] for vertex in coloring for neighbor in adjacency[vertex])
            retained_colors = {spaces[vertex]: color for vertex, color in coloring.items()}
            candidate = {'dimension': 7, 'colors': 17, 'pattern_mask': 127,
                         'subspace_colors': [{'basis': basis, 'color': retained_colors[frozenset(span(nonradical_target(basis)))]}
                                            for basis in bases(7, 7)], 'cnf_sha256': report['cnf_sha256']}
            path = args.output_dir / (stem + '-candidate.json')
            path.write_text(json.dumps(candidate, indent=2) + '\n')
            report.update(status='sat_candidate_requires_independent_original_graph_check', candidate_sha256=digest(path))
        elif solved is False:
            proof = solver.get_proof()
            path = args.output_dir / (stem + '.drat')
            path.write_text('\n'.join(proof) + '\n')
            report.update(status='unsat_reported_branch_proof_not_checked', proof_sha256=digest(path), proof_lines=len(proof))
        else:
            report['status'] = 'unknown_time_limit'
    report['scope'] = 'One bounded attempt on the audited mask127 saturated branch only. Other nine orbits remain. SAT candidates need independent original-graph verification; UNSAT reports need checked proofs and exclude only this branch. Unknown gives no bound. No Lean.'
    (args.output_dir / (stem + '-search.json')).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()
