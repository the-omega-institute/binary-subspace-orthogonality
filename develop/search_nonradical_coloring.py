"""Emit and search the nonradical-retracted fixed-clique coloring instance."""
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

from check_nonradical_retraction import dot, nonradical_target, totally_isotropic
from dimension_seven_feasibility import bases, span


ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_encoding(dimension, last_line=64):
    assert last_line in (64, 127) and (dimension == 7 or last_line == 64)
    colors = 15 if dimension == 6 else 17
    rows = bases(dimension, 3)
    retained = [vertex for vertex, basis in enumerate(rows) if len(basis) == 1 or totally_isotropic(basis)]
    spaces = {vertex: frozenset(span(rows[vertex])) for vertex in retained}
    isotropic = frozenset(span((3, 12, 48)))
    clique = [vertex for vertex in retained if spaces[vertex] <= isotropic]
    if dimension == 7:
        clique.append(next(vertex for vertex in retained if rows[vertex] == (last_line,)))
    fixed = {vertex: color for color, vertex in enumerate(clique)}
    adjacency = {vertex: set() for vertex in retained}
    for vertex, neighbor in combinations(retained, 2):
        if all(dot(left, right) == 0 for left in rows[vertex] for right in rows[neighbor]):
            adjacency[vertex].add(neighbor)
            adjacency[neighbor].add(vertex)
    assert all(neighbor in adjacency[vertex] for vertex, neighbor in combinations(clique, 2))
    palettes = {vertex: set(range(colors)) - {fixed[neighbor] for neighbor in adjacency[vertex] & fixed.keys()}
                for vertex in retained if vertex not in fixed}
    assert all(len(palette) > 1 for palette in palettes.values())
    if dimension == 7:
        assert all(16 in palette for palette in palettes.values())
        assert sum(palette == {15, 16} for palette in palettes.values()) == 7
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
    if last_line == 127:
        reference_path = ROOT / 'results/dimension-7-characteristic-clique.json'
        reference = json.loads(reference_path.read_text())
        counts = reference['alternative_instance']
        assert (len(core), edges, len(variables), len(clauses)) == (
            counts['vertices'], counts['edges'], counts['variables'], counts['clauses'])
    else:
        reference_path = ROOT / f'results/dimension-{dimension}-nonradical-retraction.json'
        reference = json.loads(reference_path.read_text())['coloring_instances'][-1]
        assert reference['target_colors'] == colors
        assert (len(core), edges, len(variables), len(clauses)) == (
            reference['uncolored_vertices'], reference['uncolored_edges'], reference['variables'], reference['pairwise_clauses'])
    assert dict(Counter(len(palette) for palette in palettes.values())) == {
        int(size): count for size, count in reference['palette_sizes'].items()}
    control = None
    if dimension == 6:
        source = ROOT / 'results/full-15-coloring.json'
        previous = {frozenset(span(record['basis'])): record['color']
                    for record in json.loads(source.read_text())['subspace_colors']}
        relabel = {previous[spaces[vertex]]: color for vertex, color in fixed.items()}
        assignment = {variables[vertex, relabel[previous[spaces[vertex]]]] for vertex in core}
        assert all(any((literal in assignment) if literal > 0 else (-literal not in assignment)
                       for literal in clause) for clause in clauses)
        control = {'status': 'existing_n6_witness_satisfies_all_nonradical_encoding_clauses',
                   'certificate_sha256': digest(source), 'old_full_graph_coloring_rerun': False}
    report = {'dimension': dimension, 'target_colors': colors, 'retained_vertices': len(retained),
              'fixed_last_line_basis': [last_line] if dimension == 7 else None,
              'fixed_clique_vertices': len(clique), 'extra_preassigned_vertices': 0,
              'core_vertices': len(core), 'core_edges': edges, 'variables': len(variables), 'clauses': len(clauses),
              'palette_sizes': reference['palette_sizes'], 'n6_control': control,
              'nonradical_report_sha256': digest(reference_path), 'search_sha256': digest(Path(__file__)),
              'retraction_sha256': digest(ROOT / 'develop/check_nonradical_retraction.py'),
              'basis_enumerator_sha256': digest(ROOT / 'develop/dimension_seven_feasibility.py')}
    return rows, spaces, adjacency, fixed, palettes, variables, CNF(from_clauses=clauses), report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dimension', type=int, choices=(6, 7), default=7)
    parser.add_argument('--last-line', type=int, choices=(64, 127), default=64)
    parser.add_argument('--seconds', type=float, default=120)
    parser.add_argument('--encode-only', action='store_true')
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    if args.dimension == 6 and args.last_line != 64:
        parser.error('--last-line 127 applies only to dimension seven')
    assert args.seconds > 0
    args.output_dir.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    rows, spaces, adjacency, fixed, palettes, variables, cnf, report = build_encoding(args.dimension, args.last_line)
    stem = f'dimension-{args.dimension}-{report["target_colors"]}-nonradical'
    if args.last_line == 127:
        stem += '-characteristic'
    cnf_path = args.output_dir / (stem + '.cnf')
    cnf.to_file(str(cnf_path))
    report.update(cnf_sha256=digest(cnf_path), encoding_seconds=time.monotonic() - started,
                  python_sat_version=version('python-sat'), solver_run=not args.encode_only, lean_run=False)
    print(json.dumps({'event': 'encoded', **report}), flush=True)
    if args.encode_only:
        report['status'] = 'encoding_emitted_no_solver_run'
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
                coloring = dict(fixed)
                for vertex, palette in palettes.items():
                    picked = [color for color in palette if variables[vertex, color] in model]
                    assert len(picked) == 1
                    coloring[vertex] = picked[0]
                assert all(coloring[vertex] != coloring[neighbor] for vertex in coloring for neighbor in adjacency[vertex])
                retained_colors = {space: coloring[vertex] for vertex, space in spaces.items()}
                candidate = {'dimension': args.dimension, 'colors': report['target_colors'],
                             'subspace_colors': [{'basis': basis, 'color': retained_colors[frozenset(span(nonradical_target(basis)))]}
                                                for basis in bases(args.dimension, args.dimension)],
                             'cnf_sha256': report['cnf_sha256']}
                path = args.output_dir / (stem + '-candidate.json')
                path.write_text(json.dumps(candidate, indent=2) + '\n')
                report.update(status='sat_candidate_requires_independent_original_graph_check', candidate_sha256=digest(path))
            elif solved is False:
                proof = solver.get_proof()
                path = args.output_dir / (stem + '.drat')
                path.write_text('\n'.join(proof) + '\n')
                report.update(status='unsat_reported_proof_not_checked', proof_sha256=digest(path), proof_lines=len(proof))
            else:
                report['status'] = 'unknown_time_limit'
    report.update(total_seconds=time.monotonic() - started,
                  scope='Fixed-clique encoding with no additional preassignment. SAT candidates require independent original-graph validation; UNSAT solver reports require checked proofs; timeout proves nothing. No Lean.')
    (args.output_dir / (stem + '-search.json')).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()
