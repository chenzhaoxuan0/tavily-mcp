# tavily-mcp

A web search and extraction MCP server powered by [Tavily](https://tavily.com), built on [Dedalus](https://dedaluslabs.ai).

## Tools

| Tool | Description |
|------|-------------|
| `tavily_search` | Search the web with AI-generated answer synthesis |
| `tavily_extract` | Extract clean content from URLs |
| `tavily_qna_search` | Ask a question and get a direct answer with sources |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TAVILY_API_KEY` | Yes | Tavily API key (`tvly-...`) |
| `DEDALUS_API_KEY` | Yes | Dedalus platform API key |
| `DEDALUS_API_URL` | No | Dedalus API base URL |
| `DEDALUS_AS_URL` | No | Dedalus auth server URL (default: `https://as.dedaluslabs.ai`) |

## Quick Start

```bash
# Install dependencies
uv sync

# Set environment variables
cp .env.example .env
# Edit .env with your keys

# Run the server
uv run python src/main.py
```

## Testing

```bash
# Unit tests (no API key needed)
uv run pytest tests/test_tools.py

# Live connection tests (requires TAVILY_API_KEY)
uv run pytest tests/test_connection_live.py
```

## Source Decision

**Decision: Build native (Python)**

The official `tavily-ai/tavily-mcp` is implemented in TypeScript using `@modelcontextprotocol/sdk`. Since our infrastructure requires Python with Dedalus DAuth integration, we build natively using `dedalus-mcp`. The official implementation served as a functional specification for tool definitions and API endpoints.

## License

MIT
