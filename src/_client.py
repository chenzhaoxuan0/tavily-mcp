import asyncio
import os

from dotenv import load_dotenv
from dedalus_mcp.client import MCPClient

load_dotenv()


async def main() -> None:
    async with MCPClient("http://localhost:8080/mcp") as client:
        # List available tools
        tools = await client.list_tools()
        print("Available tools:")
        for t in tools:
            print(f"  - {t.name}: {t.description[:80]}...")
        print()

        # Test tavily_search
        print("--- tavily_search ---")
        result = await client.call_tool("tavily_search", {
            "query": "What is Dedalus Labs?",
            "max_results": 3,
        })
        print(result)
        print()

        # Test tavily_extract
        print("--- tavily_extract ---")
        result = await client.call_tool("tavily_extract", {
            "urls": ["https://dedaluslabs.ai"],
        })
        print(result)
        print()

        # Test tavily_qna_search
        print("--- tavily_qna_search ---")
        result = await client.call_tool("tavily_qna_search", {
            "query": "What is Model Context Protocol?",
        })
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
