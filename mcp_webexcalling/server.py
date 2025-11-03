"""MCP Server for Webex Calling"""

import asyncio
import sys
from typing import Any, Sequence, Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .webex_client import WebexClient
from .config import get_settings


# Initialize the MCP server
server = Server("webex-calling")
webex_client: Optional[WebexClient] = None


def get_client() -> WebexClient:
    """Get or create Webex client instance"""
    global webex_client
    if webex_client is None:
        settings = get_settings()
        webex_client = WebexClient(
            access_token=settings.webex_access_token,
            base_url=settings.webex_base_url,
        )
    return webex_client


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools"""
    return [
        Tool(
            name="get_organization_info",
            description="Get information about your Webex organization",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="list_locations",
            description="List all locations in your Webex organization",
            inputSchema={
                "type": "object",
                "properties": {
                    "org_id": {
                        "type": "string",
                        "description": "Optional organization ID to filter locations",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 100)",
                        "default": 100,
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="get_location_details",
            description="Get detailed information about a specific location",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_id": {
                        "type": "string",
                        "description": "The ID of the location",
                    },
                },
                "required": ["location_id"],
            },
        ),
        Tool(
            name="list_users",
            description="List users in your Webex organization",
            inputSchema={
                "type": "object",
                "properties": {
                    "org_id": {
                        "type": "string",
                        "description": "Optional organization ID to filter users",
                    },
                    "location_id": {
                        "type": "string",
                        "description": "Optional location ID to filter users",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 100)",
                        "default": 100,
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="get_user_details",
            description="Get detailed information about a specific user by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "person_id": {
                        "type": "string",
                        "description": "The ID of the user",
                    },
                },
                "required": ["person_id"],
            },
        ),
        Tool(
            name="get_user_by_email",
            description="Get user information by email address",
            inputSchema={
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "The email address of the user",
                    },
                },
                "required": ["email"],
            },
        ),
        Tool(
            name="get_user_calling_settings",
            description="Get calling settings for a specific user",
            inputSchema={
                "type": "object",
                "properties": {
                    "person_id": {
                        "type": "string",
                        "description": "The ID of the user",
                    },
                },
                "required": ["person_id"],
            },
        ),
        Tool(
            name="list_call_queues",
            description="List all call queues in your organization",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_id": {
                        "type": "string",
                        "description": "Optional location ID to filter call queues",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 100)",
                        "default": 100,
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="get_call_queue_details",
            description="Get detailed information about a specific call queue",
            inputSchema={
                "type": "object",
                "properties": {
                    "queue_id": {
                        "type": "string",
                        "description": "The ID of the call queue",
                    },
                },
                "required": ["queue_id"],
            },
        ),
        Tool(
            name="list_auto_attendants",
            description="List all auto attendants in your organization",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_id": {
                        "type": "string",
                        "description": "Optional location ID to filter auto attendants",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 100)",
                        "default": 100,
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="get_auto_attendant_details",
            description="Get detailed information about a specific auto attendant",
            inputSchema={
                "type": "object",
                "properties": {
                    "auto_attendant_id": {
                        "type": "string",
                        "description": "The ID of the auto attendant",
                    },
                },
                "required": ["auto_attendant_id"],
            },
        ),
        Tool(
            name="get_call_history",
            description="Get call history for a user or location",
            inputSchema={
                "type": "object",
                "properties": {
                    "person_id": {
                        "type": "string",
                        "description": "Optional user ID to filter call history",
                    },
                    "location_id": {
                        "type": "string",
                        "description": "Optional location ID to filter call history",
                    },
                    "start_time": {
                        "type": "string",
                        "description": "Optional start time in ISO 8601 format (e.g., 2024-01-01T00:00:00Z)",
                    },
                    "end_time": {
                        "type": "string",
                        "description": "Optional end time in ISO 8601 format (e.g., 2024-01-31T23:59:59Z)",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 100)",
                        "default": 100,
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="search_users",
            description="Search for users by display name or email address",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (display name or email)",
                    },
                    "org_id": {
                        "type": "string",
                        "description": "Optional organization ID to filter search",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 100)",
                        "default": 100,
                    },
                },
                "required": ["query"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> Sequence[TextContent]:
    """Handle tool calls"""
    client = get_client()

    try:
        if name == "get_organization_info":
            result = await client.get_organization_info()
            return [TextContent(type="text", text=format_json(result))]

        elif name == "list_locations":
            org_id = arguments.get("org_id")
            max_results = arguments.get("max_results", 100)
            result = await client.list_locations(org_id=org_id, max_results=max_results)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "get_location_details":
            location_id = arguments["location_id"]
            result = await client.get_location_details(location_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "list_users":
            org_id = arguments.get("org_id")
            location_id = arguments.get("location_id")
            max_results = arguments.get("max_results", 100)
            result = await client.list_users(
                org_id=org_id, location_id=location_id, max_results=max_results
            )
            return [TextContent(type="text", text=format_json(result))]

        elif name == "get_user_details":
            person_id = arguments["person_id"]
            result = await client.get_user_details(person_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "get_user_by_email":
            email = arguments["email"]
            result = await client.get_user_by_email(email)
            if result:
                return [TextContent(type="text", text=format_json(result))]
            else:
                return [TextContent(type="text", text=f"User with email {email} not found")]

        elif name == "get_user_calling_settings":
            person_id = arguments["person_id"]
            result = await client.get_user_calling_settings(person_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "list_call_queues":
            location_id = arguments.get("location_id")
            max_results = arguments.get("max_results", 100)
            result = await client.list_call_queues(location_id=location_id, max_results=max_results)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "get_call_queue_details":
            queue_id = arguments["queue_id"]
            result = await client.get_call_queue_details(queue_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "list_auto_attendants":
            location_id = arguments.get("location_id")
            max_results = arguments.get("max_results", 100)
            result = await client.list_auto_attendants(
                location_id=location_id, max_results=max_results
            )
            return [TextContent(type="text", text=format_json(result))]

        elif name == "get_auto_attendant_details":
            auto_attendant_id = arguments["auto_attendant_id"]
            result = await client.get_auto_attendant_details(auto_attendant_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "get_call_history":
            person_id = arguments.get("person_id")
            location_id = arguments.get("location_id")
            start_time = arguments.get("start_time")
            end_time = arguments.get("end_time")
            max_results = arguments.get("max_results", 100)
            result = await client.get_call_history(
                person_id=person_id,
                location_id=location_id,
                start_time=start_time,
                end_time=end_time,
                max_results=max_results,
            )
            return [TextContent(type="text", text=format_json(result))]

        elif name == "search_users":
            query = arguments["query"]
            org_id = arguments.get("org_id")
            max_results = arguments.get("max_results", 100)
            result = await client.search_users(query=query, org_id=org_id, max_results=max_results)
            return [TextContent(type="text", text=format_json(result))]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        error_msg = f"Error calling {name}: {str(e)}"
        return [TextContent(type="text", text=error_msg)]


def format_json(data: Any) -> str:
    """Format data as JSON string"""
    import json

    return json.dumps(data, indent=2, default=str)


async def main():
    """Main entry point for the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())

