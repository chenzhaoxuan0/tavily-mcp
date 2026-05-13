import os

from dedalus_mcp import MCPServer
from dedalus_mcp.server import TransportSecuritySettings

from tavily import tavily_connections, tavily_tools


def create_server() -> MCPServer:
    as_url = os.getenv("DEDALUS_AS_URL", "https://as.dedaluslabs.ai")
    return MCPServer(
        name="tavily-mcp",
        connections=tavily_connections,
        http_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
        streamable_http_stateless=True,
        authorization_server=as_url,
    )


async def main() -> None:
    server = create_server()
    server.collect(*tavily_tools)
    await server.serve(port=8080)
