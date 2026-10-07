# A nineteen-coloring must put at least three lines in the characteristic class

**Theorem.** In any proper nineteen-coloring of the dimension-seven
line graph Gamma_7, the class C_z containing the characteristic line
z=127 has size at least three. Thus 3<=|C_z|<=8. The exact line and
full-subspace chromatic numbers remain open with lower bound nineteen;
no nineteen-color witness or improved numerical lower bound is supplied.

Here size counts z itself: the theorem requires at least two other
lines in C_z. It excludes all three two-point-characteristic profiles
left by the [preceding deficit analysis](dimension-seven-nineteen-deficits.md).
The proof uses a projected vector sum and a recoloring step.

## Every saturated seven-point class has zero projected sum

Let E=z-perp and define the linear projection

```text
pi(v)=v+(v dot z)z.
```

Since z dot z=1, pi maps onto E and has kernel {0,z}. It sends an
even line u to u and an odd line z+e to e. Over all 127 nonzero
line generators its sum is zero: every nonzero e in E has two
preimages, and z projects to zero.

An independent class of size seven avoiding z has one of three
forms. In each form its projected sum is zero:

- Seven even vectors have Gram matrix J_7+I_7 of rank six with
  all-ones kernel, so their vector sum is zero.
- Seven odd vectors project to all seven nonzero points of a
  Lagrangian three-space, whose vector sum is zero.
- Six even vectors u_1,...,u_6 and one odd line z+e have
  e=u_1+...+u_6. Their projected sum is e+e=0.

The last identity follows directly: the even Gram matrix J_6+I_6
is invertible, and the sum of the six even vectors pairs to one
with each u_i, as does e. They form a basis of E, so these pairings
determine e uniquely.

Consequently, in any nineteen-color partition, the projected sums
of the undersized classes outside C_z add up to the projected sum
of C_z. All saturated seven-point classes contribute zero. This
is a vector constraint in E, stronger than the scalar size deficit.

## Moving the companion excludes the remaining two-point profiles

Suppose C_z={z,a}, where a=z+e_0 and e_0 is nonzero. The deficit
identity gives exactly one six-point class D outside C_z and
seventeen saturated seven-point classes. The projection identity gives

```text
sum_{v in D} pi(v)=e_0.
```

The three remaining count profiles all have an even number of odd
lines in D: either six odd lines, or two even and four odd lines.
Thus sum_{v in D}(v dot z)=0, and the projected sum is the ordinary
sum. In particular

```text
sum_{v in D} v=e_0,       a=z+sum_{v in D}v.
```

For each v in D, the five other vectors pair to one with v, and
v dot v=v dot z. Therefore

```text
v dot a = v dot z + v dot sum_{w in D}w
        = v dot z + v dot v + 5 = 1.
```

Since a is in C_z, it is distinct from every member of D. Moving a
from C_z into D therefore preserves the coloring. After removing z,
its singleton class disappears, leaving an eighteen-coloring of
Gamma_7 minus z. The [deleted-line lower bound nineteen](dimension-seven-nineteen-deficits.md)
excludes this. All three remaining size-two profiles are impossible.

For completeness, the six-point capacity table allows even counts
0,2,4,5,6. The same transfer argument excludes all even-count cases.
The sole odd-count case is D of type (5 even,1 odd); its forced
profile (A,B,C)=(4,5,8) was already excluded by the eight-Lagrangian
completion argument, which leaves only four labels for a seven-clique.
Thus the result does not depend on leaving any unexamined size-two
count profile.

The lower bound three is necessary, not an assertion that a
nineteen-coloring with a three-point characteristic class exists.
For such a coloring the outside deficit is two: it has either one
five-point class or two six-point classes. Their projected sums
must equal the sum of the two nonzero projections in C_z. These
are the next structural cases, still open here.

## Independent finite checks and scope

The [standard-library checker](../develop/check_dimension_seven_characteristic_three.py)
constructs the line generators and all 135 Lagrangians directly from
binary dot products. It enumerates all independent six-point and
seven-point sets avoiding z by their even part and their compatible
odd projections. The odd projections span an isotropic space and
therefore lie in a Lagrangian, which justifies the enumeration.

For every seven-point class it checks the zero projected sum. For
every six-point class with even odd count it checks the transfer
pairings. It records separately when the proposed transferred line
already belongs to D; in a hypothetical partition that would itself
contradict disjointness from C_z. The (5,1) classes provide controls
for the parity requirement: their proposed line is orthogonal to
the existing odd member, so the transfer argument does not apply.
The checker also verifies all seven historical size-two count
profiles and their final exclusions, without asserting their
realizability. The [certificate](../results/dimension-7-characteristic-three.json)
records the exact counts and source identities.

These checks support the written universal recoloring argument.
There is no SAT solve, checked UNSAT proof, Lean run or enumeration
of complete colorings. The submitted manuscript at 28e27a8 and the
original dimension-six Lean theorem, with three standard and four
native-evaluation axioms, remain unchanged.

```sh
python3 develop/check_dimension_seven_characteristic_three.py --report /tmp/dimension-7-characteristic-three.json
```
