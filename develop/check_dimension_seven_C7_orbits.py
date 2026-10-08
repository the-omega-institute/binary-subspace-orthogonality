"""Independently audit the full C7 hole-pair group and complete marked orbits."""
from collections import Counter, defaultdict
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import copy
import json

from check_dimension_seven_C7_equality import check as check_equality, markings_from_disjoint_pairs
from check_dimension_seven_five_four_charge import array_cliques, digest, dot, vector_sum


def group_from_second_bases(first, second):
    first_basis = (3,12,48)
    second_basis = (65,71,95)
    original = first_basis + second_basis + (127,)
    expansions = {vector_sum(original[index] for index in range(7) if bits & (1 << index)):
                  tuple(index for index in range(7) if bits & (1 << index)) for bits in range(128)}
    assert len(expansions) == 128
    maps = []
    for images in permutations(second,3):
        if len({vector_sum(images[index] for index in range(3) if bits & (1 << index)) for bits in range(8)}) != 8:
            continue
        dual = tuple(next(point for point in first if all(dot(point, image) == int(index == column) for column,image in enumerate(images))) for index in range(3))
        targets = dual + images + (127,)
        mapping = tuple(vector_sum(targets[index] for index in expansions[point]) for point in range(128))
        maps.append(mapping)
    return sorted(maps)


def mapped_record(record, mapping):
    characteristic, roles = record
    images = [(mapping[charge],mapping[partner],mapping[hole]) for charge,partner,hole in roles]
    return tuple(sorted(mapping[point] for point in characteristic)), tuple(sorted(images))


def as_record(record):
    return tuple(record[0]),tuple(tuple(role) for role in record[1])


def audit(artifact, maps, records):
    assert artifact['group_maps'] == [list(mapping) for mapping in maps]
    assert artifact['group_order'] == 168 and artifact['markings_with_distinct_actual_defect_holes'] == len(records)
    seen = set()
    histograms = {0:Counter(),1:Counter()}
    for orbit in artifact['orbits']:
        representative = as_record(orbit['representative'])
        expected = {mapped_record(representative,mapping) for mapping in maps}
        members = [as_record(record) for record in orbit['members']]
        assert members == sorted(expected) and representative == min(expected)
        assert expected <= records and not expected & seen
        case = sum(charge in (3,12,15,48,51,60,63) for charge,partner,hole in representative[1])
        assert orbit['case'] == case
        stabilizer = sum(mapped_record(representative,mapping) == representative for mapping in maps)
        assert orbit['orbit_size'] == len(expected) and orbit['stabilizer_order'] == stabilizer
        assert len(expected) * stabilizer == 168
        histograms[case][(len(expected),stabilizer)] += 1
        seen.update(expected)
    assert seen == records
    return histograms


