"""Describe the fixed coloring relative to T without inferring a uniform rule."""
from collections import Counter, defaultdict
from pathlib import Path
import argparse
import hashlib
import json

from check_full_coloring import dot, span

ROOT = Path(__file__).resolve().parents[1]


def analyze(certificate):
    data = json.loads(certificate.read_text())
    assert data['dimension'] == 6 and data['colors'] == 15
    records = data['subspace_colors']
    T = span([3, 12, 48])
    spaces = [span(r['basis']) for r in records]
    labels = {r['color']: U for r, U in zip(records, spaces) if U <= T}
    assert set(labels) == set(range(15))
    profiles = defaultdict(Counter)
    exact_profiles = defaultdict(set)
    classes = defaultdict(Counter)
    for r, U in zip(records, spaces):
        d, c = len(r['basis']), r['color']
        H = frozenset(t for t in T if all(dot(t, u) == 0 for u in r['basis']))
        intersection = U & T
        h, a = len(H).bit_length() - 1, len(intersection).bit_length() - 1
        classes[c][d] += 1
        if U <= T:
            assert labels[c] == U
            continue
        forbidden = {k for k, W in labels.items() if W <= H}
        assert c not in forbidden and len(forbidden) == (0, 1, 4)[h]
        profiles[d, h, a][c] += 1
        exact_profiles[d, tuple(sorted(H)), tuple(sorted(intersection))].add(c)
    return {
        'status': 'passed',
        'certificate_sha256': hashlib.sha256(certificate.read_bytes()).hexdigest(),
        'analyzer_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'clique_color_labels': [
            {'color': c, 'vectors': sorted(W), 'dimension': len(W).bit_length() - 1}
            for c, W in sorted(labels.items())],
        'profiles_outside_T': [
            {'dimension': d, 'H_dimension': h, 'intersection_dimension': a,
             'vertices': sum(counts.values()), 'color_counts': dict(sorted(counts.items()))}
            for (d, h, a), counts in sorted(profiles.items())],
        'color_classes': [
            {'color': c, 'vertices': sum(counts.values()), 'dimensions': dict(sorted(counts.items()))}
            for c, counts in sorted(classes.items())],
        'exact_geometric_profiles': len(exact_profiles),
        'exact_profiles_using_multiple_colors': sum(len(cs) > 1 for cs in exact_profiles.values()),
        'scope': 'The archived coloring is profiled by dim(U), H(U), and U intersect T. '
                 'Multiple colors in one profile describe this certificate, not an obstruction '
                 'to a different coloring determined by those invariants.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, default=ROOT / 'results/coloring-geometry.json')
    args = parser.parse_args()
    report = analyze(ROOT / 'results/full-15-coloring.json')
    args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items()
                      if k not in ('profiles_outside_T', 'color_classes', 'clique_color_labels')}, indent=2))
