#!/usr/bin/env python3
"""Validate Anomaly string-table XML for its Windows-1251 runtime loader."""
from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "gamedata" / "configs" / "text"
MAX_ENGINE_LINE_BYTES = 4094


def main() -> int:
    errors: list[str] = []
    files = sorted(ROOT.rglob("*.xml"))
    ids_by_language: dict[str, set[str]] = {"eng": set(), "rus": set()}

    for path in files:
        raw = path.read_bytes()
        language = path.parent.name.casefold()
        if language not in ids_by_language:
            errors.append(f"{path}: unexpected language directory")
            continue
        lines = raw.splitlines()
        declaration = lines[0] if lines else b""
        if b'encoding="windows-1251"' not in declaration.lower():
            errors.append(f"{path}: expected windows-1251 declaration on line 1")
        try:
            text = raw.decode("cp1251", errors="strict")
        except UnicodeDecodeError as error:
            errors.append(f"{path}: invalid CP1251: {error}")
            continue
        for line_number, line in enumerate(lines, 1):
            if len(line) > MAX_ENGINE_LINE_BYTES:
                errors.append(f"{path}:{line_number}: engine line limit exceeded ({len(line)} bytes)")
        try:
            root = ET.fromstring(text)
        except ET.ParseError as error:
            errors.append(f"{path}: XML parse error: {error}")
            continue
        if root.tag != "string_table":
            errors.append(f"{path}: expected string_table root")
            continue
        local_ids: set[str] = set()
        for string in root.findall("string"):
            string_id = string.attrib.get("id")
            if not string_id:
                errors.append(f"{path}: string without id")
            elif string_id in local_ids:
                errors.append(f"{path}: duplicate id {string_id}")
            else:
                local_ids.add(string_id)
        duplicates = ids_by_language[language] & local_ids
        if duplicates:
            errors.append(f"{path}: duplicate IDs across files: {sorted(duplicates)}")
        ids_by_language[language].update(local_ids)

    missing_russian = ids_by_language["eng"] - ids_by_language["rus"]
    missing_english = ids_by_language["rus"] - ids_by_language["eng"]
    if missing_russian:
        errors.append(f"Missing Russian IDs: {sorted(missing_russian)}")
    if missing_english:
        errors.append(f"Missing English IDs: {sorted(missing_english)}")

    print(f"Checked {len(files)} localization XML files")
    if errors:
        print("FAIL")
        print("\n".join(errors))
        return 1
    print("PASS: CP1251, XML, line lengths, and EN/RU IDs are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

