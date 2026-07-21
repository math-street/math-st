---
attempt: A005
status: completed
---
# A005 - All full algebraic tori of bounded dimension

## Idea

[CONJECTURE] The A004 obstruction extends from norm-one tori to every full
algebraic torus of uniformly bounded dimension over $\mathbb F_r$, because its
point-count polynomial is a product of cyclotomic polynomials in $r$.

## Prior art

[CITED] Batyrev--Tschinkel 1995, Theorem 1.3.11, gives
$|T(\mathbb F_r)|=(-1)^d\det(\Phi-rI)$ for the finite-order Frobenius action
$\Phi$ on the rank-$d$ character lattice.

## Prediction and decision rule

[CONJECTURE] For every fixed $D$, one CRT--Linnik prime family simultaneously
forces a factor $r^{\Omega_D(1)}$ into the order of every nontrivial full
torus of dimension at most $D$.  The prediction is refuted if a bounded-
dimension Frobenius characteristic polynomial has a noncyclotomic factor, if
infinitely many cyclotomic indices occur at fixed dimension, or if the
simultaneous congruences cannot retain polynomial-size forced factors.

## Plan

1. Prove the finite-order Frobenius characteristic polynomial is cyclotomic.
2. Prove only finitely many indices can occur below dimension $D$.
3. Force one large prime divisor of every possible cyclotomic value by
   fixed-progression PNT, exact-order residues, CRT, and Linnik.
4. State precisely why the result covers full tori but not selected subgroups.

## Execution log

- [CITED] Verified Batyrev--Tschinkel 1995, Theorem 1.3.11:
  $|T(\mathbb F_r)|=\det(rI-\Phi)$ for finite-order integral Frobenius
  $\Phi$ on the character lattice.
- [PROVED] Factored the characteristic polynomial of $\Phi$ into cyclotomic
  polynomials and proved that only indices
  $\mathcal N_D=\{n:\varphi(n)\le D\}$ occur below dimension $D$.
- [PROVED] Proved $\mathcal N_D$ is finite directly from
  $p^{a-1}(p-1)\mid\varphi(n)$ for every $p^a\mid n$.
- [PROVED] For every $n\in\mathcal N_D$, selected a comparable prime
  $\ell_n\equiv1\pmod n$, an exact-order-$n$ residue, and combined all
  congruences by CRT.
- [PROVED] Applied Linnik once to obtain an infinite prime family on which
  every $\Phi_n(r)$ in the finite menu has a factor at least
  $c_Dr^{1/(|\mathcal N_D|L_0)}$.
- [PROVED] Substituting the point-count factorization proves the same lower
  bound for every nontrivial full torus of dimension at most $D$, even when
  the algorithm chooses the torus after seeing $r$.

## Outcome

[PROVED] The prediction was confirmed.  Full algebraic tori of arbitrary type
but globally bounded dimension cannot provide a polylog-smooth auxiliary
group for every prime.  This strictly subsumes A004's norm-one result.

[PROVED] The proof does not apply to a selected subgroup of $T(\mathbb F_r)$
that omits the forced factor, to non-torus affine groups, or to abelian
varieties.  These are the next branches; no claim about elliptic-curve
existence follows from A005.
