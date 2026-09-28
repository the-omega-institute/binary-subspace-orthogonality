"""Check the line coloring from integer coordinates without SAT dependencies."""
from itertools import combinations
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / 'results/line-coloring.json'
data = json.loads(path.read_text())
assert data['dimension'] == 6
assert type(data['colors']) is int and len(data['classes']) == data['colors']
assert sorted(v for group in data['classes'] for v in group) == list(range(1, 64))
for group in data['classes']:
    assert group
    for u, v in combinations(group, 2):
        assert sum(((u >> i) % 2)*((v >> i) % 2) for i in range(6)) % 2 == 1
report = {'status': 'passed', 'vertices': 63, 'colors': data['colors'],
          'class_sizes': [len(group) for group in data['classes']],
          'certificate_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
          'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'scope': 'Exact upper-bound certificate; no optimality or Lean claim.'}
(ROOT / 'results/line-coloring-check.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
