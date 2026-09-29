"""Translate the fixed JSON witness into Lean data, with extension witnesses.

The generated tables are untrusted inputs to Certificate.lean. In particular,
Lean checks closure under adjoining every vector to establish coverage without
trusting this generator's Gaussian counts or the Python enumeration.
"""
from pathlib import Path
import hashlib
import json

from check_full_coloring import span, dot

ROOT = Path(__file__).resolve().parents[1]


def csv(values):
    return ','.join(map(str, values))


def main():
    source = ROOT / 'results/full-15-coloring.json'
    data = json.loads(source.read_text())
    assert data['dimension'] == 6 and data['colors'] == 15
    records = [{'basis': [], 'color': 0}] + data['subspace_colors']
    spaces = [span(r['basis']) for r in records]
    lookup = {U: i for i, U in enumerate(spaces)}
    assert len(lookup) == len(spaces) == 2825
    masks = [sum(1 << x for x in U) for U in spaces]
    perps = [sum(1 << v for v in range(64) if all(dot(u, v) == 0 for u in r['basis']))
             for r in records]
    extensions = [lookup[U | {x ^ v for x in U}] for U in spaces for v in range(64)]
    T = span([3, 12, 48])
    clique = [i for i, U in enumerate(spaces) if i and U <= T]
    assert len(clique) == 15
    header = '\n'.join([
        'import Certificate', '',
        '/- Generated from results/full-15-coloring.json. Regenerate with',
        '   python3 develop/export_lean_coloring.py. All tables are checked inputs. -/',
        'namespace BinaryOrthogonality', '',
        'def parseNats (s : String) : Array Nat :=',
        '  (s.splitOn ",").toArray.map String.toNat!', '',
    ])
    arrays = {'masks': masks, 'perps': perps,
              'colors': [r['color'] for r in records], 'extensions': extensions,
              'cliqueIndices': clique}
    text = header + '\n'.join(f'def {name} : Array Nat := parseNats "{csv(values)}"\n'
                              for name, values in arrays.items())
    text += '\n'.join([
        '\ndef dimensionSix : Catalogue where',
        '  count := 2825', '  positive := by decide',
        '  masks := masks', '  perps := perps', '  colors := colors',
        '  extensions := extensions', '', 'end BinaryOrthogonality', '',
    ])
    target = ROOT / 'formal/Chromatic/Data.lean'
    target.write_text(text)
    report = {'certificate_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'generator_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'lean_data_sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
              'catalogue_entries_including_zero': len(spaces),
              'extension_witnesses': len(extensions), 'clique_indices': clique,
              'scope': 'Deterministic data export; Lean checks are recorded separately.'}
    (ROOT / 'results/lean-export.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
