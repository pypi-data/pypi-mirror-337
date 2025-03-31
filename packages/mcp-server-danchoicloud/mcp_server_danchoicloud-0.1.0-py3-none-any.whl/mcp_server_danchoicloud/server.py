from typing import Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent

from mcp_server_danchoicloud.tools.sieu_nhan import SieuNhanTools, get_sieu_nhan_tools


async def serve() -> None:
    server = Server('mcp_server_danchoicloud', 'v0.1.0')

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available tools."""
        return [
            Tool(
                name=SieuNhanTools.GET_SIEU_NHAN.value,
                description="Get a random superhero from the API.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The text to display.",
                        },
                    },
                    "required": ["text"],
                }
            )
        ]

    @server.call_tool()
    async def handle_call_tool(
            name: str, arguments: dict | None
    ) -> Sequence[TextContent | ImageContent]:
        """Handle tool calls."""
        try:
            match name:
                case SieuNhanTools.GET_SIEU_NHAN.value:
                    result = await get_sieu_nhan_tools()
                case _:
                    raise ValueError(f"Unknown tool: {name}")
            return [result]
        except Exception as e:
            raise ValueError(f"Error processing mcp_server_danchoicloud query: {str(e)}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options)
