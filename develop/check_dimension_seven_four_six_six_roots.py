"""Independently reconstruct and audit complete transferred two-hole covering roots."""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import argparse
import copy
import json

from check_dimension_seven_five_four_charge import array_cliques, digest, dot, vector_sum


def linear_table(images):
    values = [0]
    for image in images:
        values += [point ^ image for point in values]
    return tuple(values)


def reconstruct():
    even = tuple(point for point in range(1, 128) if point.bit_count() % 2 == 0)
    holes = {3, 12, 15, 48, 51, 60, 63}
    cliques = {size: array_cliques(list(even), size) for size in (4, 6, 7)}
    assert len(cliques[7]) == 288
    anchored = tuple(block for block in cliques[7] if len(set(block) & holes) == 1)
    assert len(anchored) == 224
    pure = [[block for block in cliques[6] if vector_sum(block) == total
             and sum(point in holes for point in block) == 1 and other not in block]
            for total, other in ((95, 96), (96, 95))]
    mixed = [[block for block in cliques[6] if vector_sum(block) == odd and completion in block]
             for odd, completion in ((51, 95), (60, 96))]
    assert [len(catalog) for catalog in pure + mixed] == [18, 18, 6, 6]
    basis = (3, 12, 48, 65, 71, 95, 127)
    coordinates = {point: index for index, point in enumerate(linear_table(basis))}
    expected = []
    stats = []
    controls = Counter()
    for charge, expected_count in ((3, 1708), (15, 1648), (63, 304)):
        four = [block for block in cliques[4] if vector_sum(block) == 48
                and all(dot(point, 48) == dot(point, charge) == 1 for point in block)]
        catalogs = [four, pure[0], pure[1], mixed[0], mixed[1]]
        assert len(four) == 16
        catalog_sets = [[frozenset(block) for block in catalog] for catalog in catalogs]
        families = {}
        for first_mixed, second_mixed in product(range(6), repeat=2):
            used_mixed = catalog_sets[3][first_mixed] | catalog_sets[4][second_mixed]
            if len(used_mixed) != 12:
                continue
            for defect in range(16):
                used_defect = used_mixed | catalog_sets[0][defect]
                if len(used_defect) != 16:
                    continue
                for first_pure in range(18):
                    used_first = used_defect | catalog_sets[1][first_pure]
                    if len(used_first) != 22:
                        continue
                    for second_pure in range(18):
                        used = used_first | catalog_sets[2][second_pure]
                        if len(used) != 28:
                            continue
                        remaining = tuple(point for point in even if point not in used)
                        assert len(remaining) == 35 and vector_sum(remaining) == 0
                        indices = (defect, first_pure, second_pure, first_mixed, second_mixed)
                        actual = [next(point for point in catalogs[role][indices[role]] if point in holes) for role in (1, 2)]
                        assert actual[0] != actual[1] and len(set(remaining) & holes) == 5
                        assert set(remaining) & holes == holes - set(actual)
                        assert remaining not in families
                        families[remaining] = {'component_indices': indices, 'actual_holes': actual}
                        original_classes = [four[defect] + (127 ^ 48, 127 ^ charge),
                                            pure[0][first_pure], pure[1][second_pure],
                                            mixed[0][first_mixed] + (127 ^ 51,),
                                            mixed[1][second_mixed] + (127 ^ 60,)]
                        for block in original_classes:
                            assert all(dot(first, second) for first, second in combinations(block, 2))
                            controls['original_graph_component_pair_checks'] += len(block) * (len(block) - 1) // 2
                        assert len(set().union(*(set(block) for block in original_classes))) == 32
                        for role, completion in ((1, 95), (2, 96)):
                            assert tuple(sorted(catalogs[role][indices[role]] + (completion,))) in anchored
                        controls['reversed_pure_source_heptads'] += 2
        assert len(families) == expected_count
        roots = [{'component_indices': record['component_indices'],
                  'remaining': str(sum(2**point for point in remaining)),
                  'actual_holes': record['actual_holes']}
                 for remaining, record in families.items()]
        roots.sort(key=lambda record: int(record['remaining']))
        points_by_index = [tuple(point for point in even if int(record['remaining']) & 2**point) for record in roots]
        index_by_points = {points: index for index, points in enumerate(points_by_index)}
        group = []
        for exchange in range(1 if charge == 3 else 2):
            for first, second, cross in product(range(2), repeat=3):
                if exchange:
                    images = (12, 3, 48, 71 ^ (3 * cross) ^ (12 * second) ^ 48,
                              65 ^ (3 * first) ^ (12 * cross) ^ 48, 96, 127)
                else:
                    images = (3, 12, 48, 65 ^ (3 * first) ^ (12 * cross),
                              71 ^ (3 * cross) ^ (12 * second), 95, 127)
                table = linear_table(images)
                group.append(tuple(table[coordinates[point]] for point in range(128)))
        group.sort()
        assert len(set(group)) == (8 if charge == 3 else 16)
        group_set = set(group)
        for mapping in group:
            assert all(dot(first, second) == dot(mapping[first], mapping[second])
                       for first in range(128) for second in range(128))
            controls['full_dot_product_checks'] += 128**2
            assert mapping[48] == 48 and mapping[charge] == charge and mapping[127] == 127
            for following in group:
                assert tuple(mapping[following[point]] for point in range(128)) in group_set
                controls['composition_point_checks'] += 128
        orbit_by_index = {}
        stabilizers = Counter()
        for index, points in enumerate(points_by_index):
            record = roots[index]
            blocks = [catalogs[role][entry] for role, entry in enumerate(record['component_indices'])]
            members = set()
            fixed = 0
            for mapping in group:
                image_points = tuple(sorted(mapping[point] for point in points))
                assert image_points in index_by_points
                destination = index_by_points[image_points]
                members.add(destination)
                exchanged = mapping[95] == 96
                image_blocks = [tuple(sorted(mapping[point] for point in block)) for block in blocks]
                if exchanged:
                    image_blocks[1], image_blocks[2] = image_blocks[2], image_blocks[1]
                    image_blocks[3], image_blocks[4] = image_blocks[4], image_blocks[3]
                image_indices = tuple(catalogs[role].index(block) for role, block in enumerate(image_blocks))
                assert image_indices == tuple(roots[destination]['component_indices'])
                image_holes = [mapping[point] for point in record['actual_holes']]
                if exchanged:
                    image_holes.reverse()
                assert image_holes == roots[destination]['actual_holes']
                controls['root_actions_with_all_roles_and_actual_holes'] += 1
                fixed += destination == index
            assert len(members) * fixed == len(group)
            orbit_by_index[index] = tuple(sorted(members))
            stabilizers[fixed] += 1
        partitions = sorted(set(orbit_by_index.values()))
        assert sum(len(members) for members in partitions) == len(roots)
        orbits = [{'representative': members[0], 'members': members} for members in partitions]
        row = {'b': charge, 'complete_joint_families': len(roots), 'distinct_35_point_remaining_sets': len(roots),
               'decompositions_per_remaining_set': 1, 'full_marked_group_order': len(group),
               'remaining_set_orbits': len(orbits),
               'orbit_size_counts': dict(sorted(Counter(len(members) for members in partitions).items())),
               'root_stabilizer_size_counts': dict(sorted(stabilizers.items())),
               'families_by_ordered_actual_holes': [{'holes': pair, 'families': count}
                    for pair, count in sorted(Counter(tuple(record['actual_holes']) for record in roots).items())],
               'representatives_by_unordered_actual_holes': [{'holes': pair, 'representatives': count}
                    for pair, count in sorted(Counter(tuple(sorted(roots[orbit['representative']]['actual_holes'])) for orbit in orbits).items())]}
        stats.append(row)
        expected.append({'b': charge, 'component_catalogs': catalogs,
                         'group_basis_images': [tuple(mapping[point] for point in basis) for mapping in group],
                         'roots': roots, 'orbits': orbits})
    return expected, stats, dict(controls)


