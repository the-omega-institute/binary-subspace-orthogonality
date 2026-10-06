"""Encode the retracted list instance and perform a bounded SAT attempt."""
from collections import Counter
from importlib.metadata import version
from itertools import combinations
from pathlib import Path
from threading import Timer
import argparse
import hashlib
import json
import time

from pysat.formula import CNF
from pysat.solvers import Solver

from check_subspace_retraction import dot, target_basis
from dimension_seven_feasibility import bases, span


ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_encoding(dimension):
    rows = bases(dimension, 3)
    retained = [vertex for vertex, basis in enumerate(rows)
                if len(basis) == 1
                or (len(basis) == 2 and all(dot(row, row) == 0 for row in basis))
                or all(dot(left, right) == 0 for left in basis for right in basis)]
    spaces = {vertex: frozenset(span(rows[vertex])) for vertex in retained}
    isotropic = frozenset(span((3, 12, 48)))
    clique = [vertex for vertex in retained if spaces[vertex] <= isotropic]
    if dimension == 7:
        clique.append(next(vertex for vertex in retained if rows[vertex] == (64,)))
    fixed = dict((vertex, color) for color, vertex in enumerate(clique))
    adjacency = {vertex: set() for vertex in retained}
    for vertex, neighbor in combinations(retained, 2):
        if all(dot(left, right) == 0 for left in rows[vertex] for right in rows[neighbor]):
            adjacency[vertex].add(neighbor)
            adjacency[neighbor].add(vertex)
    assert all(neighbor in adjacency[vertex] for vertex, neighbor in combinations(clique, 2))
    palettes = {vertex: set(range(len(clique))) - {fixed[neighbor] for neighbor in adjacency[vertex] & fixed.keys()}
                for vertex in retained if vertex not in fixed}
    forced = {vertex: next(iter(palette)) for vertex, palette in palettes.items() if len(palette) == 1}
    assert len(forced) == (7 if dimension == 7 else 0)
    assert all(color == 15 for color in forced.values())
    fixed.update(forced)
    for vertex in forced:
        palettes.pop(vertex)
    for vertex, palette in palettes.items():
        palette.difference_update(fixed[neighbor] for neighbor in adjacency[vertex] & forced.keys())
        assert palette
        intersection = {vector for vector in isotropic if all(dot(vector, row) == 0 for row in rows[vertex])}
        geometric = {color for color, neighbor in enumerate(clique[:15])
                     if not spaces[neighbor] <= intersection}
        if dimension == 7 and 64 in {left ^ right for left in spaces[vertex] for right in isotropic}:
            geometric.add(15)
        assert palette == geometric
    assert all(fixed[vertex] != fixed[neighbor] for vertex in fixed for neighbor in adjacency[vertex] & fixed.keys())
    core = sorted(palettes)
    variables = {(vertex, color): identifier + 1 for identifier, (vertex, color) in enumerate(
        (vertex, color) for vertex in core for color in sorted(palettes[vertex]))}
    clauses = []
    for vertex in core:
        choices = [variables[vertex, color] for color in sorted(palettes[vertex])]
        clauses.append(choices)
        clauses.extend([-first, -second] for first, second in combinations(choices, 2))
    edges = 0
    for vertex in core:
        for neighbor in sorted(adjacency[vertex] & palettes.keys()):
            if neighbor < vertex:
                edges += 1
                clauses.extend([-variables[vertex, color], -variables[neighbor, color]]
                               for color in sorted(palettes[vertex] & palettes[neighbor]))
    expected = (890, 33978, 11558, 426406) if dimension == 7 else (218, 3450, 2614, 47414)
    assert (len(core), edges, len(variables), len(clauses)) == expected
    old_report = json.loads((ROOT / f'results/dimension-{dimension}-retraction.json').read_text())
    assert old_report['uncolored_core'] == dict(zip(('vertices', 'edges', 'variables', 'clauses'), expected))
    assert len(retained) == old_report['retained_vertices']
    assert sum(map(len, adjacency.values())) // 2 == old_report['retained_edges']
    assert dict(Counter(len(palettes[vertex]) for vertex in core)) == {
        int(size): count for size, count in old_report['core_palette_sizes'].items()}
    control = None
    if dimension == 6:
        source = ROOT / 'results/full-15-coloring.json'
        previous = {frozenset(span(record['basis'])): record['color']
                    for record in json.loads(source.read_text())['subspace_colors']}
        relabel = {previous[spaces[vertex]]: color for vertex, color in fixed.items()}
        assignment = {variables[vertex, relabel[previous[spaces[vertex]]]] for vertex in core}
        assert all(any((literal in assignment) if literal > 0 else (-literal not in assignment)
                       for literal in clause) for clause in clauses)
        control = {'status': 'existing_n6_witness_satisfies_every_retracted_clause',
                   'certificate_sha256': digest(source), 'full_graph_rerun': False}
    report = {'dimension': dimension, 'target_colors': len(clique), 'retained_vertices': len(retained),
              'retained_edges': sum(map(len, adjacency.values())) // 2, 'fixed_clique_vertices': len(clique),
              'extra_forced_vertices': len(forced), 'core': old_report['uncolored_core'],
              'palette_sizes': old_report['core_palette_sizes'], 'direct_basis_adjacency': True,
              'geometric_lists_checked': len(core), 'previous_counts_match': True,
              'n6_control': control, 'retraction_report_sha256': digest(ROOT / f'results/dimension-{dimension}-retraction.json'),
              'search_sha256': digest(Path(__file__)),
              'basis_enumerator_sha256': digest(ROOT / 'develop/dimension_seven_feasibility.py'),
              'retraction_sha256': digest(ROOT / 'develop/check_subspace_retraction.py')}
    return rows, spaces, adjacency, fixed, palettes, variables, CNF(from_clauses=clauses), report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dimension', type=int, choices=(6, 7), default=7)
    parser.add_argument('--seconds', type=float, default=120)
    parser.add_argument('--encode-only', action='store_true')
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    assert args.seconds > 0
    args.output_dir.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    rows, spaces, adjacency, fixed, palettes, variables, cnf, report = build_encoding(args.dimension)
    cnf_path = args.output_dir / f'dimension-{args.dimension}-retracted.cnf'
    cnf.to_file(str(cnf_path))
    report.update(cnf_sha256=digest(cnf_path), encoding_seconds=time.monotonic() - started,
                  python_sat_version=version('python-sat'), solver_run=not args.encode_only, lean_run=False)
    print(json.dumps({'event': 'encoding_checked', **report}), flush=True)
    if args.encode_only:
        report['status'] = 'encoding_checked_no_solver_run'
    else:
        report.update(solver='Glucose4', time_limit_seconds=args.seconds)
        with Solver(name='g4', bootstrap_with=cnf.clauses, with_proof=True) as solver:
            solver_started = time.monotonic()
            timer = Timer(args.seconds, solver.interrupt)
            timer.start()
            try:
                solved = solver.solve_limited(expect_interrupt=True)
            finally:
                timer.cancel()
            report.update(solver_seconds=time.monotonic() - solver_started, stats=solver.accum_stats())
            if solved is True:
                model = {literal for literal in solver.get_model() if literal > 0}
                colors = dict(fixed)
                for vertex, palette in palettes.items():
                    picked = [color for color in palette if variables[vertex, color] in model]
                    assert len(picked) == 1
                    colors[vertex] = picked[0]
                assert all(colors[vertex] != colors[neighbor] for vertex in colors for neighbor in adjacency[vertex])
                retained_colors = {space: colors[vertex] for vertex, space in spaces.items()}
                candidate = {'dimension': args.dimension, 'colors': report['target_colors'],
                             'subspace_colors': [{'basis': basis, 'color': retained_colors[frozenset(span(target_basis(basis)))]}
                                                for basis in bases(args.dimension, args.dimension)],
                             'cnf_sha256': report['cnf_sha256']}
                candidate_path = args.output_dir / f'dimension-{args.dimension}-candidate.json'
                candidate_path.write_text(json.dumps(candidate, indent=2) + '\n')
                report.update(status='sat_candidate_independent_full_check_required', candidate_sha256=digest(candidate_path))
            elif solved is False:
                proof = solver.get_proof()
                proof_path = args.output_dir / f'dimension-{args.dimension}-retracted.drat'
                proof_path.write_text('\n'.join(proof) + '\n')
                report.update(status='unsat_reported_proof_not_checked', proof_sha256=digest(proof_path), proof_lines=len(proof))
            else:
                report['status'] = 'unknown_time_limit'
    report['total_seconds'] = time.monotonic() - started
    report['scope'] = 'Exact list encoding and bounded solver attempt. A timeout proves nothing; SAT requires an independent original-graph check; UNSAT requires a checked proof. No Lean run.'
    report_path = args.output_dir / f'dimension-{args.dimension}-retracted-search.json'
    report_path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()
