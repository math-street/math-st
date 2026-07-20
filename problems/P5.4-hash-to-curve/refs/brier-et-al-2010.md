# Brier et al. 2010 - small-characteristic encodings

## Citation

- [CITED] Eric Brier, Jean-Sebastien Coron, Thomas Icart, David Madore, Hugues Randriam, and Mehdi Tibouchi, "Efficient Indifferentiable Hashing into Ordinary Elliptic Curves," *CRYPTO 2010*, LNCS 6223, 237--254; full version IACR ePrint 2009/340. <https://eprint.iacr.org/2009/340.pdf>

## Claims used here

- [CITED] In characteristic three, an ordinary elliptic curve can be written as $y^2=x^3+a x^2+b$ with $ab\ne0$; Section 8.1 gives a bounded encoding when the discriminant is square.
- [CITED] For square discriminant, choose nonsquare $\eta$ and $c^2=-b/a$. With $u=\eta t^2$, the candidates $x_1=c(1-u^{-1})$ and $x_2=u x_1$ include one whose curve right-hand side is square (Section 8.1).
- [CITED] In characteristic two, Appendix E treats the ordinary model $y^2+xy=x^3+a x^2+b$, $b\ne0$, over $\mathbb F_{2^n}$ for odd $n$ and gives three rational $x$ candidates.
- [CITED] The binary candidates are $x_1=tc/(1+t+t^2)$, $x_2=tx_1+c$, and $x_3=x_1x_2/(x_1+x_2)$, with $c=a+w+w^2$; at least one corresponding $h=(x^3+a x^2+b)/x^2$ has zero absolute trace (Appendix E).
- [CITED] For odd $n$, half trace solves $z^2+z=h$ when $\operatorname{Tr}(h)=0$, so $(x,x\operatorname{HTr}(h))$ is on the binary curve (Appendix D--E).
- [PROVED] The repository evaluates all three candidates and replaces the paper's early return with masked first-valid selection. It additionally masks the undefined $x=0$ rational expression to the unique point $(0,\sqrt b)$; this totalization is locally derived and exhaustively tested, not attributed to the paper.

## Scope

- [CITED] These formulas concern ordinary curves in their stated models and do not establish one formula across characteristics or presentations.
- [EMPIRICAL: repository toy fixtures only] `code/validate_small_characteristic.py` validates the formulas over $\mathbb F_3$ and $\mathbb F_{2^n}$ for $n=3,5,7$.
