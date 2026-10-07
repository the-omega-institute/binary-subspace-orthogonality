# The (2,6,6;7,0,8) profile is excluded

**Theorem.** A nineteen-coloring of Gamma_7 with characteristic
class size four cannot have profile (2,6,6;7,0,8).

The [charge and recoloring theorem](dimension-seven-two-six-six-charge.md)
excludes the branch with pure-six sums in M by converting it to the
previously excluded five-plus-six profile (2,6;7,1,8). That step retains
the historical finite hole-cover input of the earlier theorem.
For sums outside M, its written normalization yields one marked form
with full stabilizer order eight. The
[complete necessary roots](dimension-seven-two-six-six-roots.md)
give 384 distinct 49-point remaining sets, reduced to 75 representatives.
A new finite failed-state certificate excludes all 75 using the full
288-row even-heptad catalog.

Exactly this raw three-six row is removed. There remain 25 five-plus-six
and 38 three-six count candidates, whose joint feasibility is untested.
Four three-six C=8 rows remain. Characteristic sizes four through eight
and exact n7 remain open, with lower bound nineteen.

## The necessary covering problem

The normalized mixed defect has even members 95,111 and odd
projections 48,51,60,63. The two pure-six sums are 65 and 113;
their roles are distinguished by pairing with the even pair. Every
ordered disjoint pure-defect pair leaves 49 even points. The preceding
complete audit supplies all 384 sets and their unique ordered defects.
The order-eight marked group preserves cover existence, actual holes
and both roles, giving 75 representatives. The orbit sizes are not
assumed equal; all orbit-stabilizer identities were checked.

The four ordered defect-hole allocations (0,0),(0,1),(1,0),(1,1)
retain 2,11,8,54 representatives. Each contains seven, six, six or
five remaining holes respectively. A cover by seven pure even heptads
must use exactly that many anchored rows, together with zero, one,
one or two rows avoiding M. The new search and independent audit
therefore use all 288 heptads, comprising 224 anchored and 64
avoiding M. No anchored-only restriction is imposed on descendants.

## A finite induction excludes every representative

The [certificate](../results/dimension-7-two-six-six-cover-proof.json)
assigns a pivot p to every recorded nonempty failed state R. The
[auditor](../develop/check_dimension_seven_two_six_six_cover.py)
reconstructs every even heptad independently from the original dot
product. For each failed state it checks p in R and considers every
heptad H contained in R with p in H. Each successor R minus H must
also be recorded as failed and have seven fewer points.

If there is no such H, the state has no cover. Otherwise any cover
must use one of those rows to cover p, and would induce a cover of
its strictly smaller successor. Induction on state cardinality proves
failure. The empty set is not recorded as failed. All representatives
occur in this acyclic proof, and every recorded state is reachable
from a required representative. The complete proof has 368 reachable
failed states, 293 checked branches and 225 leaves with no admissible
row. Its state sizes are 49,42,35,28, with counts 75,186,103,4.

This proves the outside-M covering obstruction using a new finite
certificate. Together with the inherited inside-M recoloring exclusion,
it excludes the entire specified profile. The earlier certificate is
not used to prove the outside-M obstruction and is not rerun here.

## Independent reconstruction and accounting

The auditor reconstructs the complete root catalogs and orbit partitions,
matches the preceding report exactly, and binds its source identity.
Independent array and bitmask catalogs agree. It checks all admissible
pivot successors from the complete 288-row catalog and rejects invalid
controls with a missing representative, absent pivot, falsely failed
empty state or omitted required successor.

Accounting independently enumerates all 46 five-plus-six and 48
three-six raw rows from the parity-count equations. It verifies that
the target appears exactly once in the preceding 39-row three-six
list, removes exactly it, and preserves the 25-row five-plus-six list.
The [audit report](../results/dimension-7-two-six-six-cover-check.json)
records the new 25/38 lists and their full count distributions.
This raises the excluded three-six count to 10 of 48; the excluded
five-plus-six count stays 21 of 46.

No Lean or independent Pro review is claimed. The original six-dimensional
formal theorem retains three standard plus four native-evaluation axioms.
The submitted manuscript is preserved; the result is incorporated in
the authorized extended working draft, whose publication and submission
remain separate decisions.

```sh
python3 develop/build_dimension_seven_two_six_six_cover.py --certificate /tmp/dimension-7-two-six-six-cover-proof.json
python3 develop/check_dimension_seven_two_six_six_cover.py --report /tmp/dimension-7-two-six-six-cover-check.json
```
