"""Build complete C7 equality marking orbits with actual defect holes."""
from itertools import permutations, product
from pathlib import Path
import argparse
import json
import time

from check_dimension_seven_C7_equality import markings_from_charge_splits
from check_dimension_seven_five_four_charge import digest, dot, vector_sum


FIRST_BASIS = (3, 12, 48)
SECOND_BASIS = (65, 71, 95)
FIRST = tuple(sorted(vector_sum(FIRST_BASIS[index] for index in range(3) if bits & (1 << index)) for bits in range(1, 8)))
SECOND = tuple(sorted(vector_sum(SECOND_BASIS[index] for index in range(3) if bits & (1 << index)) for bits in range(1, 8)))


def maps_from_first_bases():
    maps = []
    for images in permutations(FIRST, 3):
        if vector_sum(images) == 0:
            continue
        dual = tuple(next(point for point in SECOND if tuple(dot(point, image) for image in images) == tuple(int(index == column) for column in range(3))) for index in range(3))
        mapping = []
        for point in range(128):
            odd = dot(point, 127)
            even_point = point ^ (127 if odd else 0)
            mapping.append(vector_sum(image for index, image in enumerate(images) if dot(even_point, SECOND_BASIS[index])) ^
                           vector_sum(image for index, image in enumerate(dual) if dot(even_point, FIRST_BASIS[index])) ^
                           (127 if odd else 0))
        maps.append(tuple(mapping))
    return sorted(maps)


def augment(markings):
    records = set()
    for characteristic, roles in markings:
        choices = [tuple(point for point in (SECOND if charge in FIRST else FIRST) if dot(point, charge) and dot(point, partner)) for charge, partner in roles]
        for allocation in product(*choices):
            if len(set(allocation)) == 3:
                records.add((characteristic, tuple((charge, partner, hole) for (charge, partner), hole in zip(roles, allocation))))
    return records


def transport(record, mapping):
    characteristic, roles = record
    return tuple(sorted(mapping[point] for point in characteristic)), tuple(sorted(tuple(mapping[point] for point in role) for role in roles))


def build(seconds=20.0):
    if not __debug__:
        raise RuntimeError('Run without -O or PYTHONOPTIMIZE.')
    started = time.monotonic()
    if seconds <= 0:
        raise ValueError('Time limit must be positive.')
    root = Path(__file__).parents[1]
    maps = maps_from_first_bases()
    assert len(maps) == len(set(maps)) == 168
    markings = markings_from_charge_splits(FIRST, SECOND)
    records = augment(markings)
    assert len(records) == 29232
    unseen = set(records)
    orbits = []
    while unseen:
        if time.monotonic() - started > seconds:
            raise RuntimeError('Bounded orbit construction incomplete; no artifact written.')
        representative = min(unseen)
        members = {transport(representative, mapping) for mapping in maps}
        assert members <= unseen
        stabilizer = sum(transport(representative, mapping) == representative for mapping in maps)
        assert len(members) * stabilizer == 168
        orbits.append({'representative':representative, 'case':sum(charge in FIRST for charge, partner, hole in representative[1]),
                       'members':sorted(members), 'orbit_size':len(members), 'stabilizer_order':stabilizer})
        unseen -= members
    return {'status':'complete_ordered_hole_pair_C7_marking_orbits_pending_independent_audit',
            'profile':[4,4,4,3,5,7],'ordered_hole_pair':[FIRST,SECOND],
            'group_maps':maps,'group_order':168,'necessary_odd_markings':4200,
            'markings_with_distinct_actual_defect_holes':len(records),
            'orbits':orbits,'construction_limit_seconds':seconds,
            'equality_report_sha256':digest(root/'results/dimension-7-C7-equality.json')}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--orbits',type=Path,required=True)
    parser.add_argument('--seconds',type=float,default=20.0)
    arguments = parser.parse_args()
    artifact = build(arguments.seconds)
    arguments.orbits.write_text(json.dumps(artifact,separators=(',',':'))+'\n')
    print(json.dumps({'orbits':len(artifact['orbits']),'markings':artifact['markings_with_distinct_actual_defect_holes']},indent=2))
