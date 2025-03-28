# -*- coding: utf-8 -*-
# server.py
# Copyright (c) 2025 zedmoster

from contextlib import asynccontextmanager
from typing import AsyncIterator, Dict, Any
from mcp.server.fastmcp import FastMCP
from .revit_connection import RevitConnection
from .tools import *

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("RevitMCPServer")

# Global connection for resources
_Revit_connection = None
_polyhaven_enabled = False
_port = 8080


def get_Revit_connection():
    """Get or create a persistent Revit connection"""
    global _Revit_connection, _polyhaven_enabled

    if _Revit_connection is not None:
        try:
            result = _Revit_connection.send_command("get_polyhaven_status")
            _polyhaven_enabled = result.get("enabled", False)
            return _Revit_connection
        except Exception as e:
            logger.warning(f"Existing connection is no longer valid: {str(e)}")
            try:
                _Revit_connection.disconnect()
            except:
                pass
            _Revit_connection = None

    if _Revit_connection is None:
        _Revit_connection = RevitConnection(host="localhost", port=_port)
        if not _Revit_connection.connect():
            logger.error("Failed to connect to Revit")
            _Revit_connection = None
            raise Exception(
                "Could not connect to Revit. Make sure the Revit addon is running.")
        logger.info("Created new persistent connection to Revit")

    return _Revit_connection


@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[Dict[str, Any]]:
    """Manage server startup and shutdown lifecycle"""
    try:
        logger.info("RevitMCP server starting up")
        try:
            Revit = get_Revit_connection()
            logger.info("Successfully connected to Revit on startup")
        except Exception as e:
            logger.warning(f"Could not connect to Revit on startup: {str(e)}")
            logger.warning(
                "Make sure the Revit addon is running before using Revit resources or tools")

        yield {}
    finally:
        global _Revit_connection
        if _Revit_connection:
            logger.info("Disconnecting from Revit on shutdown")
            _Revit_connection.disconnect()
            _Revit_connection = None
        logger.info("RevitMCP server shut down")


# Create the MCP server with lifespan support
mcp = FastMCP(
    "RevitMCP",
    description="Revit integration through the Model Context Protocol",
    lifespan=server_lifespan
)

# Register tools
mcp.tool()(create_levels)
mcp.tool()(create_grids)
mcp.tool()(create_walls)
mcp.tool()(create_floors)
mcp.tool()(create_rooms)
mcp.tool()(create_room_tags)
mcp.tool()(create_family_instances)
mcp.tool()(find_elements)
mcp.tool()(update_elements)
mcp.tool()(delete_elements)
mcp.tool()(parameter_elements)
mcp.tool()(get_location)
mcp.tool()(show_elements)
mcp.tool()(active_view)
mcp.tool()(call_func)


def main():
    """Run the MCP server"""
    mcp.run()


if __name__ == "__main__":
    main()
