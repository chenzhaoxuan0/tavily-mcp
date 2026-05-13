from __future__ import annotations

from typing import Any

import pytest

from tavily import ExtractResult, SearchResult, tavily_extract, tavily_qna_search, tavily_search


# --- tavily_search ---


@pytest.mark.asyncio
async def test_search_builds_correct_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}

    async def fake_dispatch(path: str, body: dict[str, Any]) -> tuple[dict[str, Any], str | None]:
        captured["path"] = path
        captured["body"] = body
        return {
            "query": "test query",
            "answer": "AI answer",
            "results": [{"url": "https://example.com", "title": "Example", "content": "text"}],
        }, None

    monkeypatch.setattr("tavily.tools._dispatch", fake_dispatch)
    result = await tavily_search(query="test query", max_results=3)

    assert isinstance(result, SearchResult)
    assert result.success
    assert result.answer == "AI answer"
    assert len(result.results) == 1
    assert captured["path"] == "/search"
    assert captured["body"]["query"] == "test query"
    assert captured["body"]["max_results"] == 3
    assert captured["body"]["include_answer"] is True


@pytest.mark.asyncio
async def test_search_clamps_max_results(monkeypatch: pytest.MonkeyPatch) -> None:
    bodies: list[dict[str, Any]] = []

    async def fake_dispatch(_path: str, body: dict[str, Any]) -> tuple[dict[str, Any], str | None]:
        bodies.append(body)
        return {"results": []}, None

    monkeypatch.setattr("tavily.tools._dispatch", fake_dispatch)

    await tavily_search(query="x", max_results=-5)
    await tavily_search(query="x", max_results=999)

    assert bodies[0]["max_results"] == 1
    assert bodies[1]["max_results"] == 10


@pytest.mark.asyncio
async def test_search_surfaces_error(monkeypatch: pytest.MonkeyPatch) -> None:

    async def fake_dispatch(_path: str, _body: dict[str, Any]) -> tuple[dict[str, Any], str | None]:
        return {}, "rate limited"

    monkeypatch.setattr("tavily.tools._dispatch", fake_dispatch)
    result = await tavily_search(query="anything")

    assert isinstance(result, SearchResult)
    assert not result.success
    assert result.error == "rate limited"


# --- tavily_extract ---


@pytest.mark.asyncio
async def test_extract_builds_correct_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}

    async def fake_dispatch(path: str, body: dict[str, Any]) -> tuple[dict[str, Any], str | None]:
        captured["path"] = path
        captured["body"] = body
        return {
            "results": [{"url": "https://example.com", "text": "extracted content"}],
            "failed_results": [],
        }, None

    monkeypatch.setattr("tavily.tools._dispatch", fake_dispatch)
    result = await tavily_extract(urls=["https://example.com"])

    assert isinstance(result, ExtractResult)
    assert result.success
    assert len(result.results) == 1
    assert len(result.failed_results) == 0
    assert captured["path"] == "/extract"
    assert captured["body"]["urls"] == ["https://example.com"]


@pytest.mark.asyncio
async def test_extract_truncates_urls(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}

    async def fake_dispatch(_path: str, body: dict[str, Any]) -> tuple[dict[str, Any], str | None]:
        captured.update(body)
        return {"results": [], "failed_results": []}, None

    monkeypatch.setattr("tavily.tools._dispatch", fake_dispatch)
    await tavily_extract(urls=[f"https://example.com/{i}" for i in range(20)])

    assert len(captured["urls"]) == 10


@pytest.mark.asyncio
async def test_extract_surfaces_error(monkeypatch: pytest.MonkeyPatch) -> None:

    async def fake_dispatch(_path: str, _body: dict[str, Any]) -> tuple[dict[str, Any], str | None]:
        return {}, "unauthorized"

    monkeypatch.setattr("tavily.tools._dispatch", fake_dispatch)
    result = await tavily_extract(urls=["https://example.com"])

    assert not result.success
    assert result.error == "unauthorized"


# --- tavily_qna_search ---


@pytest.mark.asyncio
async def test_qna_sends_advanced_depth(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}

    async def fake_dispatch(path: str, body: dict[str, Any]) -> tuple[dict[str, Any], str | None]:
        captured["path"] = path
        captured["body"] = body
        return {
            "query": "What is MCP?",
            "answer": "Model Context Protocol is...",
            "results": [{"url": "https://example.com/mcp"}],
        }, None

    monkeypatch.setattr("tavily.tools._dispatch", fake_dispatch)
    result = await tavily_qna_search(query="What is MCP?")

    assert isinstance(result, SearchResult)
    assert result.success
    assert result.answer == "Model Context Protocol is..."
    assert captured["body"]["search_depth"] == "advanced"
    assert captured["body"]["include_answer"] is True


@pytest.mark.asyncio
async def test_qna_surfaces_error(monkeypatch: pytest.MonkeyPatch) -> None:

    async def fake_dispatch(_path: str, _body: dict[str, Any]) -> tuple[dict[str, Any], str | None]:
        return {}, "server error"

    monkeypatch.setattr("tavily.tools._dispatch", fake_dispatch)
    result = await tavily_qna_search(query="anything")

    assert not result.success
    assert result.error == "server error"
