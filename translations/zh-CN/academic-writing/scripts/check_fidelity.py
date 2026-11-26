#!/usr/bin/env python3
"""Deterministic local fidelity checker for academic and technical writing.

Python 3.9+, standard library only, no network calls.
Checks surface preservation of numbers, units, LaTeX math/citations/refs,
code spans/blocks, Markdown link URLs, and user-protected literals.
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import sys
from typing import Counter, Iterable, Sequence

TASKS = ("proofread", "polish", "rewrite", "translate", "draft")

# Exact preservation of common academic markup (not a full LaTeX parser).
# Inline $...$ uses Pandoc-style boundaries (no leading/trailing whitespace) to avoid
# swallowing currency ranges such as "$5 million to $10 million".
MARKUP_RE = re.compile(
    r"```[\s\S]*?```"
    r"|`[^`\n]+`"
    r"|\$\$[\s\S]*?\$\$"
    r"|(?<!\\)\$(?!\s)(?:\\.|[^$\n])+?(?<!\s)\$"
    r"|\\\([\s\S]*?\\\)"
    r"|\\\[[\s\S]*?\\\]"
    r"|\\(?:(?:auto|paren|text|foot|full|super|no)?cite\w*|label|ref|eqref|autoref|cref|Cref|nameref)"
    r"(?:\[[^\]\n]*\]){0,2}\{[^{}]+\}"
    r"|\[@[^\]\n]+\]"
)

# Capture Markdown link/image URL targets while keeping visible anchor text for normal checks.
MD_LINK_RE = re.compile(r"(!?\[[^\]]*\])\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")

# Core numeric pattern supporting signs, thousands separators, decimals, and scientific notation.
_NUM_CORE = (
    r"[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?"
    r"(?:[eE][-+]?\d+|\s*[×xX]\s*10\^\{?[-+]?\d+\}?)?"
    r"|[-+]?\.\d+(?:[eE][-+]?\d+)?"
)

NUM_RE = re.compile(rf"(?<![A-Za-z0-9_])(?:{_NUM_CORE})")

# Common scientific & engineering units, including compound forms like m/s^2, Wh/kg, kg/m³.
_BASE_UNITS = (
    r"°\s*[CF]|%|ppm|ppb|dBm|dB"
    r"|kWh|MWh|Wh|GW|MW|kW|mW|µW|W"
    r"|kV|mV|µV|V|kA|mA|µA|A|mAh|Ah"
    r"|GHz|MHz|kHz|Hz|min|ms|µs|ns|h|s"
    r"|kg|mg|µg|g|km|cm|mm|µm|nm|m"
    r"|GPa|MPa|kPa|Pa|bar|psi|atm"
    r"|rpm|kN|N·m|Nm|N|kJ|MJ|J|mmol|mol|mL|L|MΩ|kΩ|Ω|K"
)
_UNIT_EXP = r"(?:\^-?\d+|[²³])"
_UNIT_COMPOUND = rf"(?:/[A-Za-zµ°]+{_UNIT_EXP}?|{_UNIT_EXP})?"

UNIT_RE = re.compile(
    rf"(?<![A-Za-z0-9_])({_NUM_CORE})\s*((?:{_BASE_UNITS}){_UNIT_COMPOUND})(?![A-Za-z])"
)

UNIT_EXPONENT_CLEANUP_RE = re.compile(r"(?<=[A-Za-zµ°])\^-?\d+")

FULLWIDTH_TABLE = str.maketrans(
    "０１２３４５６７８９＋－．％，",
    "0123456789+-.%,",
)


def normalize_text(text: str) -> str:
    """Normalize visually equivalent signs, fullwidth digits, and micro symbols."""
    return (
        text.translate(FULLWIDTH_TABLE)
        .replace("\u2212", "-")  # Unicode minus
        .replace("\u03bc", "\u00b5")  # Greek mu -> micro sign
    )


def normalize_number(raw: str) -> str:
    """Canonicalize numeric tokens for comparison."""
    cleaned = raw.replace(",", "")
    cleaned = re.sub(r"\s+", "", cleaned)
    cleaned = cleaned.replace("E", "e").replace("X", "×").replace("x", "×")
    cleaned = re.sub(r"10\^\{([-+]?\d+)\}", r"10^\1", cleaned)
    return cleaned


def normalize_unit(unit: str) -> str:
    """Canonicalize unit formatting (spacing and superscripts)."""
    cleaned = re.sub(r"\s+", "", unit)
    cleaned = cleaned.replace("²", "^2").replace("³", "^3")
    return cleaned


def normalize_allow_set(allow_change: Iterable[str]) -> set[str]:
    """Expand --allow-change entries with normalized numeric and unit variants."""
    allowed: set[str] = set()
    for raw in allow_change:
        item = raw.strip()
        if not item:
            continue
        allowed.add(raw)
        allowed.add(item)
        norm = normalize_text(item)
        allowed.add(norm)
        if NUM_RE.fullmatch(norm):
            allowed.add(normalize_number(norm))
        unit_match = UNIT_RE.fullmatch(norm)
        if unit_match:
            allowed.add(f"{normalize_number(unit_match.group(1))} {normalize_unit(unit_match.group(2))}")
    return allowed


def extract_tokens(text: str) -> dict[str, Counter[str]]:
    """Extract surface tokens from text for fidelity comparison."""
    markup = collections.Counter(MARKUP_RE.findall(text))
    stripped = MARKUP_RE.sub(" ", text)

    link_urls: Counter[str] = collections.Counter()

    def _replace_link(match: re.Match[str]) -> str:
        link_urls[match.group(2)] += 1
        return f"{match.group(1)} "

    stripped = MD_LINK_RE.sub(_replace_link, stripped)
    normalized = normalize_text(stripped)

    units: Counter[str] = collections.Counter()
    for num_raw, unit_raw in UNIT_RE.findall(normalized):
        units[f"{normalize_number(num_raw)} {normalize_unit(unit_raw)}"] += 1

    # Remove unit exponents like ^2 in m/s^2 so they are not miscounted as standalone numbers.
    num_text = UNIT_EXPONENT_CLEANUP_RE.sub(" ", normalized)
    numbers = collections.Counter(
        normalize_number(match.group(0)) for match in NUM_RE.finditer(num_text)
    )

    return {
        "markup": markup,
        "link_url": link_urls,
        "number": numbers,
        "unit": units,
    }


def check_fidelity(
    source: str,
    candidate: str,
    *,
    task: str = "polish",
    protect: Iterable[str] = (),
    allow_change: Iterable[str] = (),
    allow_dedup: bool = False,
) -> list[dict[str, object]]:
    """Compare source and candidate text and return structured fidelity findings."""
    issues: list[dict[str, object]] = []
    if not candidate.strip():
        issues.append(
            {
                "severity": "error",
                "category": "empty",
                "direction": "missing",
                "value": "candidate text is empty",
                "count": 1,
            }
        )
        return issues

    if task == "translate" and candidate.strip() == source.strip():
        issues.append(
            {
                "severity": "error",
                "category": "translation",
                "direction": "unchanged",
                "value": "candidate is identical to source; verify target language",
                "count": 1,
            }
        )

    src_tokens = extract_tokens(source)
    cand_tokens = extract_tokens(candidate)
    allowed = normalize_allow_set(allow_change)

    for category in ("markup", "link_url", "number", "unit"):
        if allow_dedup:
            # Verify every unique source token remains present at least once,
            # while still flagging any newly added tokens not present in source.
            missing = collections.Counter(
                {k: 1 for k in src_tokens[category] if k not in cand_tokens[category]}
            )
            added = collections.Counter(
                {k: v for k, v in cand_tokens[category].items() if k not in src_tokens[category]}
            )
        else:
            missing = src_tokens[category] - cand_tokens[category]
            added = cand_tokens[category] - src_tokens[category]

        for direction, diff in (("missing", missing), ("added", added)):
            # Drafting selects from notes, so omitting unused source tokens is permitted.
            if task == "draft" and direction == "missing":
                continue
            for value, count in sorted(diff.items()):
                if value in allowed:
                    continue
                severity = "warning" if category == "unit" else "error"
                issues.append(
                    {
                        "severity": severity,
                        "category": category,
                        "direction": direction,
                        "value": value,
                        "count": count,
                    }
                )

    for term in protect:
        if term in allowed:
            continue
        src_count = source.count(term)
        cand_count = candidate.count(term)
        if src_count == 0:
            issues.append(
                {
                    "severity": "warning",
                    "category": "protected",
                    "direction": "absent_in_source",
                    "value": term,
                    "count": 0,
                }
            )
            continue
        if task == "draft" or allow_dedup:
            if cand_count == 0:
                issues.append(
                    {
                        "severity": "error",
                        "category": "protected",
                        "direction": "missing",
                        "value": term,
                        "count": src_count,
                    }
                )
        elif cand_count != src_count:
            issues.append(
                {
                    "severity": "error",
                    "category": "protected",
                    "direction": "count_mismatch",
                    "value": term,
                    "count": abs(src_count - cand_count),
                    "expected": src_count,
                    "actual": cand_count,
                }
            )

    return issues


def has_errors(issues: Sequence[dict[str, object]]) -> bool:
    return any(item["severity"] == "error" for item in issues)


def has_warnings(issues: Sequence[dict[str, object]]) -> bool:
    return any(item["severity"] == "warning" for item in issues)


def read_input(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return pathlib.Path(path).read_text(encoding="utf-8")


def format_text_report(status: str, issues: Sequence[dict[str, object]]) -> str:
    lines = [f"Status: {status}"]
    if not issues:
        lines.append("No surface fidelity issues detected.")
        return "\n".join(lines)
    for item in issues:
        extra = ""
        if "expected" in item and "actual" in item:
            extra = f" (expected {item['expected']}, actual {item['actual']})"
        lines.append(
            f"- [{item['severity']}] {item['category']} ({item['direction']} x{item['count']}): "
            f"{item['value']}{extra}"
        )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check surface fidelity (numbers, units, math, citations, URLs, protected terms)."
    )
    parser.add_argument("source", help="Path to source text file, or '-' for stdin.")
    parser.add_argument("candidate", help="Path to candidate text file, or '-' for stdin.")
    parser.add_argument(
        "--task",
        choices=TASKS,
        default="polish",
        help="Task type controlling missing/unchanged rules (default: polish).",
    )
    parser.add_argument(
        "--allow-dedup",
        action="store_true",
        help="Check unique token presence rather than exact repetition count (for deduplicating rewrites).",
    )
    parser.add_argument(
        "--protect",
        action="append",
        default=[],
        help="Literal string whose occurrences must be preserved (repeatable).",
    )
    parser.add_argument(
        "--allow-change",
        action="append",
        default=[],
        help="Authorized changed token value to ignore; normalized automatically (repeatable).",
    )
    parser.add_argument(
        "--format",
        choices=("json", "text"),
        default="json",
        help="Output format (default: json).",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.source == "-" and args.candidate == "-":
        print("Error: source and candidate cannot both be '-'.", file=sys.stderr)
        return 2

    try:
        source_text = read_input(args.source)
        candidate_text = read_input(args.candidate)
    except OSError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    issues = check_fidelity(
        source_text,
        candidate_text,
        task=args.task,
        protect=args.protect,
        allow_change=args.allow_change,
        allow_dedup=args.allow_dedup,
    )

    if has_errors(issues):
        status = "fail"
        exit_code = 2
    elif has_warnings(issues):
        status = "warning"
        exit_code = 1
    else:
        status = "pass"
        exit_code = 0

    if args.format == "text":
        print(format_text_report(status, issues))
    else:
        print(json.dumps({"status": status, "issues": issues}, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
