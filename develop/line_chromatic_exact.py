"""
Determine whether Gamma_6 minus the isometry-normalized 6-class
C = {1, 3, 5, 9, 17, 33} is 11-colorable.

An independently checked SAT witness gives chi(Gamma_6) = 12.
An UNSAT report needs a separate proof check before giving equality 13.

The class C is the unique (up to isometry) independent set of size 6
in Gamma_6, by Lemma 3.1 and the isometry argument in Section 3.
"""
import argparse
import hashlib
import json
from pathlib import Path
from threading import Timer
import time

from pysat.formula import CNF
from pysat.solvers import Solver


def dot(u, v):
    return (u & v).bit_count() % 2


def build_graph():
    edges = []
    for u in range(1, 64):
        for v in range(u + 1, 64):
            if dot(u, v) == 0:
                edges.append((u, v))
    return edges


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seconds', type=float, default=60)
    args = parser.parse_args()
    if args.seconds <= 0:
        parser.error('--seconds must be positive')
    root = Path(__file__).resolve().parents[1]
    C = {1, 3, 5, 9, 17, 33}
    all_edges = build_graph()
    vertices = [v for v in range(1, 64) if v not in C]
    n = len(vertices)
    k = 11
    idx = {v: i for i, v in enumerate(vertices)}

    def var(v, c):
        return idx[v] * k + c + 1

    cnf = CNF()

    # At least one color per vertex
    for v in vertices:
        cnf.append([var(v, c) for c in range(k)])

    # At most one color per vertex
    for v in vertices:
        for c1 in range(k):
            for c2 in range(c1 + 1, k):
                cnf.append([-var(v, c1), -var(v, c2)])

    # Adjacent vertices have different colors
    for u, v in all_edges:
        if u in C or v in C:
            continue
        for c in range(k):
            cnf.append([-var(u, c), -var(v, c)])

    print(f"Variables: {cnf.nv}, Clauses: {len(cnf.clauses)}")
    print(f"Vertices: {n}, Edges in H: "
          f"{sum(1 for u, v in all_edges if u not in C and v not in C)}")

    cnf_path = root / 'results/line-chromatic-exact.cnf'
    cnf.to_file(str(cnf_path))
    report = {
        'dimension': 6, 'fixed_class': sorted(C), 'remaining_colors': k,
        'vertices': n, 'variables': cnf.nv, 'clauses': len(cnf.clauses),
        'edges_in_remaining_graph': sum(
            1 for first, second in all_edges if first not in C and second not in C),
        'solver': 'glucose4', 'seconds_limit': args.seconds,
        'cnf_sha256': hashlib.sha256(cnf_path.read_bytes()).hexdigest(),
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    start = time.monotonic()
    with Solver(name='g4', bootstrap_with=cnf.clauses, with_proof=True) as solver:
        timer = Timer(args.seconds, solver.interrupt)
        timer.start()
        try:
            result = solver.solve_limited(expect_interrupt=True)
        finally:
            timer.cancel()
        report.update(elapsed_seconds=time.monotonic() - start, stats=solver.accum_stats())
        if result is True:
            positive = {literal for literal in solver.get_model() if literal > 0}
            classes = [[vertex for vertex in vertices if var(vertex, color) in positive]
                       for color in range(k)] + [sorted(C)]
            certificate_path = root / 'results/line-coloring-12.json'
            certificate_path.write_text(json.dumps({
                'dimension': 6, 'colors': 12, 'classes': classes}, indent=2) + '\n')
            report.update(status='sat_candidate',
                          certificate='results/line-coloring-12.json',
                          certificate_sha256=hashlib.sha256(certificate_path.read_bytes()).hexdigest())
            print("Status: SAT")
            print("Candidate: 12 colors; run the independent checker")
        elif result is False:
            proof = solver.get_proof()
            proof_path = root / 'results/line-chromatic-exact.drat'
            proof_path.write_text('\n'.join(proof) + '\n')
            report.update(status='unsat_reported_unchecked', proof_lines=len(proof),
                          proof_sha256=hashlib.sha256(proof_path.read_bytes()).hexdigest())
            print("Status: UNSAT")
            print("Conclusion pending independent proof check")
            print(f"Proof lines: {len(proof)}")
        else:
            report['status'] = 'unknown_time_limit'
            print("Status: UNKNOWN (time limit); 12 <= chi(Gamma_6) <= 13")
    (root / 'results/line-chromatic-exact.json').write_text(
        json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
