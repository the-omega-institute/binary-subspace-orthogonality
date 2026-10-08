"""Independently audit complete roots and all decompositions in twelve source branches."""
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
import argparse
import json

from check_dimension_seven_five_four_charge import array_cliques, digest, dot, vector_sum
from check_dimension_seven_four_five_five_charge import inherited_bindings
from check_dimension_seven_four_five_six_charge import cover_binding


def linear_table(images):
    values = [0]
    for image in images:
        values += [point ^ image for point in values]
    return tuple(values)


def reconstruct():
    even = tuple(point for point in range(1, 128) if point.bit_count() % 2 == 0)
    holes = {3, 12, 15, 48, 51, 60, 63}
    cliques = {size: array_cliques(list(even), size) for size in (4, 5, 6, 7)}
    anchored = [block for block in cliques[7] if len(set(block) & holes) == 1]
    assert len(cliques[7]) == 288 and len(anchored) == 224
    basis = (3, 12, 48, 65, 71, 95, 127)
    coordinates = {point: index for index, point in enumerate(linear_table(basis))}
    dual_choices = [[point for point in even if all(dot(point, basis[index]) == (index == role) for index in range(3))]
                    for role in range(3)]
    assert [len(choices) for choices in dual_choices] == [8, 8, 8]
    groups = {}
    controls = Counter()
    for eta, completion in ((0, 71), (1, 89)):
        group = []
        for first, second, third in product(*dual_choices):
            if dot(first, second) or dot(first, third) or dot(second, third):
                continue
            if (second if not eta else first ^ second ^ third) != completion:
                continue
            table = linear_table((3, 12, 48, first, second, third, 127))
            mapping = tuple(table[coordinates[point]] for point in range(128))
            assert all(mapping[hole] == hole for hole in holes)
            assert all(dot(left, right) == dot(mapping[left], mapping[right]) for left in range(128) for right in range(128))
            controls['full_group_dot_product_pairs'] += 128**2
            group.append(mapping)
        group.sort()
        assert len(set(group)) == 8 and tuple(range(128)) in group
        for first in group:
            for second in group:
                assert tuple(first[second[point]] for point in range(128)) in group
                controls['composition_points'] += 128
        groups[eta] = group
    expected = []
    stats = []
    for eta, completion, other in ((0, 71, 120), (1, 89, 102)):
        for charge in (15, 51, 60, 63):
            for source in ('pure', 'mixed') if eta else ('pure',):
                roles = ['D0', 'D1', 'P', 'J', 'Hq'] + (['Ht'] if source == 'pure' else [])
                catalogs = [
                    [block for block in cliques[4] if vector_sum(block) == 3 and completion not in block and other not in block
                     and all(dot(point, 3) == dot(point, charge) == 1 for point in block)],
                    [block for block in cliques[5] if vector_sum(block) ^ 12 == completion
                     and other not in block and all(dot(point, 12) for point in block)],
                    [block for block in cliques[6] if vector_sum(block) == other
                     and sum(point in holes for point in block) == 1 and completion not in block],
                    [block for block in cliques[6] if vector_sum(block) == 48 and other not in block
                     and (completion in block if source == 'mixed' else completion not in block)],
                    [block for block in anchored if other in block and completion not in block]]
                if source == 'pure':
                    catalogs.append([block for block in anchored if completion in block and other not in block])
                odd_roles = [(3, charge), (12,), (), (48,), (), ()]
                for role, catalog in enumerate(catalogs):
                    for block in catalog:
                        original = block + tuple(127 ^ odd for odd in odd_roles[role])
                        assert len(set(original)) == len(original)
                        assert all(dot(first, second) for first, second in combinations(original, 2))
                        controls['original_graph_component_pairs'] += len(original) * (len(original) - 1) // 2
                        if role == 1:
                            assert all(dot(point, completion) for point in original) and completion not in original
                            controls['recipient_mixed_completions'] += 1
                        if role == 2:
                            assert tuple(sorted(block + (other,))) in anchored
                            controls['recipient_pure_completions'] += 1
                catalog_sets = [[frozenset(block) for block in catalog] for catalog in catalogs]
                order = [2, 4] + ([5] if source == 'pure' else []) + [3, 1, 0]
                chosen = [None] * len(roles)
                families = defaultdict(list)
                remaining_size = 28 if source == 'pure' else 35
                remaining_holes = 4 if source == 'pure' else 5

                def visit(depth, used):
                    if depth == len(order):
                        remaining = tuple(point for point in even if point not in used)
                        assert len(remaining) == remaining_size and vector_sum(remaining) == 0
                        actual = [next(point for point in catalogs[role][chosen[role]] if point in holes)
                                  for role in (2, 4, 5) if role < len(roles)]
                        assert len(set(actual)) == len(actual)
                        assert set(remaining) & holes == holes - set(actual)
                        assert len(set(remaining) & holes) == remaining_holes
                        assert all(dot(point, completion) for point in actual)
                        original_classes = [catalogs[role][chosen[role]] + tuple(127 ^ odd for odd in odd_roles[role])
                                            for role in range(len(roles))]
                        assert len(set().union(*map(set, original_classes))) == 63 - remaining_size + 4
                        assert other in catalogs[4][chosen[4]]
                        assert completion in catalogs[5 if source == 'pure' else 3][chosen[5 if source == 'pure' else 3]]
                        families[remaining].append({'component_indices': tuple(chosen), 'actual_holes': actual})
                        controls['complete_family_partition_and_hole_checks'] += 1
                        return
                    role = order[depth]
                    for index, block in enumerate(catalog_sets[role]):
                        combined = used | block
                        if len(combined) == len(used) + len(block):
                            chosen[role] = index
                            visit(depth + 1, combined)

                visit(0, frozenset())
                roots = [{'remaining': str(sum(2**point for point in points)),
                          'decompositions': sorted(records, key=lambda record: record['component_indices'])}
                         for points, records in families.items()]
                roots.sort(key=lambda record: int(record['remaining']))
                points_by_index = [tuple(point for point in even if int(record['remaining']) & 2**point) for record in roots]
                index_by_points = {points: index for index, points in enumerate(points_by_index)}
                family_by_indices = {tuple(record['component_indices']): (index, record)
                                     for index, root_record in enumerate(roots) for record in root_record['decompositions']}
                assert len(family_by_indices) == sum(len(records) for records in families.values())
                group = groups[eta]
                index_by_block = [{block: index for index, block in enumerate(catalog)} for catalog in catalogs]
                orbit_by_index = {}
                stabilizers = Counter()
                family_stabilizers = Counter()
                for index, points in enumerate(points_by_index):
                    members = set()
                    fixed = 0
                    for mapping in group:
                        mapped_points = tuple(sorted(mapping[point] for point in points))
                        assert mapped_points in index_by_points
                        destination = index_by_points[mapped_points]
                        members.add(destination)
                        fixed += destination == index
                        for record in roots[index]['decompositions']:
                            mapped_indices = tuple(index_by_block[role][tuple(sorted(mapping[point] for point in catalogs[role][component]))]
                                                   for role, component in enumerate(record['component_indices']))
                            image_index, image_record = family_by_indices[mapped_indices]
                            assert image_index == destination
                            assert image_record['actual_holes'] == [mapping[point] for point in record['actual_holes']] == record['actual_holes']
                            controls['family_group_actions_with_roles_and_actual_holes'] += 1
                    assert len(members) * fixed == len(group)
                    stabilizers[fixed] += 1
                    orbit_by_index[index] = tuple(sorted(members))
                for indices in family_by_indices:
                    orbit = {tuple(index_by_block[role][tuple(sorted(mapping[point] for point in catalogs[role][component]))]
                                   for role, component in enumerate(indices)) for mapping in group}
                    fixed = sum(tuple(index_by_block[role][tuple(sorted(mapping[point] for point in catalogs[role][component]))]
                                      for role, component in enumerate(indices)) == indices for mapping in group)
                    assert len(orbit) * fixed == 8
                    family_stabilizers[fixed] += 1
                partitions = sorted(set(orbit_by_index.values()))
                assert sum(len(members) for members in partitions) == len(roots)
                orbits = [{'representative': members[0], 'members': members} for members in partitions]
                stats.append({'eta': eta, 'b': charge, 't_source': source,
                              'component_catalog_sizes': [len(catalog) for catalog in catalogs],
                              'complete_joint_families': len(family_by_indices), 'distinct_remaining_sets': len(roots),
                              'decomposition_multiplicity_histogram': dict(sorted(Counter(len(root_record['decompositions']) for root_record in roots).items())),
                              'remaining_set_orbits': len(orbits),
                              'orbit_size_histogram': dict(sorted(Counter(len(members) for members in partitions).items())),
                              'remaining_set_stabilizer_histogram': dict(sorted(stabilizers.items())),
                              'family_stabilizer_histogram': dict(sorted(family_stabilizers.items())),
                              'remaining_points': remaining_size, 'remaining_holes': remaining_holes,
                              'residual_pure_heptads_required': remaining_holes, 'full_marked_group_order': 8,
                              'families_by_ordered_actual_holes': [{'holes': pair, 'families': count}
                                  for pair, count in sorted(Counter(tuple(record['actual_holes']) for root_record in roots
                                                                  for record in root_record['decompositions']).items())]})
                expected.append({'eta': eta, 'b': charge, 't_source': source, 'component_order': roles,
                                 'component_catalogs': catalogs,
                                 'group_basis_images': [tuple(mapping[point] for point in basis) for mapping in group],
                                 'roots': roots, 'orbits': orbits})
    return expected, stats, dict(controls)


