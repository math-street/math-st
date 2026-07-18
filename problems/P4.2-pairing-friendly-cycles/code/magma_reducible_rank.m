// magma_reducible_rank.m - close the QG012/QG013 pointed exceptions.
// Sub-goal: P4.2 / SG-25
// Inputs: none; Outputs: rank bounds, torsion, and point images.
// Runtime: <1 s on V2.29-8.
// Validated against: direct substitution of (-1,+/-9) on QG012.

model := ChangeRing(
    GenusOneModel([17,-10,27,-10,17]),
    Rationals()
);
curve := Curve(model);
point_plus := curve![-1,1,9];
point_minus := curve![-1,1,-9];
elliptic_curve, curve_map := EllipticCurve(curve, point_plus);
RankBounds(elliptic_curve);
torsion, torsion_map := TorsionSubgroup(elliptic_curve);
torsion;
torsion_map(torsion.1);
curve_map(point_plus);
curve_map(point_minus);
