# Corrigan-Gibbs--Henzinger--Wu -- structured generic groups

Henry Corrigan-Gibbs, Alexandra Henzinger, and David J. Wu, “The Structured
Generic-Group Model,” EUROCRYPT 2026; IACR ePrint 2026/384.

Primary text: <https://www.cs.utexas.edu/~dwu4/papers/SGGM.pdf>

## Model and theorem checked

[CITED] Definitions 2.2--2.4 give algorithms free access to a partial label
operation $\star$ that must agree with the group oracle wherever it is defined;
the cost measure charges only group-operation-oracle queries.

[CITED] Definition 3.1 defines labels constrained by $\star$.  Theorem 3.2
constructs a distribution over structured labelings and bounds prime-order
discrete-log advantage by
$\delta(3T+2)+(3T+1)^2/r+1/r$.

[CITED] The proof fixes the discrete logarithms of all constrained labels from
one structured labeling and randomly completes the remaining labels.  Thus its
hardness statement is existential in a labeling distribution rather than
pointwise over every concrete representation.

## Relevance to P2.2

[PROVED] A007 checks that the theorem's density term is probabilistic and does
not bound how many publicly recognizable labels an adaptive reduction may use.
It therefore cannot be substituted directly for A006's execution-wise
freshness budget.
