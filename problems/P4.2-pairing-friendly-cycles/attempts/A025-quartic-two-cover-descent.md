---
attempt: A025
status: completed
---
# A025 - Fake two-Selmer audit of the unpointed quartics

## Idea

Run Magma `TwoCoverDescent` on the five everywhere-locally-soluble normalized
quartics with no known rational point. An empty fake two-Selmer set proves
that the curve has no rational point despite local solubility. Run the two
reducible pointed exceptions as positive controls.

## Predeclared outcome criteria

[CONJECTURE] Each of QG018, QG019, QG026, QG028, and QG029 has empty fake
two-Selmer set. QG012 and QG013 must have nonempty sets; otherwise the
computation contradicts their explicit rational points and is rejected.

## Execution log

[EMPIRICAL: exact Magma V2.29-8 `TwoCoverDescent`] The two positive controls
QG012 and QG013 each have fake two-Selmer set size one. Each of QG018, QG019,
QG026, QG028, and QG029 has fake two-Selmer set size zero.

## Outcome

[PROVED] The positive controls validate the direction of the calculation. The
five empty fake two-Selmer sets prove that those locally soluble curves have no
rational points and hence no integral points. The conjecture is confirmed.
