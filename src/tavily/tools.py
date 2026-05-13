from __future__ import annotations

from typing import Any

from dedalus_mcp import HttpMethod, HttpRequest, get_context, tool
from dedalus_mcp.auth import Connection, SecretKeys
from dedalus_mcp.types import ToolAnnotations

from tavily.types import ExtractResult, SearchResult

# --- Connection ---

_BASE_URL = "https://api.tavily.com"

tavily_conn = Connection(
    name="tavily",
    secrets=SecretKeys(token="TAVILY_API_KEY"),
    base_url=_BASE_URL,
    auth_header_format="Bearer {api_key}",
)

tavily_connections = [tavily_conn]


# --- Transport ---


async def _dispatch(path: str, body: dict[str, Any]) -> tuple[dict[str, Any], str | None]:
    ctx = get_context()
    resp = await ctx.dispatch(
        "tavily",
        HttpRequest(method=HttpMethod.POST, path=path, body=body),
    )
    if resp.success and resp.response is not None:
        raw = resp.response.body
        return raw if isinstance(raw, dict) else {}, None
    return {}, resp.error.message if resp.error else "Tavily request failed"


# --- Tools ---


@tool(
    description=(
        "Search the web using Tavily. Returns relevant results with AI-generated answer. "
        "Use for finding current information, news, articles, and general web content."
    ),
    tags=["search", "read"],
    annotations=ToolAnnotations(readOnlyHint=True),
)
async def tavily_search(
    query: str,
    max_results: int = 5,
    search_depth: str = "basic",
) -> SearchResult:
    """Search the web.

    Args:
        query: Natural language search query
        max_results: Maximum results to return (1-10, default 5)
        search_depth: "basic" for speed, "advanced" for depth

    Returns:
        SearchResult with answer and list of result dicts
    """
    raw, error = await _dispatch(
        "/search",
        {
            "query": query,
            "max_results": max(1, min(10, max_results)),
            "search_depth": search_depth,
            "include_answer": True,
        },
    )
    if error:
        return SearchResult(success=False, error=error)
    return SearchResult(
        success=True,
        query=raw.get("query"),
        answer=raw.get("answer"),
        results=raw.get("results", []),
    )


@tool(
    description=(
        "Extract clean content from one or more URLs. "
        "Returns parsed text/markdown from web pages, articles, documentation, etc."
    ),
    tags=["extract", "read"],
    annotations=ToolAnnotations(readOnlyHint=True),
)
async def tavily_extract(
    urls: list[str],
) -> ExtractResult:
    """Extract content from URLs.

    Args:
        urls: URLs to extract content from (1-10)

    Returns:
        ExtractResult with extracted content per URL
    """
    raw, error = await _dispatch(
        "/extract",
        {"urls": urls[:10]},
    )
    if error:
        return ExtractResult(success=False, error=error)
    return ExtractResult(
        success=True,
        results=raw.get("results", []),
        failed_results=raw.get("failed_results", []),
    )


@tool(
    description=(
        "Ask a question and get a direct answer with sources. "
        "Optimized for Q&A — returns a concise synthesized answer backed by web search."
    ),
    tags=["search", "qna", "read"],
    annotations=ToolAnnotations(readOnlyHint=True),
)
async def tavily_qna_search(
    query: str,
) -> SearchResult:
    """Ask a question, get an answer.

    Args:
        query: Natural language question

    Returns:
        SearchResult with synthesized answer and source results
    """
    raw, error = await _dispatch(
        "/search",
        {
            "query": query,
            "search_depth": "advanced",
            "include_answer": True,
            "max_results": 5,
        },
    )
    if error:
        return SearchResult(success=False, error=error)
    return SearchResult(
        success=True,
        query=raw.get("query"),
        answer=raw.get("answer"),
        results=raw.get("results", []),
    )


# --- Export ---

tavily_tools = [
    tavily_search,
    tavily_extract,
    tavily_qna_search,
]
