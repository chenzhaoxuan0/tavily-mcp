from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class SearchResult:
    success: bool
    query: str | None = None
    answer: str | None = None
    results: list[dict[str, Any]] = field(default_factory=list)
    error: str | None = None


@dataclass(frozen=True, slots=True)
class ExtractResult:
    success: bool
    results: list[dict[str, Any]] = field(default_factory=list)
    failed_results: list[dict[str, Any]] = field(default_factory=list)
    error: str | None = None
