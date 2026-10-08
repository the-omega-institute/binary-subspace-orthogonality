"""Build complete necessary seven-component roots for sixteen ordered pure-source forms."""
from collections import defaultdict
from pathlib import Path
from time import monotonic
import argparse
import json

from check_dimension_seven_five_four_charge import bit_cliques, dot, mask, vector_sum
from check_dimension_seven_three_six_charge import linear_values


def build(max_visits=1000000, seconds=20.0):
    if not __debug__:
        raise RuntimeError('Run without -O or PYTHONOPTIMIZE.')
    started = monotonic()
    visits = 0
    even = [point for point in range(1, 128) if not dot(point, 127)]
    holes = {3, 12, 15, 48, 51, 60, 63}
    cliques = {size: bit_cliques(even, size) for size in (4, 6, 7)}
    anchored = [block for block in cliques[7] if set(block) & holes]
    basis = (3, 12, 48, 65, 71, 95, 127)
    decoded = linear_values(basis)
    encoded = {point: bits for bits, point in enumerate(decoded)}
    forms = []
    for pattern in (1, 2, 4, 7):
        completion = decoded[pattern << 3]
        other = completion ^ 63
        group = []
        for bits in range(64):
            first, second, third, cross_first, cross_second, cross_third = [(bits >> index) & 1 for index in range(6)]
            shear = linear_values((first | cross_first << 1 | cross_second << 2,
                                   cross_first | second << 1 | cross_third << 2,
                                   cross_second | cross_third << 1 | third << 2))
            if shear[pattern]:
                continue
            group.append(tuple(decoded[(encoded[point] & 7) ^ shear[(encoded[point] >> 3) & 7]
                                        | encoded[point] & 120] for point in range(128)))
        group.sort()
        assert len(group) == 8
        for charge in (15, 51, 60, 63):
            roles = ['D0', 'J1', 'J2', 'P1', 'P2', 'H1', 'H2']
            catalogs = [
                [block for block in cliques[4] if vector_sum(block) == 3
                 and all(dot(point, 3) and dot(point, charge) for point in block)
                 and completion not in block and other not in block],
                [block for block in cliques[6] if vector_sum(block) == 12 and completion not in block and other not in block],
                [block for block in cliques[6] if vector_sum(block) == 48 and completion not in block and other not in block],
                [block for block in cliques[6] if vector_sum(block) == completion and set(block) & holes and other not in block],
                [block for block in cliques[6] if vector_sum(block) == other and set(block) & holes and completion not in block],
                [block for block in anchored if completion in block and other not in block],
                [block for block in anchored if other in block and completion not in block]]
            masks = [[mask(block) for block in catalog] for catalog in catalogs]
            order = sorted(range(len(roles)), key=lambda role: (len(catalogs[role]), role))
            chosen = [None] * len(roles)
            families = defaultdict(list)

            def visit(depth, used):
                nonlocal visits
                visits += 1
                if visits > max_visits or visits % 2048 == 0 and monotonic() - started > seconds:
                    raise RuntimeError('Bounded root construction incomplete; no complete artifact written.')
                if depth == len(roles):
                    actual = [next(iter(set(catalogs[role][chosen[role]]) & holes)) for role in (3, 4, 5, 6)]
                    families[mask(even) ^ used].append({'component_indices': tuple(chosen), 'actual_holes': actual})
                    return
                role = order[depth]
                for index, component in enumerate(masks[role]):
                    if not component & used:
                        chosen[role] = index
                        visit(depth + 1, used | component)

            visit(0, 0)
            roots = [{'remaining': str(remaining), 'decompositions': sorted(records, key=lambda record: record['component_indices'])}
                     for remaining, records in sorted(families.items())]
            remaining_index = {int(record['remaining']): index for index, record in enumerate(roots)}
            frontier = set(range(len(roots)))
            orbits = []
            while frontier:
                representative = min(frontier)
                remaining = int(roots[representative]['remaining'])
                members = sorted({remaining_index[mask(mapping[point] for point in even if remaining & 1 << point)] for mapping in group})
                assert set(members) <= frontier
                frontier.difference_update(members)
                orbits.append({'representative': representative, 'members': members})
            forms.append({'functional_values': [(pattern >> index) & 1 for index in range(3)], 'b': charge,
                          'component_order': roles, 'component_catalogs': catalogs,
                          'group_basis_images': [tuple(mapping[point] for point in basis) for mapping in group],
                          'roots': roots, 'orbits': orbits})
    return {'status': 'complete_sixteen_ordered_pure_source_roots_pending_independent_audit',
            'profile': [4, 6, 6, 5, 2, 8], 'forms': forms,
            'all_component_decompositions_retained': True, 'cover_search_run': False,
            'construction_limits': {'max_visits': max_visits, 'seconds': seconds},
            'visited_partial_families': visits}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--roots', type=Path, required=True)
    parser.add_argument('--max-visits', type=int, default=1000000)
    parser.add_argument('--seconds', type=float, default=20.0)
    arguments = parser.parse_args()
    artifact = build(arguments.max_visits, arguments.seconds)
    arguments.roots.write_text(json.dumps(artifact, separators=(',', ':')) + '\n')
    print(json.dumps({'status': artifact['status'], 'visited_partial_families': artifact['visited_partial_families'],
                      'forms': [{'functional_values': form['functional_values'], 'b': form['b'],
                                 'families': sum(len(root['decompositions']) for root in form['roots']),
                                 'remaining_sets': len(form['roots']), 'orbits': len(form['orbits'])} for form in artifact['forms']]}, indent=2))
