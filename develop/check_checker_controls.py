"""Negative controls for the independent full-graph coloring checker."""
from pathlib import Path
from tempfile import TemporaryDirectory
import copy
import json

from check_full_coloring import check

ROOT = Path(__file__).resolve().parents[1]
source = json.loads((ROOT/'results/full-15-coloring.json').read_text())
cases = {}
bad = copy.deepcopy(source)
bad['subspace_colors'].pop()
cases['missing_subspace'] = bad
bad = copy.deepcopy(source)
bad['subspace_colors'][1]['basis'] = bad['subspace_colors'][0]['basis']
cases['duplicate_subspace'] = bad
bad = copy.deepcopy(source)
one = next(r for r in bad['subspace_colors'] if r['basis'] == [1])
two = next(r for r in bad['subspace_colors'] if r['basis'] == [2])
two['color'] = one['color']
cases['monochromatic_coordinate_edge'] = bad
rejected = []
with TemporaryDirectory(prefix='orthogonality-checker-controls-') as directory:
    for name, data in cases.items():
        path = Path(directory)/(name+'.json')
        path.write_text(json.dumps(data))
        try:
            check(path)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('Checker accepted '+name)
report = {'status':'passed','rejected':rejected}
(ROOT/'results/checker-controls.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
