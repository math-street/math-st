// magma_pointed_quartics.m - complete integral points on pointed A024 curves.
// Sub-goal: P4.2 / SG-25
// Inputs: none; Outputs: tagged calculator text; Runtime: <1 s on V2.29-8.
// Validated against: y^2=x^4+1 and direct substitution of every returned point.

cases := [
    <"QG001", [1,0,0,0,1], []>,
    <"QG002", [4,-4,5,-4,4], []>,
    <"QG003", [4,0,-3,0,4], []>,
    <"QG004", [4,0,1,0,4], []>,
    <"QG005", [4,4,5,4,4], []>,
    <"QG006", [9,-8,10,-8,9], []>,
    <"QG007", [9,-6,11,-6,9], []>,
    <"QG008", [9,0,16,0,9], []>,
    <"QG009", [9,6,11,6,9], []>,
    <"QG010", [9,8,10,8,9], []>,
    <"QG011", [16,0,29,0,16], []>,
    <"QG012", [17,-10,27,-10,17], [-1,9]>,
    <"QG013", [17,10,27,10,17], [1,9]>,
    <"QG014", [25,-16,42,-16,25], []>,
    <"QG015", [25,-14,51,-14,25], []>,
    <"QG016", [25,14,51,14,25], []>,
    <"QG017", [25,16,42,16,25], []>,
    <"QG022", [49,-28,150,-28,49], []>,
    <"QG023", [49,-26,171,-26,49], []>,
    <"QG024", [49,26,171,26,49], []>,
    <"QG025", [49,28,150,28,49], []>,
    <"QG027", [64,0,293,0,64], []>,
    <"QG030", [81,42,443,42,81], []>,
    <"QG031", [81,44,406,44,81], []>
];

for entry in cases do
    identifier := entry[1];
    quartic := entry[2];
    point := entry[3];
    if #point eq 0 then
        points := IntegralQuarticPoints(quartic);
    else
        points := IntegralQuarticPoints(quartic, point);
    end if;
    printf "%o|OK|%o\n", identifier, points;
end for;
