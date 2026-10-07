"""Construct the complete five-component roots of the transferred two-hole branch."""
from itertools import product
from pathlib import Path
import argparse
import json

from check_dimension_seven_five_four_charge import bit_cliques, dot, mask, vector_sum
from check_dimension_seven_three_six_charge import linear_values


def build():
    if not __debug__:
        raise RuntimeError('Run without -O or PYTHONOPTIMIZE.')
    even = [point for point in range(1, 128) if not dot(point, 127)]
    holes = {3, 12, 15, 48, 51, 60, 63}
    cliques = {size: bit_cliques(even, size) for size in (4, 6)}
    pure = [[block for block in cliques[6] if vector_sum(block) == total
             and len(set(block) & holes) == 1 and other not in block]
            for total, other in ((95, 96), (96, 95))]
    mixed = [[block for block in cliques[6] if vector_sum(block) == odd and total in block]
             for odd, total in ((51, 95), (60, 96))]
    decoded = linear_values((3, 12, 48, 65, 71, 95, 127))
    encoded = {point: bits for bits, point in enumerate(decoded)}
    forms = []
    for charge in (3, 15, 63):
        four = [block for block in cliques[4] if vector_sum(block) == 48
                and all(dot(point, 48) and dot(point, charge) for point in block)]
        catalogs = [four, pure[0], pure[1], mixed[0], mixed[1]]
        masks = [[mask(block) for block in catalog] for catalog in catalogs]
        roots = []
        for indices in product(*(range(len(catalog)) for catalog in catalogs)):
            used = 0
            for role, index in enumerate(indices):
                component = masks[role][index]
                if component & used:
                    break
                used |= component
            else:
                actual_holes = [next(iter(set(catalogs[role][indices[role]]) & holes)) for role in (1, 2)]
                roots.append({'component_indices': indices, 'remaining': str(mask(even) ^ used),
                              'actual_holes': actual_holes})
        roots.sort(key=lambda record: int(record['remaining']))
        remaining_index = {int(record['remaining']): index for index, record in enumerate(roots)}
        assert len(remaining_index) == len(roots)
        group = []
        for exchange in range(1 if charge == 3 else 2):
            for first, second, cross in product(range(2), repeat=3):
                shear = linear_values((first | cross << 1 | exchange << 2,
                                       cross | second << 1 | exchange << 2,
                                       exchange | exchange << 1 | exchange << 2))

                def swap(bits):
                    return ((bits & 1) << 1 | (bits & 2) >> 1 | bits & 4) if exchange else bits

                mapping = []
                for point in range(128):
                    bits = encoded[point]
                    dual = swap((bits >> 3) & 7)
                    image = swap(bits & 7) ^ shear[dual] | dual << 3 | bits & 64
                    mapping.append(decoded[image])
                group.append(tuple(mapping))
        group.sort()
        frontier = set(range(len(roots)))
        orbits = []
        while frontier:
            representative = min(frontier)
            remaining = int(roots[representative]['remaining'])
            members = sorted({remaining_index[mask(mapping[point] for point in even if remaining & (1 << point))]
                              for mapping in group})
            assert set(members) <= frontier
            frontier.difference_update(members)
            orbits.append({'representative': representative, 'members': members})
        forms.append({'b': charge, 'component_catalogs': catalogs,
                      'group_basis_images': [tuple(mapping[point] for point in (3, 12, 48, 65, 71, 95, 127))
                                             for mapping in group],
                      'roots': roots, 'orbits': orbits})
    return {'status': 'complete_necessary_five_component_roots_pending_independent_audit',
            'profile': [4, 6, 6, 5, 2, 8],
            'scope': 'Transferred two-hole subbranch only; paired pure/mixed roles and actual holes retained.',
            'component_order': ['four_even_defect', 'pure_u', 'pure_v', 'mixed_c', 'mixed_d'],
            'forms': forms, 'cover_search_run': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--roots', type=Path, required=True)
    args = parser.parse_args()
    artifact = build()
    args.roots.write_text(json.dumps(artifact, separators=(',', ':')) + '\n')
    print(json.dumps({'status': artifact['status'],
                      'forms': [{'b': form['b'], 'roots': len(form['roots']), 'orbits': len(form['orbits'])}
                                for form in artifact['forms']]}, indent=2))
