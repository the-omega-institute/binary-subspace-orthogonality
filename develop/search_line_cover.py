"""Remove color-permutation symmetry by covering Gamma_6 with maximal independent sets."""
from collections import Counter
from pathlib import Path
from threading import Timer
import hashlib
import json
import time
import argparse

from pysat.card import CardEnc, EncType
from pysat.formula import CNF
from pysat.solvers import Solver

ROOT = Path(__file__).resolve().parents[1]
FULL = (1 << 63) - 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fix-six-class', action='store_true')
    args = parser.parse_args()
    compatible = [sum(1 << (w-1) for w in range(1,64) if w != v and (v & w).bit_count() % 2) for v in range(1,64)]
    maximal = []

    def bron_kerbosch(chosen, candidates, excluded):
        if not candidates and not excluded:
            maximal.append(chosen)
            return
        both = candidates | excluded
        pivot = max((i for i in range(63) if both >> i & 1), key=lambda i: (candidates & compatible[i]).bit_count())
        choices = candidates & ~compatible[pivot]
        while choices:
            bit = choices & -choices
            i = bit.bit_length()-1
            bron_kerbosch(chosen | bit, candidates & compatible[i], excluded & compatible[i])
            candidates ^= bit
            excluded |= bit
            choices ^= bit

    bron_kerbosch(0,FULL,0)
    fixed = [1,3,5,9,17,33] if args.fix_six_class else []
    fixed_mask = sum(1 << (v-1) for v in fixed)
    if fixed:
        # Any 12-coloring of 63 vertices has a six-vertex class. Its orthonormal
        # basis description makes all such classes equivalent under an isometry.
        candidates = set(mask & ~fixed_mask for mask in maximal)
        maximal = [mask for mask in candidates if not any(mask != other and mask & ~other == 0 for other in candidates)]
    maximal.sort()
    sets = [[v for v in range(1,64) if mask >> (v-1) & 1] for mask in maximal]
    suffix = '-fixed' if fixed else ''
    catalog = {'dimension':6, 'fixed_class':fixed, 'sets':sets, 'count':len(sets), 'size_counts':dict(sorted(Counter(map(len,sets)).items()))}
    catalog_path = ROOT / f'results/line-independent-sets{suffix}.json'
    catalog_path.write_text(json.dumps(catalog,indent=2)+'\n')
    print(json.dumps({k:v for k,v in catalog.items() if k!='sets'}),flush=True)
    k = 11 if fixed else 12
    cnf = CNF()
    for v in range(1,64):
        if v not in fixed:
            cnf.append([i+1 for i,mask in enumerate(maximal) if mask >> (v-1) & 1])
    cardinality = CardEnc.atmost(lits=list(range(1,len(sets)+1)),bound=k,encoding=EncType.seqcounter)
    cnf.extend(cardinality.clauses)
    cnf_path = ROOT / f'results/line-cover-12{suffix}.cnf'
    cnf.to_file(str(cnf_path))
    report = {'colors':12,'remaining_colors':k,'fixed_class':fixed,'variables':cnf.nv,'clauses':len(cnf.clauses),
              'catalog_sha256':hashlib.sha256(catalog_path.read_bytes()).hexdigest(),
              'cnf_sha256':hashlib.sha256(cnf_path.read_bytes()).hexdigest(),
              'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    begin=time.monotonic()
    with Solver(name='g4',bootstrap_with=cnf.clauses,with_proof=True) as solver:
        timer=Timer(90,solver.interrupt)
        timer.start()
        try:
            answer=solver.solve_limited(expect_interrupt=True)
        finally:
            timer.cancel()
        report.update(elapsed_seconds=time.monotonic()-begin,stats=solver.accum_stats())
        if answer is True:
            model=set(x for x in solver.get_model() if x>0)
            selected=[i for i in range(len(sets)) if i+1 in model]
            assert len(selected)<=k
            used=set(fixed)
            classes=[fixed] if fixed else []
            for i in selected:
                fresh=set(sets[i])-used
                if fresh:
                    classes.append(sorted(fresh)); used |= fresh
            assert used==set(range(1,64))
            (ROOT/'results/line-coloring.json').write_text(json.dumps({'dimension':6,'colors':len(classes),'classes':classes},indent=2)+'\n')
            report['status']='sat_candidate'
        elif answer is False:
            path=ROOT/f'results/line-cover-12{suffix}.drat'
            path.write_text('\n'.join(solver.get_proof())+'\n')
            report.update(status='unsat_reported_unchecked',proof_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        else:
            report['status']='unknown_time_limit'
    (ROOT/f'results/line-cover-search{suffix}.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__':
    main()
