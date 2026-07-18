"""
build.py — compile ECC-research papers from Typst to PDF and report page counts.

Usage:
    python build.py                 # compile every papers/P*.typ
    python build.py P1.1 P2.3       # compile only the named PIDs
"""
from __future__ import annotations
import sys, glob, os
import typst
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))


def compile_one(src: str) -> tuple[str, int | None, str | None]:
    pdf = src[:-4] + ".pdf"
    try:
        typst.compile(src, output=pdf, root=HERE)
    except Exception as e:  # surface real compile errors, never swallow
        return (src, None, str(e))
    n = len(PdfReader(pdf).pages)
    return (pdf, n, None)


def main(argv: list[str]) -> int:
    if argv:
        srcs = [os.path.join(HERE, f"{a}.typ") for a in argv]
    else:
        srcs = sorted(glob.glob(os.path.join(HERE, "P*.typ")))
    rc = 0
    for src in srcs:
        name = os.path.basename(src)
        if not os.path.exists(src):
            print(f"  MISSING  {name}")
            rc = 1
            continue
        pdf, n, err = compile_one(src)
        if err is not None:
            print(f"  FAIL     {name}")
            print("           " + err.strip().replace("\n", "\n           "))
            rc = 1
        else:
            flag = "ok " if (n or 0) >= 10 else "<10"
            print(f"  {flag}      {os.path.basename(pdf)}  --  {n} pages")
    return rc


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
