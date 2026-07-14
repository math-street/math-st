# P5.3 code

## `sample_rigid_curve.py`

Implements SG-08's toy, forced first-passing generator. The field is fixed
from `--bits`; SHAKE256-derived field elements use exact rejection sampling;
the first curve passing the public curve/twist, cofactor, trace, embedding,
and Frobenius-discriminant checks is published. The base point is selected by
the deterministic shared-library rule.

Run the under-ten-second validation profile:

```powershell
python problems/P5.3-rigidity-formalization/code/sample_rigid_curve.py --smoke
```

The script is deliberately limited to at most 16-bit fields because it uses
the shared exact exhaustive point counter. It is not a production curve
generator.

`--samples` creates independent domain-separated experiments for measurement;
it is not a menu within one generator execution. A real \(b=0\) use fixes the
sample index, accepts one externally supplied beacon, and forbids choosing,
restarting, or suppressing that beacon.

Validation: the smoke run at \(p=127\) and eight beacon labels completed in
under one second on Python 3.13.4. Tests include the known value
\(\#E(\mathbb F_5)=9\) for \(E:y^2=x^3+x+1\), independent point enumeration, forced
first-passing verification, and deterministic replay.

## `class_uniform_kernel.py`

Exhaustively quotients the toy short-Weierstrass coefficient space by
\(\mathbb F_p\)-isomorphism, applies the existing public safety profile once
per canonical class, and exactly un-ranks the safe classes from a
domain-separated SHAKE256 stream. It is deliberately restricted to
`--bits <= 8`; it is an exact audit/reference kernel, not a production
parameter search.

Generate the fixed \(p=127\) report and canonical-class table:

```powershell
python problems/P5.3-rigidity-formalization/code/class_uniform_kernel.py --bits 7
```

Run the explicit sub-second smoke profile at \(p=31\):

```powershell
python problems/P5.3-rigidity-formalization/code/class_uniform_kernel.py --smoke
```

The JSON report distinguishes the class distribution induced by uniform
coefficient encodings from the uniform distribution over canonical safe
classes. Tests verify every recorded scaling orbit, exact counts and masses,
rank boundaries, subgroup base points, deterministic replay, and the smoke
CLI's fixed quick-profile override.