def audit_artifact(artifact, expected):
    assert artifact['status'] == 'complete_twelve_branch_joint_roots_pending_independent_audit'
    assert artifact['profile'] == [4, 5, 6, 6, 1, 8]
    assert artifact['all_component_decompositions_retained'] and not artifact['cover_search_run']
    assert 0 < artifact['visited_partial_families'] <= artifact['construction_limits']['max_visits']
    assert artifact['forms'] == json.loads(json.dumps(expected))


def check(roots_path):
    if not __debug__:
        raise RuntimeError('Run without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    artifact = json.loads(roots_path.read_text())
    expected, stats, controls = reconstruct()
    audit_artifact(artifact, expected)
    rejected = []
    for kind in ('missing_branch', 'missing_decomposition', 'wrong_actual_hole', 'missing_orbit_member'):
        invalid = dict(artifact)
        invalid['forms'] = list(artifact['forms'])
        if kind == 'missing_branch':
            invalid['forms'].pop()
        else:
            form = dict(invalid['forms'][0])
            invalid['forms'][0] = form
            if kind == 'missing_orbit_member':
                form['orbits'] = list(form['orbits'])
                form['orbits'][0] = dict(form['orbits'][0])
                form['orbits'][0]['members'] = form['orbits'][0]['members'][:-1]
            else:
                form['roots'] = list(form['roots'])
                record = dict(form['roots'][0])
                form['roots'][0] = record
                record['decompositions'] = list(record['decompositions'])
                if kind == 'missing_decomposition':
                    record['decompositions'].pop()
                else:
                    record['decompositions'][0] = dict(record['decompositions'][0])
                    actual = list(record['decompositions'][0]['actual_holes'])
                    actual[0] = actual[1]
                    record['decompositions'][0]['actual_holes'] = actual
        try:
            audit_artifact(invalid, expected)
        except AssertionError:
            rejected.append(kind)
        else:
            raise AssertionError('Invalid artifact accepted: ' + kind)
    previous_name = 'results/dimension-7-four-five-six-symmetry.json'
    previous = json.loads((root / previous_name).read_text())
    assert previous['written_exhaustive_normalization'] and previous['full_ordered_marked_groups_proved']
    assert previous['checker_sha256'] == digest(root / 'develop/check_dimension_seven_four_five_six_symmetry.py')
    assert previous['proof_note_sha256'] == digest(root / 'notes/dimension-seven-four-five-six-symmetry.md')
    for name, checksum in previous['dependency_sha256'].items():
        assert digest(root / name) == checksum, name
    inherited = inherited_bindings(root)
    inherited.update(cover_binding(root, stem) for stem in ('three-six-cover', 'four-six-six-cover'))
    assert inherited == previous['inherited_theorem_report_sha256']
    dependencies = ('develop/check_dimension_seven_four_five_six_symmetry.py',
                    'notes/dimension-seven-four-five-six-symmetry.md', previous_name,
                    'develop/check_dimension_seven_five_four_charge.py')
    return {'status': 'complete_twelve_branch_roots_and_orbits_independently_checked', 'dimension': 7,
            'profile': [4, 5, 6, 6, 1, 8], 'forms': stats, 'controls': controls,
            'all_twelve_source_branches_complete': True, 'all_component_decompositions_retained': True,
            'remaining_set_decomposition_unique': all(all(len(record['decompositions']) == 1 for record in form['roots']) for form in artifact['forms']),
            'all_roles_and_actual_holes_transported': True, 'free_group_action_assumed': False,
            'array_reconstruction_matches_bitmask_builder': True, 'rejected_invalid_controls': rejected,
            'complete_joint_families': sum(form['complete_joint_families'] for form in stats),
            'distinct_form_labelled_remaining_sets': sum(form['distinct_remaining_sets'] for form in stats),
            'complete_remaining_set_orbits': sum(form['remaining_set_orbits'] for form in stats),
            'anchored_even_heptads_for_later_cover': 224,
            'new_raw_profile_exclusions': 0, 'target_raw_profile_excluded': False,
            'remaining_raw_profiles': previous['remaining_raw_profiles'],
            'remaining_raw_profile_lists': previous['remaining_raw_profile_lists'],
            'remaining_three_six_C8_count': 2, 'remaining_C6_through_C8_count': 59, 'remaining_C5_count': 2,
            'inherited_theorem_report_sha256': inherited,
            'historical_cover_audits_rerun': False, 'previous_normalization_and_source_audits_rerun': False,
            'new_cover_search': False, 'new_cover_certificate': False, 'new_Lean': False,
            'new_independent_Pro_review': False, 'exact_n7': 'open_lower_bound19',
            'old_n6_formal_scope': 'three standard plus four native-evaluation axioms',
            'construction_limits': artifact['construction_limits'], 'visited_partial_families': artifact['visited_partial_families'],
            'roots_sha256': digest(roots_path),
            'builder_sha256': digest(root / 'develop/build_dimension_seven_four_five_six_roots.py'),
            'checker_sha256': digest(Path(__file__)),
            'proof_note_sha256': digest(root / 'notes/dimension-seven-four-five-six-roots.md'),
            'dependency_sha256': {name: digest(root / name) for name in dependencies}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--roots', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    arguments = parser.parse_args()
    report = check(arguments.roots)
    arguments.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: value for key, value in report.items() if key not in ('forms', 'remaining_raw_profile_lists')}, indent=2))
