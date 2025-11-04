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
        # License Management Tools
        Tool(
            name="list_licenses",
            description="List all licenses in your organization",
            inputSchema={
                "type": "object",
                "properties": {
                    "org_id": {
                        "type": "string",
                        "description": "Optional organization ID to filter licenses",
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
            name="get_license_details",
            description="Get details about a specific license",
            inputSchema={
                "type": "object",
                "properties": {
                    "license_id": {
                        "type": "string",
                        "description": "The ID of the license",
                    },
                },
                "required": ["license_id"],
            },
        ),
        Tool(
            name="list_user_licenses",
            description="List licenses assigned to a user",
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
            name="assign_license_to_user",
            description="Assign a license to a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "person_id": {
                        "type": "string",
                        "description": "The ID of the user",
                    },
                    "license_id": {
                        "type": "string",
                        "description": "The ID of the license to assign",
                    },
                },
                "required": ["person_id", "license_id"],
            },
        ),
        Tool(
            name="remove_license_from_user",
            description="Remove a license from a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "person_id": {
                        "type": "string",
                        "description": "The ID of the user",
                    },
                    "license_id": {
                        "type": "string",
                        "description": "The ID of the license to remove",
                    },
                },
                "required": ["person_id", "license_id"],
            },
        ),
        # Device Management Tools
        Tool(
            name="list_devices",
            description="List devices in your organization",
            inputSchema={
                "type": "object",
                "properties": {
                    "person_id": {
                        "type": "string",
                        "description": "Optional user ID to filter devices",
                    },
                    "location_id": {
                        "type": "string",
                        "description": "Optional location ID to filter devices",
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
            name="get_device_details",
            description="Get details about a specific device",
            inputSchema={
                "type": "object",
                "properties": {
                    "device_id": {
                        "type": "string",
                        "description": "The ID of the device",
                    },
                },
                "required": ["device_id"],
            },
        ),
        # Phone Number Tools
        Tool(
            name="list_phone_numbers",
            description="List phone numbers in your organization",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_id": {
                        "type": "string",
                        "description": "Optional location ID to filter phone numbers",
                    },
                    "org_id": {
                        "type": "string",
                        "description": "Optional organization ID to filter phone numbers",
                    },
                    "number": {
                        "type": "string",
                        "description": "Optional phone number to search for",
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
            name="get_phone_number_details",
            description="Get details about a specific phone number",
            inputSchema={
                "type": "object",
                "properties": {
                    "number_id": {
                        "type": "string",
                        "description": "The ID of the phone number",
                    },
                },
                "required": ["number_id"],
            },
        ),
        # User Extension Management Tools
        Tool(
            name="update_user_extension",
            description="Update user extension and calling settings",
            inputSchema={
                "type": "object",
                "properties": {
                    "person_id": {
                        "type": "string",
                        "description": "The ID of the user",
                    },
                    "extension": {
                        "type": "string",
                        "description": "Optional extension number to set",
                    },
                    "extension_dial": {
                        "type": "string",
                        "description": "Optional extension dial string",
                    },
                    "first_name": {
                        "type": "string",
                        "description": "Optional first name",
                    },
                    "last_name": {
                        "type": "string",
                        "description": "Optional last name",
                    },
                    "phone_number": {
                        "type": "string",
                        "description": "Optional phone number",
                    },
                    "mobile_number": {
                        "type": "string",
                        "description": "Optional mobile number",
                    },
                    "location_id": {
                        "type": "string",
                        "description": "Optional location ID",
                    },
                },
                "required": ["person_id"],
            },
        ),
        Tool(
            name="assign_phone_number_to_user",
            description="Assign a phone number to a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "person_id": {
                        "type": "string",
                        "description": "The ID of the user",
                    },
                    "phone_number_id": {
                        "type": "string",
                        "description": "The ID of the phone number to assign",
                    },
                },
                "required": ["person_id", "phone_number_id"],
            },
        ),
        Tool(
            name="update_user_calling_features",
            description="Update user calling features (call park, forwarding, voicemail, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "person_id": {
                        "type": "string",
                        "description": "The ID of the user",
                    },
                    "call_park_enabled": {
                        "type": "boolean",
                        "description": "Enable/disable call park",
                    },
                    "call_forwarding_enabled": {
                        "type": "boolean",
                        "description": "Enable/disable call forwarding",
                    },
                    "voicemail_enabled": {
                        "type": "boolean",
                        "description": "Enable/disable voicemail",
                    },
                    "call_recording_enabled": {
                        "type": "boolean",
                        "description": "Enable/disable call recording",
                    },
                    "call_waiting_enabled": {
                        "type": "boolean",
                        "description": "Enable/disable call waiting",
                    },
                },
                "required": ["person_id"],
            },
        ),
        # Reporting and Analytics Tools
        Tool(
            name="get_call_detail_records",
            description="Get call detail records (CDRs) for reporting",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_time": {
                        "type": "string",
                        "description": "Start time in ISO 8601 format (e.g., 2024-01-01T00:00:00Z)",
                    },
                    "end_time": {
                        "type": "string",
                        "description": "End time in ISO 8601 format (e.g., 2024-01-31T23:59:59Z)",
                    },
                    "person_id": {
                        "type": "string",
                        "description": "Optional user ID to filter records",
                    },
                    "location_id": {
                        "type": "string",
                        "description": "Optional location ID to filter records",
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
            name="get_call_analytics",
            description="Get call analytics and statistics for a time period",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_time": {
                        "type": "string",
                        "description": "Start time in ISO 8601 format (e.g., 2024-01-01T00:00:00Z)",
                    },
                    "end_time": {
                        "type": "string",
                        "description": "End time in ISO 8601 format (e.g., 2024-01-31T23:59:59Z)",
                    },
                    "location_id": {
                        "type": "string",
                        "description": "Optional location ID to filter analytics",
                    },
                    "org_id": {
                        "type": "string",
                        "description": "Optional organization ID to filter analytics",
                    },
                },
                "required": ["start_time", "end_time"],
            },
        ),
        Tool(
            name="get_queue_analytics",
            description="Get analytics for a specific call queue",
            inputSchema={
                "type": "object",
                "properties": {
                    "queue_id": {
                        "type": "string",
                        "description": "The ID of the call queue",
                    },
                    "start_time": {
                        "type": "string",
                        "description": "Start time in ISO 8601 format (e.g., 2024-01-01T00:00:00Z)",
                    },
                    "end_time": {
                        "type": "string",
                        "description": "End time in ISO 8601 format (e.g., 2024-01-31T23:59:59Z)",
                    },
                },
                "required": ["queue_id", "start_time", "end_time"],
            },
        ),
        # Additional Data Retrieval Tools
        Tool(
            name="list_trunk_groups",
            description="List trunk groups in your organization",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_id": {
                        "type": "string",
                        "description": "Optional location ID to filter trunk groups",
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
            name="get_trunk_group_details",
            description="Get details about a specific trunk group",
            inputSchema={
                "type": "object",
                "properties": {
                    "trunk_group_id": {
                        "type": "string",
                        "description": "The ID of the trunk group",
                    },
                },
                "required": ["trunk_group_id"],
            },
        ),
        Tool(
            name="list_hunt_groups",
            description="List hunt groups in your organization",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_id": {
                        "type": "string",
                        "description": "Optional location ID to filter hunt groups",
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
            name="get_hunt_group_details",
            description="Get details about a specific hunt group",
            inputSchema={
                "type": "object",
                "properties": {
                    "hunt_group_id": {
                        "type": "string",
                        "description": "The ID of the hunt group",
                    },
                },
                "required": ["hunt_group_id"],
            },
        ),
        Tool(
            name="list_call_park_extensions",
            description="List call park extensions in your organization",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_id": {
                        "type": "string",
                        "description": "Optional location ID to filter call park extensions",
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
            name="get_location_features",
            description="Get available features for a location",
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

        # License Management
        elif name == "list_licenses":
            org_id = arguments.get("org_id")
            max_results = arguments.get("max_results", 100)
            result = await client.list_licenses(org_id=org_id, max_results=max_results)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "get_license_details":
            license_id = arguments["license_id"]
            result = await client.get_license_details(license_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "list_user_licenses":
            person_id = arguments["person_id"]
            result = await client.list_user_licenses(person_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "assign_license_to_user":
            person_id = arguments["person_id"]
            license_id = arguments["license_id"]
            result = await client.assign_license_to_user(person_id, license_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "remove_license_from_user":
            person_id = arguments["person_id"]
            license_id = arguments["license_id"]
            result = await client.remove_license_from_user(person_id, license_id)
            return [TextContent(type="text", text=format_json(result))]

        # Device Management
        elif name == "list_devices":
            person_id = arguments.get("person_id")
            location_id = arguments.get("location_id")
            max_results = arguments.get("max_results", 100)
            result = await client.list_devices(
                person_id=person_id, location_id=location_id, max_results=max_results
            )
            return [TextContent(type="text", text=format_json(result))]

        elif name == "get_device_details":
            device_id = arguments["device_id"]
            result = await client.get_device_details(device_id)
            return [TextContent(type="text", text=format_json(result))]

        # Phone Numbers
        elif name == "list_phone_numbers":
            location_id = arguments.get("location_id")
            org_id = arguments.get("org_id")
            number = arguments.get("number")
            max_results = arguments.get("max_results", 100)
            result = await client.list_phone_numbers(
                location_id=location_id, org_id=org_id, number=number, max_results=max_results
            )
            return [TextContent(type="text", text=format_json(result))]

        elif name == "get_phone_number_details":
            number_id = arguments["number_id"]
            result = await client.get_phone_number_details(number_id)
            return [TextContent(type="text", text=format_json(result))]

        # User Extension Management
        elif name == "update_user_extension":
            person_id = arguments["person_id"]
            extension = arguments.get("extension")
            extension_dial = arguments.get("extension_dial")
            first_name = arguments.get("first_name")
            last_name = arguments.get("last_name")
            phone_number = arguments.get("phone_number")
            mobile_number = arguments.get("mobile_number")
            location_id = arguments.get("location_id")
            result = await client.update_user_extension(
                person_id=person_id,
                extension=extension,
                extension_dial=extension_dial,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                mobile_number=mobile_number,
                location_id=location_id,
            )
            return [TextContent(type="text", text=format_json(result))]

        elif name == "assign_phone_number_to_user":
            person_id = arguments["person_id"]
            phone_number_id = arguments["phone_number_id"]
            result = await client.assign_phone_number_to_user(person_id, phone_number_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "update_user_calling_features":
            person_id = arguments["person_id"]
            call_park_enabled = arguments.get("call_park_enabled")
            call_forwarding_enabled = arguments.get("call_forwarding_enabled")
            voicemail_enabled = arguments.get("voicemail_enabled")
            call_recording_enabled = arguments.get("call_recording_enabled")
            call_waiting_enabled = arguments.get("call_waiting_enabled")
            result = await client.update_user_calling_features(
                person_id=person_id,
                call_park_enabled=call_park_enabled,
                call_forwarding_enabled=call_forwarding_enabled,
                voicemail_enabled=voicemail_enabled,
                call_recording_enabled=call_recording_enabled,
                call_waiting_enabled=call_waiting_enabled,
            )
            return [TextContent(type="text", text=format_json(result))]

        # Reporting and Analytics
        elif name == "get_call_detail_records":
            start_time = arguments.get("start_time")
            end_time = arguments.get("end_time")
            person_id = arguments.get("person_id")
            location_id = arguments.get("location_id")
            max_results = arguments.get("max_results", 100)
            result = await client.get_call_detail_records(
                start_time=start_time,
                end_time=end_time,
                person_id=person_id,
                location_id=location_id,
                max_results=max_results,
            )
            return [TextContent(type="text", text=format_json(result))]

        elif name == "get_call_analytics":
            start_time = arguments["start_time"]
            end_time = arguments["end_time"]
            location_id = arguments.get("location_id")
            org_id = arguments.get("org_id")
            result = await client.get_call_analytics(
                start_time=start_time,
                end_time=end_time,
                location_id=location_id,
                org_id=org_id,
            )
            return [TextContent(type="text", text=format_json(result))]

        elif name == "get_queue_analytics":
            queue_id = arguments["queue_id"]
            start_time = arguments["start_time"]
            end_time = arguments["end_time"]
            result = await client.get_queue_analytics(
                queue_id=queue_id, start_time=start_time, end_time=end_time
            )
            return [TextContent(type="text", text=format_json(result))]

        # Additional Data Retrieval
        elif name == "list_trunk_groups":
            location_id = arguments.get("location_id")
            max_results = arguments.get("max_results", 100)
            result = await client.list_trunk_groups(location_id=location_id, max_results=max_results)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "get_trunk_group_details":
            trunk_group_id = arguments["trunk_group_id"]
            result = await client.get_trunk_group_details(trunk_group_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "list_hunt_groups":
            location_id = arguments.get("location_id")
            max_results = arguments.get("max_results", 100)
            result = await client.list_hunt_groups(location_id=location_id, max_results=max_results)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "get_hunt_group_details":
            hunt_group_id = arguments["hunt_group_id"]
            result = await client.get_hunt_group_details(hunt_group_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "list_call_park_extensions":
            location_id = arguments.get("location_id")
            max_results = arguments.get("max_results", 100)
            result = await client.list_call_park_extensions(
                location_id=location_id, max_results=max_results
            )
            return [TextContent(type="text", text=format_json(result))]

        elif name == "get_location_features":
            location_id = arguments["location_id"]
            result = await client.get_location_features(location_id)
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

