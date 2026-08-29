#!/usr/bin/env python3
"""Load a Qt QM catalog and verify context-sensitive sentinel translations."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

try:
    from PyQt5.QtCore import QCoreApplication, QTranslator, QT_VERSION_STR, PYQT_VERSION_STR
except ImportError as exc:  # pragma: no cover - depends on the build environment
    print(f"ERROR: PyQt5 is required to validate QM files: {exc}", file=sys.stderr)
    raise SystemExit(2)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_sentinel(value: str) -> tuple[str, str, str]:
    parts = value.split("|", 2)
    if len(parts) != 3 or not all(parts):
        raise argparse.ArgumentTypeError("sentinel must be CONTEXT|SOURCE|EXPECTED")
    return parts[0], parts[1].replace("\\n", "\n"), parts[2].replace("\\n", "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog", type=Path)
    parser.add_argument(
        "--sentinel",
        action="append",
        type=parse_sentinel,
        default=[],
        metavar="CONTEXT|SOURCE|EXPECTED",
        help="Repeat for every exact translation that must resolve",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not args.catalog.is_file():
        parser.error(f"catalog not found: {args.catalog}")

    app = QCoreApplication.instance() or QCoreApplication([])
    translator = QTranslator(app)
    loaded = translator.load(str(args.catalog.resolve()))
    checks = []
    errors = []
    if not loaded:
        errors.append("QTranslator.load() returned false")
    else:
        app.installTranslator(translator)
        for context, source, expected in args.sentinel:
            actual = QCoreApplication.translate(context, source)
            passed = actual == expected
            checks.append(
                {
                    "context": context,
                    "source": source,
                    "expected": expected,
                    "actual": actual,
                    "passed": passed,
                }
            )
            if not passed:
                errors.append(f"sentinel failed: {context!r} / {source!r}")

    report = {
        "schema_version": 1,
        "catalog": str(args.catalog),
        "bytes": args.catalog.stat().st_size,
        "sha256": sha256(args.catalog),
        "qt_version": QT_VERSION_STR,
        "pyqt_version": PYQT_VERSION_STR,
        "loaded": loaded,
        "sentinels": checks,
        "errors": errors,
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(
            f"{args.catalog}: loaded={str(loaded).lower()}, bytes={report['bytes']}, "
            f"sentinels={len(checks)}, errors={len(errors)}, Qt={QT_VERSION_STR}"
        )
        for error in errors:
            print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
