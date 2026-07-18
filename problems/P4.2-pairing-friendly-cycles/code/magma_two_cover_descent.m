// magma_two_cover_descent.m - fake two-Selmer sets for A025 quartics.
// Sub-goal: P4.2 / SG-26
// Inputs: none; Outputs: curve id and Selmer-set size; Runtime: <1 s on V2.29-8.
// Validated against: QG012/QG013 explicit rational-point positive controls.

R<x> := PolynomialRing(Rationals());
cases := [
    <"QG012", 17*x^4-10*x^3+27*x^2-10*x+17>,
    <"QG013", 17*x^4+10*x^3+27*x^2+10*x+17>,
    <"QG018", 33*x^4-20*x^3+70*x^2-20*x+33>,
    <"QG019", 33*x^4+20*x^3+70*x^2+20*x+33>,
    <"QG026", 52*x^4+117*x^2+52>,
    <"QG028", 73*x^4-40*x^3+330*x^2-40*x+73>,
    <"QG029", 73*x^4+40*x^3+330*x^2+40*x+73>
];

for entry in cases do
    curve := HyperellipticCurve(entry[2]);
    selmer_set, descent_map := TwoCoverDescent(curve);
    printf "%o|%o\n", entry[1], #selmer_set;
end for;
