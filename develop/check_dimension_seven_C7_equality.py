"""Audit equality-case odd markings and local hole catalogs for (4,4,4;3,5,7)."""
from collections import Counter, defaultdict
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import hashlib
import json

from check_dimension_seven_five_four_charge import array_cliques, bit_cliques, digest, dot, vector_sum


def markings_from_charge_splits(first, second):
    records = set()
    for characteristic in combinations(first, 3):
        if vector_sum(characteristic):
            continue
        for charges in combinations(second, 3):
            if vector_sum(charges):
                continue
            for partners in permutations(sorted(set(second) - set(charges)), 3):
                roles = tuple(sorted(zip(charges, partners)))
                records.add((characteristic, roles))
    for characteristic_first in combinations(first, 2):
        charge_first = vector_sum(characteristic_first)
        for characteristic_second in second:
            if any(dot(point, characteristic_second) for point in characteristic_first):
                continue
            characteristic = tuple(sorted(characteristic_first + (characteristic_second,)))
            for partner_first in sorted(set(first) - set(characteristic_first) - {charge_first}):
                for charges_second in combinations(sorted(set(second) - {characteristic_second}), 2):
                    if vector_sum(charges_second) != characteristic_second:
                        continue
                    for partners_second in permutations(sorted(set(second) - set(charges_second) - {characteristic_second}), 2):
                        roles = tuple(sorted(((charge_first, partner_first),) + tuple(zip(charges_second, partners_second))))
                        records.add((characteristic, roles))
    return records


def markings_from_disjoint_pairs(first, second):
    first_set = set(first)
    second_set = set(second)
    holes = first_set | second_set
    pairs = [pair for side in (first, second) for pair in combinations(side, 2)]
    records = set()
    for characteristic in combinations(sorted(holes), 3):
        if sum(point in first_set for point in characteristic) not in (2, 3):
            continue
        if any(dot(left, right) for left, right in combinations(characteristic, 2)):
            continue
        available = [pair for pair in pairs if not set(pair) & set(characteristic)]
        for selected in combinations(available, 3):
            if len(set().union(*map(set, selected))) != 6:
                continue
            first_roles = sum(pair[0] in first_set for pair in selected)
            if first_roles != 3 - sum(point in first_set for point in characteristic):
                continue
            for orientations in product((0, 1), repeat=3):
                roles = tuple(sorted((pair[orientation], pair[1 - orientation]) for pair, orientation in zip(selected, orientations)))
                if vector_sum(role[0] for role in roles) != vector_sum(characteristic):
                    continue
                if sum(dot(left[0], right[0]) for left, right in combinations(roles, 2)) % 2:
                    continue
                records.add((characteristic, roles))
    return records


