# Walsh 2022 -- exact traces for j=1728 curves

**Reference:** P. G. Walsh, "A note on the trace of Frobenius for curves of the form $y^2=x^3+dx$," *Annales Mathematicae et Informaticae* 55, 184--188, 2022, DOI 10.33039/ami.2022.11.003.

- [CITED] For primes $p\equiv3\pmod4$, the curve $y^2=x^3+dx$ is supersingular and has trace zero. (Section 2.)
- [CITED] For $p\equiv1\pmod4$, write $p=a^2+b^2$ with $a\equiv1\pmod4$ and $b>0$ even; the trace lies in $\{\pm2a,\pm2b\}$ and is determined by the quartic-residue class of $d$. (Theorem 2.1.)
- [CITED] The trace class can be distinguished by one modular exponentiation after the sum-of-two-squares representation is known. (Remark after Theorem 2.1.)

**Use here:**

- [PROVED] In Walsh's notation, $-1$ is a fourth power modulo $p$ exactly when $p\equiv1\pmod8$; otherwise, for $p\equiv5\pmod8$, it is a square but not a fourth power. The first and second cases of Theorem 2.1 therefore yield trace $2a$ and $-2a$ respectively for $d=-1$, which is the sign convention in `code/reproduce_cm_table.py`.
