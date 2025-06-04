from __future__ import annotations

from pathlib import Path


def load_guardrails(path: str | Path) -> list[str]:
    with open(path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def approve(draft: str, guardrails: list[str]) -> tuple[bool, str]:
    for banned in guardrails:
        if banned.lower() in draft.lower():
            return False, f"Found disallowed term: {banned}"
    return True, "Approved"