def audit_artifact(artifact, expected):
    assert artifact['status'] == 'complete_necessary_five_component_roots_pending_independent_audit'
    assert artifact['profile'] == [4, 6, 6, 5, 2, 8]
    assert artifact['scope'] == 'Transferred two-hole subbranch only; paired pure/mixed roles and actual holes retained.'
    assert artifact['component_order'] == ['four_even_defect', 'pure_u', 'pure_v', 'mixed_c', 'mixed_d']
    assert artifact['cover_search_run'] is False
    assert artifact['forms'] == json.loads(json.dumps(expected))


def check(roots_path=None):
    if not __debug__:
        raise RuntimeError('Run without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    source = roots_path or root / 'results/dimension-7-four-six-six-roots.json'
    artifact = json.loads(source.read_text())
    expected, stats, controls = reconstruct()
    audit_artifact(artifact, expected)
    negative_controls = []
    for kind in ('missing_root', 'changed_component', 'wrong_actual_holes', 'missing_orbit_member'):
        invalid = copy.deepcopy(artifact)
        form = invalid['forms'][0]
        if kind == 'missing_root':
            form['roots'].pop()
        elif kind == 'changed_component':
            form['roots'][0]['component_indices'][0] = (form['roots'][0]['component_indices'][0] + 1) % 16
        elif kind == 'wrong_actual_holes':
            form['roots'][0]['actual_holes'][0] = form['roots'][0]['actual_holes'][1]
        else:
            form['orbits'][0]['members'].pop()
        try:
            audit_artifact(invalid, expected)
        except AssertionError:
            negative_controls.append(kind)
        else:
            raise AssertionError('Invalid artifact accepted: ' + kind)
    prior_path = root / 'results/dimension-7-four-six-six-two-hole.json'
    previous = json.loads(prior_path.read_text())
    assert previous['written_exhaustive_normalization'] and previous['full_marked_groups_proved']
    assert previous['checker_sha256'] == digest(root / 'develop/check_dimension_seven_four_six_six_two_hole.py')
    assert previous['proof_note_sha256'] == digest(root / 'notes/dimension-seven-four-six-six-two-hole.md')
    for name, checksum in previous['dependency_sha256'].items():
        assert digest(root / name) == checksum
    for name, checksum in previous['inherited_theorem_report_sha256'].items():
        assert digest(root / name) == checksum
    dependencies = ('develop/build_dimension_seven_four_six_six_roots.py',
                    'develop/check_dimension_seven_four_six_six_two_hole.py',
                    'notes/dimension-seven-four-six-six-two-hole.md', 'results/dimension-7-four-six-six-two-hole.json')
    return {'status': 'complete_transferred_two_hole_five_component_roots_independently_checked',
            'dimension': 7, 'profile': [4, 6, 6, 5, 2, 8], 'source_profile': [4, 5, 5, 7, 0, 8],
            'scope': artifact['scope'], 'forms': stats, 'controls': controls,
            'all_five_component_families_complete': True, 'remaining_set_decomposition_unique': True,
            'paired_roles_and_actual_holes_transported': True, 'free_group_action_assumed': False,
            'array_reconstruction_matches_bitmask_builder': True, 'rejected_invalid_controls': negative_controls,
            'residual_points': 35, 'residual_holes': 5, 'residual_pure_heptads_required': 5,
            'all_even_heptads': 288, 'anchored_heptads': 224,
            'cover_search_run': False, 'new_cover_certificate': False, 'new_raw_profile_exclusions': 0,
            'target_raw_profile_excluded': False, 'source_raw_profile_excluded': False,
            'remaining_raw_profiles': previous['remaining_raw_profiles'],
            'remaining_raw_profile_lists': previous['remaining_raw_profile_lists'],
            'remaining_three_six_C8_count': 3, 'exact_n7': 'open_lower_bound19',
            'new_Lean': False, 'new_independent_Pro_review': False,
            'old_n6_formal_scope': 'three standard plus four native-evaluation axioms',
            'historical_cover_audits_rerun': False, 'previous_local_control_audit_rerun': False,
            'inherited_theorem_report_sha256': previous['inherited_theorem_report_sha256'],
            'inherited_geometry_report_sha256': digest(prior_path),
            'roots_sha256': digest(source), 'checker_sha256': digest(Path(__file__)),
            'proof_note_sha256': digest(root / 'notes/dimension-seven-four-six-six-roots.md'),
            'dependency_sha256': {name: digest(root / name) for name in dependencies}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--roots', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = check(args.roots)
    output = json.dumps(report, indent=2) + '\n'
    if args.report:
        args.report.write_text(output)
    print(output, end='')
