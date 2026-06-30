# Query lower bound

## Phase-state model

[PROVED] Fix (N\ge2), let (s\) be uniform in `Z_N`, and let one query return a classical label (a\in\mathbb Z_N), independent of (s), together with the phase qubit

\[
  |\psi_{a,s}\rangle=\frac{|0\rangle+\exp(2\pi ias/N)|1\rangle}{\sqrt2}.
\]

[CITED] This is the standard weak-Fourier-sampling state used by Kuperberg's cyclic hidden-shift algorithms (Kuperberg 2013, Section 3, DOI 10.4230/LIPIcs.TQC.2013.20).

## Dimension lemma

[PROVED] If a uniformly distributed label (s\in\{1,\ldots,N\}) is encoded by density operators `rho_s` supported on one subspace of dimension at most (d), then every POVM that guesses (s) has average success probability at most (d/N).

[PROVED] Proof: write `Pi` for the projector onto the common support and `{M_s}` for the POVM; because each density operator satisfies (0\preceq\rho_s\preceq\Pi),

\[
 \frac1N\sum_s\operatorname{Tr}(M_s\rho_s)
 \le \frac1N\sum_s\operatorname{Tr}(M_s\Pi)
 =\frac{\operatorname{Tr}(\Pi)}N\le\frac dN.
\]

## Lower bound

[CONDITIONAL: the algorithm receives only independent standard phase-state queries as defined above] Any quantum algorithm that recovers a uniform hidden shift with success probability at least `epsilon` needs

\[
  m\ge \log_2N+\log_2\varepsilon
\]

queries, and hence needs `Omega(log N)` queries for constant success.

[PROVED] Proof under the stated condition: after conditioning on all classical labels (a_1,\ldots,a_m), the shift is encoded in (m) qubits, whose common support has dimension at most (2^m); the dimension lemma gives success at most (2^m/N), and rearranging (\varepsilon\le2^m/N) proves the bound.

[CITED] Bacon, Childs, and van Dam prove a sharper threshold for dihedral hidden-subgroup states: below one state per `log_2 N` bit the optimal identification probability is exponentially small, while above the threshold it is constant (Chicago Journal of Theoretical Computer Science 2006, DOI 10.4086/cjtcs.2006.002).

## Connection to group actions

[PROVED] For a free transitive cyclic action and endpoints (y=s\cdot x), the maps (f_0(g)=g\cdot x) and (f_1(g)=g\cdot y) are injective and satisfy (f_1(g)=f_0(g+s)); this follows directly from freeness, transitivity, and commutativity.

[CONDITIONAL: a group-action query is defined to return one standard weak-Fourier phase state] The lower bound above therefore applies to group-action inversion and is asymptotically tight at `Theta(log N)` queries, although the known measurements or postprocessing at that query count can take exponential time.

[CITED] Ettinger, Høyer, and Knill give a polynomial-logarithmic-query hidden-subgroup algorithm with potentially exponential time, and later dihedral-coset work states an `O(log N)` query upper bound (Information Processing Letters 91 (2004), DOI 10.1016/j.ipl.2004.01.024; Remaud, Schrottenloher, and Tillich 2022, arXiv:2206.14408).

## Boundary of the proof

[PROVED] The proof does not cover an arbitrary coherent query to a structured group-action circuit, because such a query need not be represented by one returned phase qubit; this is a mismatch between the proved interface and the stronger interface, not a missing algebraic step inside the dimension proof.

[PROVED] Consequently, this repository does not claim a superlogarithmic quantum query lower bound, and no subexponential query lower bound can hold in a model that already admits the cited `O(log N)`-query upper bound.

> **Gap.** [PROVED] Extending the lower bound from independent phase-state access to the most general coherent structured-action oracle requires a precise oracle definition and a reduction showing that arbitrary queries reveal no more shift information than the phase-state interface. Blocking: yes for the unrestricted wording of Task 2. Logged as Q012.
