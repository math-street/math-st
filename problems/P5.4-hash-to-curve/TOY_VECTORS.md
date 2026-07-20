# P5.4 toy vectors

## Encoding

- [PROVED] Prime-field integers are least nonnegative residues; the identity is `INF`.
- [PROVED] Cubic-extension tuples are polynomial-basis coefficients in ascending degree order.
- [PROVED] Binary integers encode polynomial coefficients as bits, so modulus `0xb` means $X^3+X+1$.

## Cubic-extension SvdW

- [EMPIRICAL: `validate_extension_svdw.py`] The suite is $\mathbb F_7[X]/(X^3+2)$, $E:y^2=x^3+X^2x+X^2$, $Z=3X^2$.

| `u` | `x` | `y` |
|---|---|---|
| `(0,0,0)` | `(0,0,2)` | `(2,6,0)` |
| `(1,0,0)` | `(3,4,6)` | `(3,4,3)` |
| `(0,1,0)` | `(1,0,3)` | `(0,5,4)` |
| `(0,0,1)` | `(4,1,4)` | `(0,1,4)` |
| `(6,6,6)` | `(5,0,5)` | `(4,0,3)` |

- [EMPIRICAL: `validate_extension_pipeline.py`] Selected cofactor-64 outputs are:

| `(u0,u1)` | cleared result |
|---|---|
| `((0,0,0),(0,0,0))` | `((4,6,2),(5,1,1))` |
| `((0,0,0),(1,0,0))` | `((4,1,1),(6,4,3))` |
| `((1,0,0),(0,1,0))` | `((4,1,1),(6,4,3))` |
| `((0,0,1),(6,6,6))` | `INF` |

## Characteristic-three map and pipeline

- [EMPIRICAL: `validate_small_characteristic.py`] On $y^2=x^3+x^2+2$, map outputs for `u=0,1,2` are `(1,2)`, `(1,1)`, `(1,2)` respectively.
- [EMPIRICAL: `validate_small_characteristic_pipelines.py`] Two-map outputs are:

| `(u0,u1)` | cleared result |
|---|---|
| `(0,0)` | `(1,1)` |
| `(0,1)` | `INF` |
| `(1,1)` | `(1,2)` |
| `(1,2)` | `INF` |
| `(2,2)` | `(1,1)` |

## Binary degree-three map and pipeline

- [EMPIRICAL: `validate_small_characteristic.py`] The suite is $\mathbb F_2[X]/(X^3+X+1)$ and $y^2+xy=x^3+x^2+1$.

| `u` | mapped point |
|---:|---|
| 0 | `(0,1)` |
| 1 | `(0,1)` |
| 2 | `(3,0)` |
| 3 | `(7,0)` |
| 4 | `(5,0)` |
| 5 | `(3,0)` |
| 6 | `(7,0)` |
| 7 | `(5,0)` |

- [EMPIRICAL: `validate_small_characteristic_pipelines.py`] Selected cofactor-two outputs are:

| `(u0,u1)` | cleared result |
|---|---|
| `(0,0)` | `INF` |
| `(0,1)` | `INF` |
| `(1,2)` | `(7,0)` |
| `(3,7)` | `(7,7)` |
| `(6,7)` | `(7,7)` |

## Compiled p=11 profile

- [EMPIRICAL: `validate_compiled_backend.py`] For $E:y^2=x^3+1$ and SvdW $Z=1$, the complete map table is:

| `u` | mapped point |
|---:|---|
| 0 | `(5,4)` |
| 1 | `(0,1)` |
| 2 | `(9,2)` |
| 3 | `(9,9)` |
| 4 | `(5,4)` |
| 5 | `(10,0)` |
| 6 | `(0,10)` |
| 7 | `(5,7)` |
| 8 | `(9,2)` |
| 9 | `(9,9)` |
| 10 | `(10,0)` |

- [EMPIRICAL: same validator] Selected cofactor-four outputs are `(0,0)->INF`, `(0,1)->(0,1)`, `(1,2)->INF`, `(3,7)->(0,1)`, and `(10,10)->INF`.

## Production-vector boundary

- [PROVED] These are repository toy vectors, not RFC production curve-suite vectors.
- [PROVED] RFC Appendix K.1 SHA-256 XMD vectors for the empty message and `abc` are tested separately; production curve-suite execution remains disallowed by the loaded field-size ceiling.
