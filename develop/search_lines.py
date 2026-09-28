"""Bounded searches for Gamma_6; an UNSAT solver report requires a separate proof check."""
from itertools import combinations
from pathlib import Path
from threading import Timer
import hashlib
import json
import time

from pysat.formula import CNF
from pysat.solvers import Solver

ROOT = Path(__file__).resolve().parents[1]


def main():
    edges = [(u, v) for u, v in combinations(range(1, 64), 2) if (u & v).bit_count() % 2 == 0]
    clique = [3, 12, 15, 48, 51, 60, 63]
    records = []
    for k in range(7, 15):
        var = lambda v, c: (v - 1) * k + c + 1
        cnf = CNF()
        for v in range(1, 64):
            cnf.append([var(v, c) for c in range(k)])
            for c, d in combinations(range(k), 2):
                cnf.append([-var(v, c), -var(v, d)])
        for u, v in edges:
            for c in range(k):
                cnf.append([-var(u, c), -var(v, c)])
        for c, v in enumerate(clique):
            cnf.append([var(v, c)])
        path = ROOT / f'results/lines-{k}.cnf'
        cnf.to_file(str(path))
        begin = time.monotonic()
        with Solver(name='g4', bootstrap_with=cnf.clauses, with_proof=True) as solver:
            timer = Timer(15, solver.interrupt)
            timer.start()
            try:
                answer = solver.solve_limited(expect_interrupt=True)
            finally:
                timer.cancel()
            record = {'colors': k, 'elapsed_seconds': time.monotonic()-begin, 'cnf_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                      'variables': cnf.nv, 'clauses': len(cnf.clauses), 'stats': solver.accum_stats()}
            if answer is True:
                positive = set(x for x in solver.get_model() if x > 0)
                classes = [[v for v in range(1, 64) if var(v, c) in positive] for c in range(k)]
                out = ROOT / 'results/line-coloring.json'
                out.write_text(json.dumps({'dimension':6, 'colors':k, 'classes':classes}, indent=2)+'\n')
                record['status'] = 'sat_candidate'
            elif answer is False:
                proof = ROOT / f'results/lines-{k}.drat'
                proof.write_text('\n'.join(solver.get_proof())+'\n')
                record.update(status='unsat_reported_unchecked', proof_sha256=hashlib.sha256(proof.read_bytes()).hexdigest())
            else:
                record['status'] = 'unknown_time_limit'
        records.append(record)
        print(json.dumps(record), flush=True)
        (ROOT / 'results/line-search.json').write_text(json.dumps(records, indent=2)+'\n')
        if answer is True:
            break


if __name__ == '__main__':
    main()
