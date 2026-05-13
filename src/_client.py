import asyncio
import os

import httpx
from dotenv import load_dotenv
from dedalus_mcp.client import BearerAuth, open_connection

load_dotenv()

AS_TOKEN_URL = "https://as.dedaluslabs.ai/oauth2/token"


async def _exchange_token(api_key: str) -> str:
    """Exchange Dedalus API key for a JWT access token via AS token-exchange."""
    async with httpx.AsyncClient() as http:
        resp = await http.post(
            AS_TOKEN_URL,
            data={
                "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
                "subject_token": api_key,
                "subject_token_type": "urn:ietf:params:oauth:token-type:api_key",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        resp.raise_for_status()
        return resp.json()["access_token"]


async def main() -> None:
    api_key = os.getenv("DEDALUS_API_KEY", "")
    if not api_key:
        raise SystemExit("DEDALUS_API_KEY not set")

    print("Exchanging API key for JWT...")
    jwt_token = await _exchange_token(api_key)
    print(f"Got JWT (len={len(jwt_token)})")

    auth = BearerAuth(access_token=jwt_token)
    async with open_connection("http://localhost:8080/mcp", auth=auth) as client:
        result = await client.list_tools()
        print("Available tools:")
        for t in result.tools:
            print(f"  - {t.name}: {t.description[:80]}...")
        print()

        print("--- tavily_search ---")
        result = await client.call_tool("tavily_search", {
            "query": "What is Dedalus Labs?",
            "max_results": 3,
        })
        print(result)
        print()

        print("--- tavily_extract ---")
        result = await client.call_tool("tavily_extract", {
            "urls": ["https://dedaluslabs.ai"],
        })
        print(result)
        print()

        print("--- tavily_qna_search ---")
        result = await client.call_tool("tavily_qna_search", {
            "query": "What is Model Context Protocol?",
        })
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
