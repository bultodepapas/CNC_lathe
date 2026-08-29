#!/usr/bin/env python3
"""Validate a Qt Linguist TS catalog before compiling it to QM."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
import json
from pathlib import Path
import re
from string import Formatter
import sys
import xml.etree.ElementTree as ET


QT_PLACEHOLDER = re.compile(r"%L?\d+|%n|%(?!%)(?:[-+#0 ]*\d*(?:\.\d+)?[diouxXeEfFgGcrsa])")
HTML_TAG = re.compile(r"<\s*(/?)\s*([A-Za-z][\w:-]*)\b[^>]*?(/?)\s*>")
CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


@dataclass(frozen=True)
class Problem:
    severity: str
    context: str
    source: str
    detail: str


def text_of(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return "".join(element.itertext())


def brace_fields(value: str) -> tuple[str, ...]:
    try:
        fields = []
        for _, field_name, _, _ in Formatter().parse(value):
            if field_name is not None:
                fields.append(field_name)
        return tuple(fields)
    except ValueError:
        return ("<MALFORMED>",)


def tag_signature(value: str) -> Counter[str]:
    signature: Counter[str] = Counter()
    for closing, name, self_closing in HTML_TAG.findall(value):
        prefix = "/" if closing else ""
        suffix = "/" if self_closing else ""
        signature[f"{prefix}{name.lower()}{suffix}"] += 1
    return signature


def variants(translation: ET.Element) -> list[str]:
    forms = translation.findall("numerusform")
    if forms:
        return [text_of(form) for form in forms]
    return [text_of(translation)]


def compact(value: str, limit: int = 90) -> str:
    value = " ".join(value.split())
    return value if len(value) <= limit else value[: limit - 1] + "…"


def validate(path: Path) -> tuple[dict[str, object], list[Problem]]:
    tree = ET.parse(path)
    root = tree.getroot()
    problems: list[Problem] = []
    totals = Counter()
    completed_by_context: Counter[str] = Counter()
    total_by_context: Counter[str] = Counter()
    translations_by_source: defaultdict[str, set[str]] = defaultdict(set)

    language = root.get("language", "")
    if language and not language.lower().startswith("es"):
        problems.append(Problem("error", "<catalog>", "", f"language is {language!r}, expected Spanish"))

    for context in root.findall("context"):
        context_name = text_of(context.find("name")) or "<unnamed>"
        for message in context.findall("message"):
            totals["messages"] += 1
            source = text_of(message.find("source"))
            translation = message.find("translation")
            translation_type = translation.get("type", "") if translation is not None else ""
            if translation_type in {"obsolete", "vanished"}:
                totals[translation_type] += 1
                continue

            totals["active"] += 1
            total_by_context[context_name] += 1
            if translation is None or translation_type == "unfinished":
                totals["unfinished"] += 1
                continue

            translated_variants = variants(translation)
            if not translated_variants or any(not item.strip() for item in translated_variants):
                totals["empty_finished"] += 1
                problems.append(Problem("error", context_name, source, "finished translation is empty"))
                continue

            totals["finished"] += 1
            completed_by_context[context_name] += 1
            for target in translated_variants:
                translations_by_source[source].add(target)
                if Counter(QT_PLACEHOLDER.findall(source)) != Counter(QT_PLACEHOLDER.findall(target)):
                    problems.append(Problem("error", context_name, source, "Qt/Python percent placeholders differ"))
                if Counter(brace_fields(source)) != Counter(brace_fields(target)):
                    problems.append(Problem("error", context_name, source, "brace-format placeholders differ"))
                if tag_signature(source) != tag_signature(target):
                    problems.append(Problem("error", context_name, source, "HTML tag structure differs"))
                if CONTROL.search(target):
                    problems.append(Problem("error", context_name, source, "translation contains control characters"))
                if source.count("\n") != target.count("\n"):
                    problems.append(Problem("warning", context_name, source, "line-break count differs"))

    for source, targets in translations_by_source.items():
        if source.strip() and len(targets) > 1:
            problems.append(
                Problem("warning", "<duplicates>", source, f"inconsistent translations: {sorted(targets)!r}")
            )

    active = totals["active"]
    report = {
        "schema_version": 1,
        "catalog": str(path),
        "language": language,
        "messages": totals["messages"],
        "active": active,
        "finished": totals["finished"],
        "unfinished": totals["unfinished"],
        "empty_finished": totals["empty_finished"],
        "obsolete": totals["obsolete"],
        "vanished": totals["vanished"],
        "coverage_percent": round(100 * totals["finished"] / active, 2) if active else 100.0,
        "contexts": {
            name: {
                "active": count,
                "finished": completed_by_context[name],
                "coverage_percent": round(100 * completed_by_context[name] / count, 2) if count else 100.0,
            }
            for name, count in sorted(total_by_context.items())
        },
        "errors": sum(problem.severity == "error" for problem in problems),
        "warnings": sum(problem.severity == "warning" for problem in problems),
    }
    return report, problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog", type=Path)
    parser.add_argument("--min-coverage", type=float, default=98.0)
    parser.add_argument("--json", action="store_true", help="Print the full report as JSON")
    args = parser.parse_args()
    if not args.catalog.is_file():
        parser.error(f"catalog not found: {args.catalog}")

    try:
        report, problems = validate(args.catalog)
    except (ET.ParseError, OSError) as exc:
        print(f"ERROR: cannot read TS catalog: {exc}", file=sys.stderr)
        return 2

    if report["coverage_percent"] < args.min_coverage:
        problems.append(
            Problem(
                "error",
                "<catalog>",
                "",
                f"coverage {report['coverage_percent']}% is below {args.min_coverage}%",
            )
        )
        report["errors"] += 1

    if args.json:
        payload = {"report": report, "problems": [problem.__dict__ for problem in problems]}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(
            f"{args.catalog}: {report['finished']}/{report['active']} active messages "
            f"({report['coverage_percent']}%), {report['errors']} errors, {report['warnings']} warnings"
        )
        for problem in problems:
            print(
                f"{problem.severity.upper()}: [{problem.context}] {problem.detail}; "
                f"source={compact(problem.source)!r}"
            )
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
