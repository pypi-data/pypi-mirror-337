import asyncio, importlib.metadata, mcp.server.stdio, mcp.server.websocket
from mcp.server import NotificationOptions
from mcp.server.models import InitializationOptions
from .common import MONDAY_API_KEY, logger, server, monday_client
from .tools import register_tools

async def main():
    
    # Log server startup
    logger.info("Starting Monday MCP server ...")
    
    # Register all available tools with the server
    register_tools(server, monday_client)

    # Start the standard I/O server with proper initialization
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        # Run the server with appropriate configuration
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="monday",
                server_version=importlib.metadata.version("mcp-monday-server"),
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    # Direct script execution entry point
    asyncio.run(main())