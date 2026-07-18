# Reingold--Trevisan--Vadhan -- black-box taxonomy

Omer Reingold, Luca Trevisan, and Salil Vadhan, “Notions of Reducibility
between Cryptographic Primitives,” TCC 2004, LNCS 2951, 1--20.

Primary text: <https://lucatrevisan.github.io/pubs/rtv04.pdf>

## Relevant definitions

[CITED] Definition 3 calls a reduction fully black-box when fixed PPT oracle
machines implement the construction and the security transformation, and the
security transformer, given oracle access to every breaking adversary and to
the primitive, breaks the underlying primitive.  The quantified breaking
adversary need not be efficient.

[CITED] The paper distinguishes fully-black-box reductions from semi-black-box,
weakly-black-box, and free reductions, emphasizing that negative results about
one class do not establish impossibility for the others.  [§§1--2]

[CITED] The authors identify access to the adversary's code as a route outside
fully-black-box barriers; a transformer that uses the code rather than only
oracle access is not covered by the fully-black-box definition.  [§§1.1, 1.5]

## Audit note

[PROVED] Definition 3 and the surrounding distinctions in Sections 1 and 2
were checked in the authors' primary PDF.
