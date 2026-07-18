---
attempt: A020
status: completed
---
# A020 - Canonicalize the final quartic curve set

## Idea

Remove constant square content from every surviving discriminant and group
identical primitive quartics. The identities
\(\Phi_5(-c)=\Phi_{10}(c)\),
\(\Phi_{10}(-c)=\Phi_5(c)\), and the evenness of
\(\Phi_8,\Phi_{12}\) predict substantial duplication.

## Predeclared outcome criteria

[CONJECTURE] The 51 surviving rows represent fewer than 40 distinct primitive
genus-one equations. Any nonsquare polynomial content prevents the proposed
normalization and must be retained separately.

## Execution log

[EMPIRICAL: exact content factorization] The 51 rows have polynomial contents
1 (46 rows), 4 (4 rows), and 13 (1 row). The nonsquare content 13 refutes any
blanket assumption that primitive-part equality alone is safe. The corrected
normal form removes only square content and retains the squarefree twist.

[PROVED] The cyclotomic sign identities in the idea identify each duplicated
pair exactly after this normalization.

## Outcome

[EMPIRICAL: exact normalized coefficient equality] The conjectured count bound
is confirmed: 51 rows reduce to 31 distinct curves, comprising 20 curves of
multiplicity two and 11 curves of multiplicity one.