def check():
    if not __debug__:
        raise RuntimeError('Run without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    first = (3, 12, 15, 48, 51, 60, 63)
    second_basis = (65, 71, 95)
    second = tuple(sorted(vector_sum(second_basis[index] for index in range(3) if bits & (1 << index)) for bits in range(1, 8)))
    first_set, second_set = set(first), set(second)
    holes = first_set | second_set
    assert not first_set & second_set and len(holes) == 14
    assert all(not dot(left, right) for side in (first, second) for left in side for right in side)
    assert [[dot(left, right) for right in second_basis] for left in (3,12,48)] == [[1,0,0],[0,1,0],[0,0,1]]
    direct = markings_from_disjoint_pairs(first, second)
    split = markings_from_charge_splits(first, second)
    assert direct == split and len(direct) == 4200
    distributions = Counter()
    for characteristic, roles in direct:
        odd_used = set(characteristic) | {point for role in roles for point in role}
        assert len(odd_used) == 9
        mixed = holes - odd_used
        first_roles = sum(charge in first_set for charge, partner in roles)
        first_mixed = len(mixed & first_set)
        first_characteristic = len(set(characteristic) & first_set)
        assert first_mixed + first_roles == 4
        assert first_characteristic == 3 - first_roles
        assert all((charge in first_set) == (partner in first_set) for charge, partner in roles)
        assert vector_sum(charge for charge, partner in roles) == vector_sum(characteristic)
        assert sum(dot(left[0], right[0]) for left, right in combinations(roles, 2)) % 2 == 0
        assert (vector_sum(characteristic) == 0) == (first_roles == 0)
        distributions[first_roles] += 1
    assert distributions == {0:1176, 1:3024}
    even = [point for point in range(1,128) if not dot(point,127)]
    array_four = array_cliques(even,4)
    assert array_four == bit_cliques(even,4) and len(array_four) == 10080
    catalogs = defaultdict(list)
    for side, other in ((first,second),(second,first)):
        for odd_pair in combinations(side,2):
            for block in array_four:
                if not all(dot(point, odd) for point in block for odd in odd_pair):
                    continue
                even_sum = vector_sum(block)
                charge = even_sum ^ vector_sum(odd_pair)
                assert even_sum in odd_pair and charge in odd_pair and charge != even_sum
                original = block + tuple(127 ^ odd for odd in odd_pair)
                assert all(dot(left,right) for left,right in combinations(original,2))
                actual = set(block) & holes
                assert len(actual) <= 1 and actual <= set(other)
                if actual:
                    catalogs[(charge,even_sum)].append((block,next(iter(actual))))
    assert len(catalogs) == 84
    catalog_counts = Counter(len(blocks) for blocks in catalogs.values())
    assert catalog_counts == {8:84}
    hole_options = {}
    for (charge,partner), blocks in catalogs.items():
        other = second if charge in first_set else first
        options = {hole for block,hole in blocks}
        expected = {hole for hole in other if dot(hole,charge) and dot(hole,partner)}
        assert options == expected and len(options) == 2
        assert Counter(hole for block,hole in blocks) == {hole:4 for hole in options}
        hole_options[(charge,partner)] = options
    assignment_histograms = {0:Counter(),1:Counter()}
    for characteristic, roles in direct:
        first_roles = sum(charge in first_set for charge,partner in roles)
        assignments = [allocation for allocation in product(*(sorted(hole_options[role]) for role in roles)) if len(set(allocation)) == 3]
        assert assignments
        assignment_histograms[first_roles][len(assignments)] += 1
    old_report_path = root/'results/dimension-7-pure-source-cover-check.json'
    old = json.loads(old_report_path.read_text())
    assert old['remaining_raw_profiles'] == {'five_six':25,'three_six':34}
    assert [4,4,4,3,5,7] in old['remaining_raw_profile_lists']['three_six']
    completion_path = root/'results/dimension-7-seven-holes.json'
    completion = json.loads(completion_path.read_text())
    assert completion['checker_sha256'] == digest(root/'develop/check_dimension_seven_seven_holes.py')
    assert completion['proof_note_sha256'] == digest(root/'notes/dimension-seven-seven-holes.md')
    inherited = {}
    for stem in ('seven-holes','two-six-profiles','size-four','hole-capacity','pure-source-cover-check'):
        path = root/('results/dimension-7-'+stem+'.json')
        report = json.loads(path.read_text())
        checker = ('develop/check_dimension_seven_pure_source_cover.py' if stem == 'pure-source-cover-check'
                   else 'develop/check_dimension_seven_'+stem.replace('-','_')+'.py')
        note = ('notes/dimension-seven-pure-source-cover.md' if stem == 'pure-source-cover-check'
                else 'notes/dimension-seven-'+stem+'.md')
        assert report['checker_sha256'] == digest(root/checker)
        assert report['proof_note_sha256'] == digest(root/note)
        for name,checksum in report.get('dependency_sha256',{}).items():
            assert digest(root/name) == checksum,name
        inherited[str(path.relative_to(root))] = digest(path)
    serialized = json.dumps(sorted(direct), separators=(',',':')).encode()
    dependencies = ('develop/check_dimension_seven_five_four_charge.py',
                    'notes/dimension-seven-two-six-profiles.md',
                    'notes/dimension-seven-size-four.md',
                    'notes/dimension-seven-hole-capacity.md',
                    'results/dimension-7-seven-holes.json',
                    'develop/check_dimension_seven_seven_holes.py',
                    'notes/dimension-seven-seven-holes.md',
                    'results/dimension-7-pure-source-cover-check.json')
    return {'status':'C7_four_four_four_capacity_equality_reduced_to_two_side_distributions',
            'dimension':7,'profile':[4,4,4,3,5,7],
            'complete_odd_markings_for_fixed_ordered_hole_pair':4200,
            'independent_marking_constructions_match':True,
            'side_distributions':[
                {'defects_on_first_side':count,'mixed_on_first_side':4-count,
                 'characteristic_on_first_side':3-count,'odd_markings':distributions[count],
                 'characteristic_charge_zero':count == 0,
                 'distinct_defect_hole_assignment_histogram':dict(sorted(assignment_histograms[count].items()))}
                for count in (0,1)],
            'all_even_four_cliques':10080,'ordered_charge_partner_catalogs':84,
            'local_one_hole_defect_catalog_size_histogram':dict(sorted(catalog_counts.items())),
            'actual_hole_options_per_defect':2,
            'even_blocks_per_actual_hole':4,
            'complete_local_defect_classes_with_one_actual_hole':sum(map(len,catalogs.values())),
            'markings_sha256':hashlib.sha256(serialized).hexdigest(),
            'new_raw_profile_exclusions':0,'remaining_raw_profiles':old['remaining_raw_profiles'],
            'remaining_raw_profile_lists':old['remaining_raw_profile_lists'],
            'remaining_C6_through_C8_count':57,'remaining_C5_count':2,
            'remaining_size_four_C8_count':0,'exact_n7':'open_lower_bound19',
            'complete_joint_roots_constructed':False,'new_cover_search':False,'new_cover_certificate':False,
            'seven_spread_completion_audit_rerun':False,'historical_cover_audits_rerun':False,
            'new_Lean':False,'new_independent_Pro_review':False,
            'old_n6_formal_scope':'three standard plus four native-evaluation axioms',
            'checker_sha256':digest(Path(__file__)),
            'proof_note_sha256':digest(root/'notes/dimension-seven-C7-equality.md'),
            'inherited_report_sha256':inherited,
            'dependency_sha256':{name:digest(root/name) for name in dependencies}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path,required=True)
    arguments = parser.parse_args()
    report = check()
    arguments.report.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:value for key,value in report.items() if key != 'remaining_raw_profile_lists'},indent=2))
