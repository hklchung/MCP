from pathlib import Path
from typing import Iterable


def read_guardrails(path: str | Path) -> list[str]:
    with open(path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def write_guardrails(path: str | Path, lines: Iterable[str]) -> None:
    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))
