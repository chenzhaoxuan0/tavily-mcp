from __future__ import annotations

import os

import pytest
from dedalus_mcp.testing import ConnectionTester
from dotenv import load_dotenv

from tavily import tavily_conn


@pytest.fixture(scope="session")
def tavily_tester() -> ConnectionTester:
    load_dotenv()
    if not os.getenv("TAVILY_API_KEY"):
        pytest.skip("TAVILY_API_KEY not set; skipping live connection tests")
    return ConnectionTester.from_env(tavily_conn)
