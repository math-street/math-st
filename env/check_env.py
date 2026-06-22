"""Print the versions of tools used by the toy-scale research environment."""

from __future__ import annotations

import platform
import shutil
from importlib.metadata import PackageNotFoundError, version


def main() -> None:
    print(f"python={platform.python_version()}")
    print(f"platform={platform.platform()}")
    try:
        print(f"numpy={version('numpy')}")
    except PackageNotFoundError:
        print("numpy=unavailable")
    for executable in ("sage", "gp", "Singular", "msolve"):
        print(f"{executable}={shutil.which(executable) or 'unavailable'}")


if __name__ == "__main__":
    main()
