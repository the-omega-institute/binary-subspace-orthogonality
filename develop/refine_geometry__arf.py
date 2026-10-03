"""
Compute the parity of the number of self-orthogonal vectors outside the
radical. This is a bilinear count, not an Arf invariant of a quadratic form.
The numerical partition omits the actual subspaces H and K; use
audit_geometry_profiles.py for a comparison retaining the exact baseline.
"""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def dot(u, v):
    return (u & v).bit_count() % 2


def span(rows):
    result = {0}
    for r in rows:
        result |= {x ^ r for x in list(result)}
    return frozenset(result)


def dim(U):
    return len(U).bit_length() - 1


def arf_invariant(U):
    """
    Return quotient dimension and self-orthogonal-count parity.
    The historical function name is retained for compatibility; no quadratic
    refinement is specified here, so this value is not an Arf invariant.
    """
    rad = frozenset(u for u in U if all(dot(u, v) == 0 for v in U))
    d_rad = dim(rad) if rad else 0
    d_U = dim(U)
    d_quot = d_U - d_rad
    if d_quot == 0:
        return (0, 0)
    # Count the number of isotropic vectors in U (not in rad)
    iso = 0
    for u in U:
        if u in rad:
            continue
        if dot(u, u) == 0:
            iso += 1
    return (d_quot, iso % 2)


def analyze(certificate_path):
    data = json.loads(certificate_path.read_text())
    records = data['subspace_colors']
    T = span([3, 12, 48])
    spaces = [span(r['basis']) for r in records]
    refined = defaultdict(set)
    for r, U in zip(records, spaces):
        if U <= T:
            continue
        H = frozenset(t for t in T if all(dot(t, u) == 0 for u in r['basis']))
        K = U & T
        UH = U & H
        KH = K & H
        arf = arf_invariant(U)
        inv = (dim(U), dim(H), dim(K), dim(UH), dim(KH), arf)
        refined[inv].add(r['color'])
    multi = {inv: cs for inv, cs in refined.items() if len(cs) > 1}
    single = {inv: cs for inv, cs in refined.items() if len(cs) == 1}
    return {
        'total_refined_profiles': len(refined),
        'single_color_profiles': len(single),
        'multi_color_profiles': len(multi),
        'first_multi_color_examples': [
            {'invariants': list(inv), 'colors': sorted(cs)}
            for inv, cs in list(multi.items())[:10]
        ],
    }


if __name__ == '__main__':
    result = analyze(ROOT / 'results/full-15-coloring.json')
    out = ROOT / 'results/refined-geometry-arf.json'
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