def check(artifact_path):
    if not __debug__:
        raise RuntimeError('Run without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    previous_path = root/'results/dimension-7-C7-equality.json'
    previous = json.loads(previous_path.read_text())
    assert json.loads(json.dumps(check_equality())) == previous
    first = (3,12,15,48,51,60,63)
    second_basis = (65,71,95)
    second = tuple(sorted(vector_sum(second_basis[index] for index in range(3) if bits & (1 << index)) for bits in range(1,8)))
    holes = set(first) | set(second)
    maps = group_from_second_bases(first,second)
    assert len(maps) == len(set(maps)) == 168
    map_set = set(maps)
    gram_controls = 0
    composition_controls = 0
    for mapping in maps:
        assert set(mapping) == set(range(128)) and mapping[127] == 127
        assert {mapping[point] for point in first} == set(first)
        assert {mapping[point] for point in second} == set(second)
        for left in range(128):
            for right in range(128):
                assert dot(mapping[left],mapping[right]) == dot(left,right)
                gram_controls += 1
        for other in maps:
            composed = tuple(mapping[other[point]] for point in range(128))
            assert composed in map_set
            composition_controls += 1
    markings = markings_from_disjoint_pairs(first,second)
    assert len(markings) == 4200
    even = [point for point in range(1,128) if not dot(point,127)]
    catalogs = defaultdict(set)
    for block in array_cliques(even,4):
        actual = set(block) & holes
        if len(actual) != 1:
            continue
        even_sum = vector_sum(block)
        for side in (first,second):
            compatible = [point for point in side if all(dot(point,member) for member in block)]
            for odd_pair in combinations(compatible,2):
                charge = even_sum ^ vector_sum(odd_pair)
                assert charge in odd_pair and even_sum in odd_pair and charge != even_sum
                catalogs[(charge,even_sum,next(iter(actual)))].add(tuple(block))
    assert len(catalogs) == 168 and all(len(blocks) == 4 for blocks in catalogs.values())
    records = set()
    for characteristic,roles in markings:
        choices = [[hole for hole in sorted(holes) if (charge,partner,hole) in catalogs] for charge,partner in roles]
        for allocation in product(*choices):
            if len(set(allocation)) == 3:
                records.add((characteristic,tuple((charge,partner,hole) for (charge,partner),hole in zip(roles,allocation))))
    assert len(records) == 29232
    cases = Counter(sum(charge in first for charge,partner,hole in record[1]) for record in records)
    assert cases == {0:7056,1:22176}
    local_actions = 0
    for mapping in maps:
        for role,blocks in catalogs.items():
            image_role = tuple(mapping[point] for point in role)
            assert {tuple(sorted(mapping[point] for point in block)) for block in blocks} == catalogs[image_role]
            local_actions += len(blocks)
    artifact = json.loads(artifact_path.read_text())
    assert artifact['equality_report_sha256'] == digest(previous_path)
    assert artifact['profile'] == [4,4,4,3,5,7]
    assert artifact['ordered_hole_pair'] == [list(first),list(second)]
    assert artifact['necessary_odd_markings'] == len(markings)
    assert artifact['status'] == 'complete_ordered_hole_pair_C7_marking_orbits_pending_independent_audit'
    histograms = audit(artifact,maps,records)
    assert histograms == {0:Counter({(56,3):3,(168,1):41}),1:Counter({(168,1):132})}
    negative = []
    for kind in ('missing_orbit','wrong_actual_hole','missing_group_map','false_stabilizer_order'):
        invalid = copy.deepcopy(artifact)
        if kind == 'missing_orbit':
            invalid['orbits'].pop()
        elif kind == 'wrong_actual_hole':
            invalid['orbits'][0]['members'][0][1][0][2] = invalid['orbits'][0]['members'][0][1][0][0]
        elif kind == 'missing_group_map':
            invalid['group_maps'].pop()
        else:
            invalid['orbits'][0]['stabilizer_order'] += 1
        try:
            audit(invalid,maps,records)
        except AssertionError:
            negative.append(kind)
        else:
            raise AssertionError('Invalid orbit artifact accepted: '+kind)
    dependencies = ('develop/check_dimension_seven_C7_equality.py','notes/dimension-seven-C7-equality.md',
                    'results/dimension-7-C7-equality.json','develop/check_dimension_seven_five_four_charge.py')
    return {'status':'complete_C7_odd_marking_and_actual_defect_hole_orbits_independently_checked',
            'dimension':7,'profile':[4,4,4,3,5,7],'full_ordered_hole_pair_group_order':168,
            'independent_group_construction':'all dual bases from N images versus builder M images',
            'full_original_dot_product_controls':gram_controls,'full_group_composition_controls':composition_controls,
            'local_defect_actions_with_actual_holes':local_actions,
            'complete_odd_markings':4200,'markings_with_distinct_actual_defect_holes':29232,
            'complete_marked_orbits':len(artifact['orbits']),
            'cases':[{'case':case,'augmented_markings':cases[case],'orbits':sum(histograms[case].values()),
                      'orbit_stabilizer_histogram':[{'orbit_size':size,'stabilizer_order':stabilizer,'orbits':count}
                                                    for (size,stabilizer),count in sorted(histograms[case].items())]}
                     for case in (0,1)],
            'all_markings_and_actual_holes_retained':True,'free_group_action_assumed':False,
            'defect_charge_partner_roles_preserved':True,'equal_defect_role_permutations_only':True,
            'rejected_invalid_controls':negative,'equality_local_audit_rerun':True,
            'inherited_report_sha256':previous['inherited_report_sha256'],
            'new_raw_profile_exclusions':0,'remaining_raw_profiles':previous['remaining_raw_profiles'],
            'remaining_raw_profile_lists':previous['remaining_raw_profile_lists'],
            'remaining_C6_through_C8_count':57,'remaining_C5_count':2,'remaining_size_four_C8_count':0,
            'complete_joint_roots_constructed':False,'new_cover_search':False,'new_cover_certificate':False,
            'historical_completion_and_cover_audits_rerun':False,'new_Lean':False,'new_independent_Pro_review':False,
            'exact_n7':'open_lower_bound19','old_n6_formal_scope':'three standard plus four native-evaluation axioms',
            'artifact_sha256':digest(artifact_path),'builder_sha256':digest(root/'develop/build_dimension_seven_C7_orbits.py'),
            'checker_sha256':digest(Path(__file__)),'proof_note_sha256':digest(root/'notes/dimension-seven-C7-orbits.md'),
            'dependency_sha256':{name:digest(root/name) for name in dependencies}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--orbits',type=Path,required=True)
    parser.add_argument('--report',type=Path,required=True)
    arguments = parser.parse_args()
    report = check(arguments.orbits)
    arguments.report.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:value for key,value in report.items() if key != 'remaining_raw_profile_lists'},indent=2))
