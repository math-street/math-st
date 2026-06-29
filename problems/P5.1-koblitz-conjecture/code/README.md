# Code — P5.1

## `measure_density.py`

- [PROVED] The script enumerates primes, excludes unsupported characteristics (2,3) and bad reductions, computes each remaining \(\#E(\mathbb{F}_p)\) with the shared Hasse-interval BSGS/twist routine, falls back to exhaustive exact counting when point-order congruences do not isolate the order, and applies deterministic 64-bit primality testing.
- [EMPIRICAL: validation primes (5\le p\le97)] Before each full run, every result from the production counter is compared with an exhaustive count for every registered curve and supported prime through the validation limit; the CSV records cumulative fallback counts.
- [CITED] The test fixture for `1728.w1` converts LMFDB q-expansion coefficients via \(\#E(\mathbb{F}_p)=p+1-a_p\). (LMFDB, curve 1728.w1, accessed 2026-06-24.)
- [CITED] The supported nonzero constant is Zywina's explicit $ (10/9)C $ for $y^2=x^3+6x-2$; the script deliberately does not guess Galois images for arbitrary curves. (Zywina 2011, equation (5.1), arXiv:0909.5280.)
- [PROVED] The two rational-torsion entries have predicted (C_{E,1}=0), since their good reductions contain points of order 2 and 3 respectively.
- [HEURISTIC] The reported 95% interval treats the cumulative prime-order count as approximately Poisson; dependence across reductions or finite-(x) bias can invalidate that interval.

Run the smoke test:

```powershell
python problems/P5.1-koblitz-conjecture/code/measure_density.py --smoke
```

Run the recorded experiment:

```powershell
python problems/P5.1-koblitz-conjecture/code/measure_density.py --limit 32768
```

Run the tests:

```powershell
python -m pytest -q problems/P5.1-koblitz-conjecture/code/tests
```

**Recorded runtime:** [EMPIRICAL: Python 3.13.4, Windows 11] 2.3 seconds for `--smoke`, 6.0 seconds at $x=2^{16}$, and 11.2 seconds at $x=2^{17}$, including validation, CSV writing, and PNG rendering.

## `measure_corrected_cases.py`

- [CITED] The non-CM certificate uses LMFDB's seven generators for the level-30 adelic image `30.16.0-30.b.1.4` of curve 540.f2, whose minimal equation is $y^2=x^3+3x-11$. (LMFDB, curve 540.f2, accessed 2026-06-29.)
- [CONDITIONAL: LMFDB's level and generator data for 540.f2 are correct] Exact subgroup generation gives $|G(30)|=8640$; enumerating all 81 lifts of each matrix to level 90 gives $|G(90)|=699840$, $98280$ favorable matrices, and $delta_{E,3}(90)=91/648$.
- [CONDITIONAL: LMFDB's level and generator data for 540.f2 are correct] Proposition 2.4 then gives $C_{E,3}=(5824/5913)C$; the factor is derived by exact rational arithmetic rather than fitted to the measured quotient counts. (Zywina 2011, Proposition 2.4.)
- [CITED] The CM branch implements Zywina's absolutely convergent $L(1,\chi)^{-1}$ product for $E:y^2=x^3-x$ over $\mathbb Q(i)$ with $t=8$ and only split rational primes $p\equiv1\pmod4$. (Zywina 2011, Lemma 7.1.)
- [HEURISTIC] The reported 95% intervals use a Poisson approximation and can miss finite-cutoff bias or dependence.

Run the smoke test:

```powershell
python problems/P5.1-koblitz-conjecture/code/measure_corrected_cases.py --smoke
```

Run the recorded experiment:

```powershell
python problems/P5.1-koblitz-conjecture/code/measure_corrected_cases.py --limit 131072
```

**Recorded runtime:** [EMPIRICAL: Python 3.13.4, Windows 11] 9.0 seconds at $x=2^{17}$, including exact finite-group certification, two point-count sweeps, CSV writing, and PNG rendering.

## `reproduce_cm_table.py`

- [CITED] For $E_d:y^2=x^3+dx$, Walsh gives the four possible CM traces in terms of $p=a^2+b^2$ and the quartic-residue class of $d$; for $d=-1$ this fixes the exact sign used by the script. (Walsh 2022, Theorem 2.1, DOI 10.33039/ami.2022.11.003.)
- [PROVED] Cornacchia's sum-of-two-squares output, the normalization $a\equiv1\pmod4$, and Walsh's $d=-1$ cases give trace $2a$ for $p\equiv1\pmod8$, trace $-2a$ for $p\equiv5\pmod8$, and trace zero for $p\equiv3\pmod4$.
- [EMPIRICAL: every prime $5\le p\le1000$] The specialized CM orders match independent exhaustive point counting at every tested prime.
- [EMPIRICAL: all 50 checkpoints $2\mathbin{\cdot}10^7\le x\le10^9$] The segmented counter exactly reproduces every actual count and every rounded integral prediction in Zywina's Table 3. (`data/reproduce_cm_table_x1000000000_s51012026_20260720.csv`.)
- [EMPIRICAL: $x=10^9$] The final count is 1,548,766 versus 1,549,656.621 predicted, ratio $0.9994253$; the run processes 25,423,491 split primes.

Run the smoke test:

```powershell
python problems/P5.1-koblitz-conjecture/code/reproduce_cm_table.py --smoke
```

Reproduce the complete published table:

```powershell
python problems/P5.1-koblitz-conjecture/code/reproduce_cm_table.py --full-published-table
```

**Recorded runtime:** [EMPIRICAL: Python 3.13.4, Windows 11] 148.7 seconds through $x=10^9$, with a 10,000,000-integer prime segment and a quotient-primality table bounded by the Hasse interval.
