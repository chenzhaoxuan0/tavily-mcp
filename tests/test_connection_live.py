from __future__ import annotations

from http import HTTPStatus

import pytest
from dedalus_mcp.testing import ConnectionTester, HttpMethod
from dedalus_mcp.testing import TestRequest as Req


@pytest.mark.asyncio
async def test_search_connection(tavily_tester: ConnectionTester) -> None:
    resp = await tavily_tester.request(
        Req(
            method=HttpMethod.POST,
            path="/search",
            body={
                "query": "hello world",
                "max_results": 1,
                "search_depth": "basic",
                "include_answer": True,
            },
        )
    )
    assert resp.success, f"Search probe failed: status={resp.status} body={resp.body!r}"
    assert resp.status == HTTPStatus.OK
    assert resp.body is not None
    assert "results" in resp.body


@pytest.mark.asyncio
async def test_extract_connection(tavily_tester: ConnectionTester) -> None:
    resp = await tavily_tester.request(
        Req(
            method=HttpMethod.POST,
            path="/extract",
            body={"urls": ["https://example.com"]},
        )
    )
    assert resp.success, f"Extract probe failed: status={resp.status} body={resp.body!r}"
    assert resp.status == HTTPStatus.OK
    assert resp.body is not None
