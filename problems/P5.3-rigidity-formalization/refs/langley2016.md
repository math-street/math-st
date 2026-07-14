# Langley–Hamburg–Turner 2016 — RFC 7748

**Reference.** [CITED] Adam Langley, Mike Hamburg, and Sean Turner,
*Elliptic Curves for Security*, RFC 7748, IRTF CFRG, January 2016,
doi:10.17487/RFC7748. <https://www.rfc-editor.org/rfc/rfc7748.html>

**Relevant source facts.** [CITED] Appendix A gives executable first-passing
rules for the Montgomery coefficient and the minimal base-point
\(u\)-coordinate after the field prime is fixed. Its square-root step does not
state a mathematical \(v\)-sign rule. It also says that choosing the precise
prime depends on implementation considerations that the RFC does not fully
articulate.

**Audit use. [PROVED]** Conditional on \(p\), the RFC leaves no screenable
curve-core menu. A full affine package has at most one base-point sign bit;
X25519's \(u\)-only package has none. The unconditional field provenance is
not identifiable from the RFC alone.
