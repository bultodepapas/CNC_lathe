#!/usr/bin/env python3
"""Audit the exact QtDragon sources used to build the Spanish catalog.

This script is intentionally read-only. It parses local snapshots and prints a
machine-readable report; it never connects to or changes the CNC controller.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from collections import Counter
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BASE = ROOT / "vendor" / "linuxcnc-2.9.7-qtdragon"
DEFAULT_UI = DEFAULT_BASE / "usr" / "share" / "qtvcp" / "screens" / "qtdragon" / "qtdragon.ui"
DEFAULT_HANDLER = DEFAULT_BASE / "usr" / "share" / "qtvcp" / "screens" / "qtdragon" / "qtdragon_handler.py"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def xml_text(element: ET.Element) -> str:
    return "".join(element.itertext())


def analyze_ui(path: Path) -> dict[str, object]:
    root = ET.parse(path).getroot()
    strings = root.findall(".//string")
    eligible = [item for item in strings if item.get("notr") != "true"]
    nonempty = [item for item in eligible if xml_text(item).strip()]
    sources = [xml_text(item) for item in nonempty]
    duplicates = {
        source: count
        for source, count in Counter(sources).items()
        if count > 1
    }
    return {
        "path": str(path),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "string_nodes": len(strings),
        "notr_true": len(strings) - len(eligible),
        "translatable_nodes": len(eligible),
        "translatable_nonempty": len(nonempty),
        "unique_nonempty_sources": len(set(sources)),
        "duplicate_source_count": len(duplicates),
    }


def call_name(node: ast.Call) -> str:
    target = node.func
    if isinstance(target, ast.Name):
        return target.id
    if isinstance(target, ast.Attribute):
        return target.attr
    return "<dynamic>"


def literal_from_call(node: ast.Call) -> str | None:
    for arg in node.args:
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            return arg.value
        if isinstance(arg, ast.JoinedStr):
            return "<f-string>"
    return None


def analyze_handler(path: Path) -> dict[str, object]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]
    visible_methods = {
        "add_status",
        "setText",
        "setToolTip",
        "setWindowTitle",
        "setTitle",
        "information",
        "warning",
        "critical",
        "question",
    }
    visible = [node for node in calls if call_name(node) in visible_methods]
    translate_names = {"_translate", "translate", "tr"}
    translated = [node for node in calls if call_name(node) in translate_names]
    method_counts = Counter(call_name(node) for node in visible)
    return {
        "path": str(path),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "translate_calls": len(translated),
        "candidate_visible_calls": len(visible),
        "visible_call_counts": dict(sorted(method_counts.items())),
        "add_status_calls": sum(1 for node in calls if call_name(node) == "add_status"),
        "literal_examples": [
            {"line": node.lineno, "method": call_name(node), "text": literal_from_call(node)}
            for node in visible[:20]
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ui", type=Path, default=DEFAULT_UI)
    parser.add_argument("--handler", type=Path, default=DEFAULT_HANDLER)
    parser.add_argument("--pretty", action="store_true", help="Indent the JSON output")
    args = parser.parse_args()

    missing = [str(path) for path in (args.ui, args.handler) if not path.is_file()]
    if missing:
        parser.error("missing source file(s): " + ", ".join(missing))

    report = {
        "schema_version": 1,
        "read_only": True,
        "ui": analyze_ui(args.ui),
        "handler": analyze_handler(args.handler),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
