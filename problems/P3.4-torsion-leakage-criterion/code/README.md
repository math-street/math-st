# P3.4 executable checklist

`leakage_checklist.py` evaluates a JSON leakage profile against the scoped
decision procedure in `../CHECKLIST.md`.

`leakage_closure.py` derives the `torsion_rank`, `target_action_derivable`, and
effective `torsion_order` inputs from coordinate-level point-image records. It
checks composite-modulus span, verifies all image equations, and combines only
certificates naming the same target map and a CRT-compatible basis family.

`surface_certificates.py` verifies the numerical part of K2-CD and K2-MM
witnesses. A valid numerical certificate still needs a separately constructed,
evaluable auxiliary isogeny before the classifier may return a K2 recovery
verdict.

Run the sourced protocol fixtures:

```powershell
python leakage_checklist.py --input protocol_cases.json
```

Run the boundary fixtures:

```powershell
python leakage_checklist.py --input boundary_cases.json
```

Derive action certificates from the point-image fixtures:

```powershell
python leakage_closure.py --input leakage_records.json
```

Check the surface-certificate fixtures:

```powershell
python surface_certificates.py --input surface_certificate_cases.json
```

Run the regression tests from the repository root:

```powershell
python -m unittest discover -s problems/P3.4-torsion-leakage-criterion/code/tests -v
```

The program writes deterministic JSON into `../data/`. A positive verdict is a
match to one of the encoded published templates; a negative verdict is not a
general security claim.
