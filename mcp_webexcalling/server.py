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
        # Enhanced Device Management Tools
        Tool(
            name="associate_device_to_user",
            description="Associate a device to a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "device_id": {"type": "string", "description": "The device ID"},
                    "person_id": {"type": "string", "description": "The user ID"},
                },
                "required": ["device_id", "person_id"],
            },
        ),
        Tool(
            name="unassociate_device",
            description="Unassociate a device from a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "device_id": {"type": "string", "description": "The device ID"},
                },
                "required": ["device_id"],
            },
        ),
        Tool(
            name="provision_device",
            description="Provision a device for a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "device_id": {"type": "string", "description": "The device ID"},
                    "person_id": {"type": "string", "description": "The user ID"},
                    "location_id": {"type": "string", "description": "The location ID"},
                },
                "required": ["device_id", "person_id", "location_id"],
            },
        ),
        Tool(
            name="activate_device",
            description="Activate a device",
            inputSchema={
                "type": "object",
                "properties": {
                    "device_id": {"type": "string", "description": "The device ID"},
                },
                "required": ["device_id"],
            },
        ),
        Tool(
            name="deactivate_device",
            description="Deactivate a device",
            inputSchema={
                "type": "object",
                "properties": {
                    "device_id": {"type": "string", "description": "The device ID"},
                },
                "required": ["device_id"],
            },
        ),
        Tool(
            name="get_device_associations",
            description="Get device associations and status",
            inputSchema={
                "type": "object",
                "properties": {
                    "device_id": {"type": "string", "description": "The device ID"},
                },
                "required": ["device_id"],
            },
        ),
        Tool(
            name="list_user_devices",
            description="List all devices associated with a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "person_id": {"type": "string", "description": "The user ID"},
                },
                "required": ["person_id"],
            },
        ),
        # Location CRUD Operations
        Tool(
            name="create_location",
            description="Create a new location",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Location name"},
                    "address": {"type": "object", "description": "Address object"},
                    "org_id": {"type": "string", "description": "Organization ID"},
                    "emergency_location": {"type": "boolean", "description": "Emergency location flag"},
                },
                "required": ["name", "address"],
            },
        ),
        Tool(
            name="update_location",
            description="Update a location",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_id": {"type": "string", "description": "Location ID"},
                    "name": {"type": "string", "description": "Location name"},
                    "address": {"type": "object", "description": "Address object"},
                    "emergency_location": {"type": "boolean", "description": "Emergency location flag"},
                },
                "required": ["location_id"],
            },
        ),
        Tool(
            name="delete_location",
            description="Delete a location",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_id": {"type": "string", "description": "Location ID"},
                },
                "required": ["location_id"],
            },
        ),
        # User CRUD Operations
        Tool(
            name="create_user",
            description="Create a new user",
            inputSchema={
                "type": "object",
                "properties": {
                    "emails": {"type": "array", "items": {"type": "string"}, "description": "User email addresses"},
                    "display_name": {"type": "string", "description": "Display name"},
                    "first_name": {"type": "string", "description": "First name"},
                    "last_name": {"type": "string", "description": "Last name"},
                    "org_id": {"type": "string", "description": "Organization ID"},
                    "location_id": {"type": "string", "description": "Location ID"},
                },
                "required": ["emails", "display_name"],
            },
        ),
        Tool(
            name="update_user",
            description="Update a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "person_id": {"type": "string", "description": "User ID"},
                    "display_name": {"type": "string", "description": "Display name"},
                    "first_name": {"type": "string", "description": "First name"},
                    "last_name": {"type": "string", "description": "Last name"},
                    "emails": {"type": "array", "items": {"type": "string"}, "description": "Email addresses"},
                    "location_id": {"type": "string", "description": "Location ID"},
                },
                "required": ["person_id"],
            },
        ),
        Tool(
            name="delete_user",
            description="Delete a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "person_id": {"type": "string", "description": "User ID"},
                },
                "required": ["person_id"],
            },
        ),
        # Call Queue Management
        Tool(
            name="create_call_queue",
            description="Create a new call queue",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Queue name"},
                    "location_id": {"type": "string", "description": "Location ID"},
                    "phone_number": {"type": "string", "description": "Phone number"},
                    "call_policies": {"type": "object", "description": "Call policies"},
                },
                "required": ["name", "location_id"],
            },
        ),
        Tool(
            name="update_call_queue",
            description="Update a call queue",
            inputSchema={
                "type": "object",
                "properties": {
                    "queue_id": {"type": "string", "description": "Queue ID"},
                    "name": {"type": "string", "description": "Queue name"},
                    "phone_number": {"type": "string", "description": "Phone number"},
                    "call_policies": {"type": "object", "description": "Call policies"},
                },
                "required": ["queue_id"],
            },
        ),
        Tool(
            name="delete_call_queue",
            description="Delete a call queue",
            inputSchema={
                "type": "object",
                "properties": {
                    "queue_id": {"type": "string", "description": "Queue ID"},
                },
                "required": ["queue_id"],
            },
        ),
        Tool(
            name="add_agent_to_queue",
            description="Add an agent to a call queue",
            inputSchema={
                "type": "object",
                "properties": {
                    "queue_id": {"type": "string", "description": "Queue ID"},
                    "person_id": {"type": "string", "description": "User ID"},
                    "skill_level": {"type": "integer", "description": "Skill level"},
                },
                "required": ["queue_id", "person_id"],
            },
        ),
        Tool(
            name="remove_agent_from_queue",
            description="Remove an agent from a call queue",
            inputSchema={
                "type": "object",
                "properties": {
                    "queue_id": {"type": "string", "description": "Queue ID"},
                    "person_id": {"type": "string", "description": "User ID"},
                },
                "required": ["queue_id", "person_id"],
            },
        ),
        Tool(
            name="list_queue_agents",
            description="List all agents in a call queue",
            inputSchema={
                "type": "object",
                "properties": {
                    "queue_id": {"type": "string", "description": "Queue ID"},
                },
                "required": ["queue_id"],
            },
        ),
        # Auto Attendant CRUD
        Tool(
            name="create_auto_attendant",
            description="Create a new auto attendant",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Auto attendant name"},
                    "location_id": {"type": "string", "description": "Location ID"},
                    "phone_number": {"type": "string", "description": "Phone number"},
                    "business_schedule": {"type": "object", "description": "Business schedule"},
                    "menu": {"type": "object", "description": "Menu configuration"},
                },
                "required": ["name", "location_id"],
            },
        ),
        Tool(
            name="update_auto_attendant",
            description="Update an auto attendant",
            inputSchema={
                "type": "object",
                "properties": {
                    "auto_attendant_id": {"type": "string", "description": "Auto attendant ID"},
                    "name": {"type": "string", "description": "Auto attendant name"},
                    "phone_number": {"type": "string", "description": "Phone number"},
                    "business_schedule": {"type": "object", "description": "Business schedule"},
                    "menu": {"type": "object", "description": "Menu configuration"},
                },
                "required": ["auto_attendant_id"],
            },
        ),
        Tool(
            name="delete_auto_attendant",
            description="Delete an auto attendant",
            inputSchema={
                "type": "object",
                "properties": {
                    "auto_attendant_id": {"type": "string", "description": "Auto attendant ID"},
                },
                "required": ["auto_attendant_id"],
            },
        ),
        # Hunt Group CRUD
        Tool(
            name="create_hunt_group",
            description="Create a new hunt group",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Hunt group name"},
                    "location_id": {"type": "string", "description": "Location ID"},
                    "phone_number": {"type": "string", "description": "Phone number"},
                    "distribution": {"type": "string", "description": "Distribution method"},
                },
                "required": ["name", "location_id"],
            },
        ),
        Tool(
            name="update_hunt_group",
            description="Update a hunt group",
            inputSchema={
                "type": "object",
                "properties": {
                    "hunt_group_id": {"type": "string", "description": "Hunt group ID"},
                    "name": {"type": "string", "description": "Hunt group name"},
                    "phone_number": {"type": "string", "description": "Phone number"},
                    "distribution": {"type": "string", "description": "Distribution method"},
                },
                "required": ["hunt_group_id"],
            },
        ),
        Tool(
            name="delete_hunt_group",
            description="Delete a hunt group",
            inputSchema={
                "type": "object",
                "properties": {
                    "hunt_group_id": {"type": "string", "description": "Hunt group ID"},
                },
                "required": ["hunt_group_id"],
            },
        ),
        Tool(
            name="add_member_to_hunt_group",
            description="Add a member to a hunt group",
            inputSchema={
                "type": "object",
                "properties": {
                    "hunt_group_id": {"type": "string", "description": "Hunt group ID"},
                    "person_id": {"type": "string", "description": "User ID"},
                },
                "required": ["hunt_group_id", "person_id"],
            },
        ),
        Tool(
            name="remove_member_from_hunt_group",
            description="Remove a member from a hunt group",
            inputSchema={
                "type": "object",
                "properties": {
                    "hunt_group_id": {"type": "string", "description": "Hunt group ID"},
                    "person_id": {"type": "string", "description": "User ID"},
                },
                "required": ["hunt_group_id", "person_id"],
            },
        ),
        # Enhanced Phone Number Management
        Tool(
            name="unassign_phone_number",
            description="Unassign a phone number from a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "number_id": {"type": "string", "description": "Phone number ID"},
                },
                "required": ["number_id"],
            },
        ),
        Tool(
            name="assign_phone_number_to_location",
            description="Assign a phone number to a location",
            inputSchema={
                "type": "object",
                "properties": {
                    "number_id": {"type": "string", "description": "Phone number ID"},
                    "location_id": {"type": "string", "description": "Location ID"},
                },
                "required": ["number_id", "location_id"],
            },
        ),
        Tool(
            name="search_available_phone_numbers",
            description="Search for available phone numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_id": {"type": "string", "description": "Location ID"},
                    "area_code": {"type": "string", "description": "Area code"},
                    "state": {"type": "string", "description": "State"},
                    "country": {"type": "string", "description": "Country"},
                },
                "required": ["location_id"],
            },
        ),
        # Voicemail Management
        Tool(
            name="get_user_voicemail_settings",
            description="Get voicemail settings for a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "person_id": {"type": "string", "description": "User ID"},
                },
                "required": ["person_id"],
            },
        ),
        Tool(
            name="update_user_voicemail_settings",
            description="Update voicemail settings for a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "person_id": {"type": "string", "description": "User ID"},
                    "enabled": {"type": "boolean", "description": "Enable voicemail"},
                    "greeting": {"type": "object", "description": "Greeting configuration"},
                    "pin": {"type": "string", "description": "PIN"},
                },
                "required": ["person_id"],
            },
        ),
        Tool(
            name="list_voicemail_messages",
            description="List voicemail messages for a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "person_id": {"type": "string", "description": "User ID"},
                    "max_results": {"type": "integer", "description": "Max results", "default": 100},
                },
                "required": ["person_id"],
            },
        ),
        Tool(
            name="get_voicemail_message",
            description="Get a specific voicemail message",
            inputSchema={
                "type": "object",
                "properties": {
                    "message_id": {"type": "string", "description": "Message ID"},
                },
                "required": ["message_id"],
            },
        ),
        Tool(
            name="delete_voicemail_message",
            description="Delete a voicemail message",
            inputSchema={
                "type": "object",
                "properties": {
                    "message_id": {"type": "string", "description": "Message ID"},
                },
                "required": ["message_id"],
            },
        ),
        # Call Recording Management
        Tool(
            name="list_call_recordings",
            description="List call recordings",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_time": {"type": "string", "description": "Start time (ISO 8601)"},
                    "end_time": {"type": "string", "description": "End time (ISO 8601)"},
                    "person_id": {"type": "string", "description": "User ID"},
                    "max_results": {"type": "integer", "description": "Max results", "default": 100},
                },
                "required": [],
            },
        ),
        Tool(
            name="get_call_recording",
            description="Get details about a call recording",
            inputSchema={
                "type": "object",
                "properties": {
                    "recording_id": {"type": "string", "description": "Recording ID"},
                },
                "required": ["recording_id"],
            },
        ),
        # Enhanced Reporting
        Tool(
            name="export_call_records",
            description="Export call records in various formats",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_time": {"type": "string", "description": "Start time (ISO 8601)"},
                    "end_time": {"type": "string", "description": "End time (ISO 8601)"},
                    "format": {"type": "string", "description": "Export format (csv, json, etc.)", "default": "csv"},
                    "location_id": {"type": "string", "description": "Location ID"},
                },
                "required": ["start_time", "end_time"],
            },
        ),
        Tool(
            name="get_real_time_call_metrics",
            description="Get real-time call metrics",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_id": {"type": "string", "description": "Location ID"},
                },
                "required": [],
            },
        ),
        Tool(
            name="get_call_statistics",
            description="Get detailed call statistics with grouping",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_time": {"type": "string", "description": "Start time (ISO 8601)"},
                    "end_time": {"type": "string", "description": "End time (ISO 8601)"},
                    "location_id": {"type": "string", "description": "Location ID"},
                    "group_by": {"type": "string", "description": "Group by (user, location, etc.)"},
                },
                "required": ["start_time", "end_time"],
            },
        ),
        Tool(
            name="get_user_call_statistics",
            description="Get call statistics for a specific user",
            inputSchema={
                "type": "object",
                "properties": {
                    "person_id": {"type": "string", "description": "User ID"},
                    "start_time": {"type": "string", "description": "Start time (ISO 8601)"},
                    "end_time": {"type": "string", "description": "End time (ISO 8601)"},
                },
                "required": ["person_id", "start_time", "end_time"],
            },
        ),
        # Webhook Management
        Tool(
            name="list_webhooks",
            description="List all webhooks",
            inputSchema={
                "type": "object",
                "properties": {
                    "max_results": {"type": "integer", "description": "Max results", "default": 100},
                },
                "required": [],
            },
        ),
        Tool(
            name="create_webhook",
            description="Create a webhook",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Webhook name"},
                    "target_url": {"type": "string", "description": "Target URL"},
                    "resource": {"type": "string", "description": "Resource type"},
                    "event": {"type": "string", "description": "Event type"},
                    "secret": {"type": "string", "description": "Webhook secret"},
                },
                "required": ["name", "target_url", "resource", "event"],
            },
        ),
        Tool(
            name="get_webhook_details",
            description="Get webhook details",
            inputSchema={
                "type": "object",
                "properties": {
                    "webhook_id": {"type": "string", "description": "Webhook ID"},
                },
                "required": ["webhook_id"],
            },
        ),
        Tool(
            name="update_webhook",
            description="Update a webhook",
            inputSchema={
                "type": "object",
                "properties": {
                    "webhook_id": {"type": "string", "description": "Webhook ID"},
                    "name": {"type": "string", "description": "Webhook name"},
                    "target_url": {"type": "string", "description": "Target URL"},
                    "secret": {"type": "string", "description": "Webhook secret"},
                },
                "required": ["webhook_id"],
            },
        ),
        Tool(
            name="delete_webhook",
            description="Delete a webhook",
            inputSchema={
                "type": "object",
                "properties": {
                    "webhook_id": {"type": "string", "description": "Webhook ID"},
                },
                "required": ["webhook_id"],
            },
        ),
        # Advanced Features
        Tool(
            name="get_call_forwarding_settings",
            description="Get call forwarding settings for a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "person_id": {"type": "string", "description": "User ID"},
                },
                "required": ["person_id"],
            },
        ),
        Tool(
            name="update_call_forwarding_settings",
            description="Update call forwarding settings",
            inputSchema={
                "type": "object",
                "properties": {
                    "person_id": {"type": "string", "description": "User ID"},
                    "always": {"type": "boolean", "description": "Forward always"},
                    "busy": {"type": "boolean", "description": "Forward when busy"},
                    "no_answer": {"type": "boolean", "description": "Forward when no answer"},
                    "destination": {"type": "string", "description": "Forward destination"},
                },
                "required": ["person_id"],
            },
        ),
        Tool(
            name="get_call_park_settings",
            description="Get call park settings for a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "person_id": {"type": "string", "description": "User ID"},
                },
                "required": ["person_id"],
            },
        ),
        Tool(
            name="get_simultaneous_ring_settings",
            description="Get simultaneous ring settings for a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "person_id": {"type": "string", "description": "User ID"},
                },
                "required": ["person_id"],
            },
        ),
        Tool(
            name="update_simultaneous_ring_settings",
            description="Update simultaneous ring settings",
            inputSchema={
                "type": "object",
                "properties": {
                    "person_id": {"type": "string", "description": "User ID"},
                    "enabled": {"type": "boolean", "description": "Enable simultaneous ring"},
                    "phone_numbers": {"type": "array", "items": {"type": "string"}, "description": "Phone numbers"},
                },
                "required": ["person_id"],
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

        # Enhanced Device Management
        elif name == "associate_device_to_user":
            device_id = arguments["device_id"]
            person_id = arguments["person_id"]
            result = await client.associate_device_to_user(device_id, person_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "unassociate_device":
            device_id = arguments["device_id"]
            result = await client.unassociate_device(device_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "provision_device":
            device_id = arguments["device_id"]
            person_id = arguments["person_id"]
            location_id = arguments["location_id"]
            result = await client.provision_device(device_id, person_id, location_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "activate_device":
            device_id = arguments["device_id"]
            result = await client.activate_device(device_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "deactivate_device":
            device_id = arguments["device_id"]
            result = await client.deactivate_device(device_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "get_device_associations":
            device_id = arguments["device_id"]
            result = await client.get_device_associations(device_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "list_user_devices":
            person_id = arguments["person_id"]
            result = await client.list_user_devices(person_id)
            return [TextContent(type="text", text=format_json(result))]

        # Location CRUD
        elif name == "create_location":
            name = arguments["name"]
            address = arguments["address"]
            org_id = arguments.get("org_id")
            emergency_location = arguments.get("emergency_location")
            result = await client.create_location(
                name=name,
                address=address,
                org_id=org_id,
                emergency_location=emergency_location,
            )
            return [TextContent(type="text", text=format_json(result))]

        elif name == "update_location":
            location_id = arguments["location_id"]
            name = arguments.get("name")
            address = arguments.get("address")
            emergency_location = arguments.get("emergency_location")
            result = await client.update_location(
                location_id=location_id,
                name=name,
                address=address,
                emergency_location=emergency_location,
            )
            return [TextContent(type="text", text=format_json(result))]

        elif name == "delete_location":
            location_id = arguments["location_id"]
            result = await client.delete_location(location_id)
            return [TextContent(type="text", text=format_json(result))]

        # User CRUD
        elif name == "create_user":
            emails = arguments["emails"]
            display_name = arguments["display_name"]
            first_name = arguments.get("first_name")
            last_name = arguments.get("last_name")
            org_id = arguments.get("org_id")
            location_id = arguments.get("location_id")
            result = await client.create_user(
                emails=emails,
                display_name=display_name,
                first_name=first_name,
                last_name=last_name,
                org_id=org_id,
                location_id=location_id,
            )
            return [TextContent(type="text", text=format_json(result))]

        elif name == "update_user":
            person_id = arguments["person_id"]
            display_name = arguments.get("display_name")
            first_name = arguments.get("first_name")
            last_name = arguments.get("last_name")
            emails = arguments.get("emails")
            location_id = arguments.get("location_id")
            result = await client.update_user(
                person_id=person_id,
                display_name=display_name,
                first_name=first_name,
                last_name=last_name,
                emails=emails,
                location_id=location_id,
            )
            return [TextContent(type="text", text=format_json(result))]

        elif name == "delete_user":
            person_id = arguments["person_id"]
            result = await client.delete_user(person_id)
            return [TextContent(type="text", text=format_json(result))]

        # Call Queue Management
        elif name == "create_call_queue":
            name = arguments["name"]
            location_id = arguments["location_id"]
            phone_number = arguments.get("phone_number")
            call_policies = arguments.get("call_policies")
            result = await client.create_call_queue(
                name=name,
                location_id=location_id,
                phone_number=phone_number,
                call_policies=call_policies,
            )
            return [TextContent(type="text", text=format_json(result))]

        elif name == "update_call_queue":
            queue_id = arguments["queue_id"]
            name = arguments.get("name")
            phone_number = arguments.get("phone_number")
            call_policies = arguments.get("call_policies")
            result = await client.update_call_queue(
                queue_id=queue_id,
                name=name,
                phone_number=phone_number,
                call_policies=call_policies,
            )
            return [TextContent(type="text", text=format_json(result))]

        elif name == "delete_call_queue":
            queue_id = arguments["queue_id"]
            result = await client.delete_call_queue(queue_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "add_agent_to_queue":
            queue_id = arguments["queue_id"]
            person_id = arguments["person_id"]
            skill_level = arguments.get("skill_level")
            result = await client.add_agent_to_queue(queue_id, person_id, skill_level)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "remove_agent_from_queue":
            queue_id = arguments["queue_id"]
            person_id = arguments["person_id"]
            result = await client.remove_agent_from_queue(queue_id, person_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "list_queue_agents":
            queue_id = arguments["queue_id"]
            result = await client.list_queue_agents(queue_id)
            return [TextContent(type="text", text=format_json(result))]

        # Auto Attendant CRUD
        elif name == "create_auto_attendant":
            name = arguments["name"]
            location_id = arguments["location_id"]
            phone_number = arguments.get("phone_number")
            business_schedule = arguments.get("business_schedule")
            menu = arguments.get("menu")
            result = await client.create_auto_attendant(
                name=name,
                location_id=location_id,
                phone_number=phone_number,
                business_schedule=business_schedule,
                menu=menu,
            )
            return [TextContent(type="text", text=format_json(result))]

        elif name == "update_auto_attendant":
            auto_attendant_id = arguments["auto_attendant_id"]
            name = arguments.get("name")
            phone_number = arguments.get("phone_number")
            business_schedule = arguments.get("business_schedule")
            menu = arguments.get("menu")
            result = await client.update_auto_attendant(
                auto_attendant_id=auto_attendant_id,
                name=name,
                phone_number=phone_number,
                business_schedule=business_schedule,
                menu=menu,
            )
            return [TextContent(type="text", text=format_json(result))]

        elif name == "delete_auto_attendant":
            auto_attendant_id = arguments["auto_attendant_id"]
            result = await client.delete_auto_attendant(auto_attendant_id)
            return [TextContent(type="text", text=format_json(result))]

        # Hunt Group CRUD
        elif name == "create_hunt_group":
            name = arguments["name"]
            location_id = arguments["location_id"]
            phone_number = arguments.get("phone_number")
            distribution = arguments.get("distribution")
            result = await client.create_hunt_group(
                name=name,
                location_id=location_id,
                phone_number=phone_number,
                distribution=distribution,
            )
            return [TextContent(type="text", text=format_json(result))]

        elif name == "update_hunt_group":
            hunt_group_id = arguments["hunt_group_id"]
            name = arguments.get("name")
            phone_number = arguments.get("phone_number")
            distribution = arguments.get("distribution")
            result = await client.update_hunt_group(
                hunt_group_id=hunt_group_id,
                name=name,
                phone_number=phone_number,
                distribution=distribution,
            )
            return [TextContent(type="text", text=format_json(result))]

        elif name == "delete_hunt_group":
            hunt_group_id = arguments["hunt_group_id"]
            result = await client.delete_hunt_group(hunt_group_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "add_member_to_hunt_group":
            hunt_group_id = arguments["hunt_group_id"]
            person_id = arguments["person_id"]
            result = await client.add_member_to_hunt_group(hunt_group_id, person_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "remove_member_from_hunt_group":
            hunt_group_id = arguments["hunt_group_id"]
            person_id = arguments["person_id"]
            result = await client.remove_member_from_hunt_group(hunt_group_id, person_id)
            return [TextContent(type="text", text=format_json(result))]

        # Enhanced Phone Number Management
        elif name == "unassign_phone_number":
            number_id = arguments["number_id"]
            result = await client.unassign_phone_number(number_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "assign_phone_number_to_location":
            number_id = arguments["number_id"]
            location_id = arguments["location_id"]
            result = await client.assign_phone_number_to_location(number_id, location_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "search_available_phone_numbers":
            location_id = arguments["location_id"]
            area_code = arguments.get("area_code")
            state = arguments.get("state")
            country = arguments.get("country")
            result = await client.search_available_phone_numbers(
                location_id=location_id,
                area_code=area_code,
                state=state,
                country=country,
            )
            return [TextContent(type="text", text=format_json(result))]

        # Voicemail Management
        elif name == "get_user_voicemail_settings":
            person_id = arguments["person_id"]
            result = await client.get_user_voicemail_settings(person_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "update_user_voicemail_settings":
            person_id = arguments["person_id"]
            enabled = arguments.get("enabled")
            greeting = arguments.get("greeting")
            pin = arguments.get("pin")
            result = await client.update_user_voicemail_settings(
                person_id=person_id, enabled=enabled, greeting=greeting, pin=pin
            )
            return [TextContent(type="text", text=format_json(result))]

        elif name == "list_voicemail_messages":
            person_id = arguments["person_id"]
            max_results = arguments.get("max_results", 100)
            result = await client.list_voicemail_messages(person_id, max_results=max_results)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "get_voicemail_message":
            message_id = arguments["message_id"]
            result = await client.get_voicemail_message(message_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "delete_voicemail_message":
            message_id = arguments["message_id"]
            result = await client.delete_voicemail_message(message_id)
            return [TextContent(type="text", text=format_json(result))]

        # Call Recording Management
        elif name == "list_call_recordings":
            start_time = arguments.get("start_time")
            end_time = arguments.get("end_time")
            person_id = arguments.get("person_id")
            max_results = arguments.get("max_results", 100)
            result = await client.list_call_recordings(
                start_time=start_time,
                end_time=end_time,
                person_id=person_id,
                max_results=max_results,
            )
            return [TextContent(type="text", text=format_json(result))]

        elif name == "get_call_recording":
            recording_id = arguments["recording_id"]
            result = await client.get_call_recording(recording_id)
            return [TextContent(type="text", text=format_json(result))]

        # Enhanced Reporting
        elif name == "export_call_records":
            start_time = arguments["start_time"]
            end_time = arguments["end_time"]
            format_type = arguments.get("format", "csv")
            location_id = arguments.get("location_id")
            result = await client.export_call_records(
                start_time=start_time,
                end_time=end_time,
                format=format_type,
                location_id=location_id,
            )
            return [TextContent(type="text", text=format_json(result))]

        elif name == "get_real_time_call_metrics":
            location_id = arguments.get("location_id")
            result = await client.get_real_time_call_metrics(location_id=location_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "get_call_statistics":
            start_time = arguments["start_time"]
            end_time = arguments["end_time"]
            location_id = arguments.get("location_id")
            group_by = arguments.get("group_by")
            result = await client.get_call_statistics(
                start_time=start_time,
                end_time=end_time,
                location_id=location_id,
                group_by=group_by,
            )
            return [TextContent(type="text", text=format_json(result))]

        elif name == "get_user_call_statistics":
            person_id = arguments["person_id"]
            start_time = arguments["start_time"]
            end_time = arguments["end_time"]
            result = await client.get_user_call_statistics(
                person_id=person_id, start_time=start_time, end_time=end_time
            )
            return [TextContent(type="text", text=format_json(result))]

        # Webhook Management
        elif name == "list_webhooks":
            max_results = arguments.get("max_results", 100)
            result = await client.list_webhooks(max_results=max_results)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "create_webhook":
            name = arguments["name"]
            target_url = arguments["target_url"]
            resource = arguments["resource"]
            event = arguments["event"]
            secret = arguments.get("secret")
            result = await client.create_webhook(
                name=name, target_url=target_url, resource=resource, event=event, secret=secret
            )
            return [TextContent(type="text", text=format_json(result))]

        elif name == "get_webhook_details":
            webhook_id = arguments["webhook_id"]
            result = await client.get_webhook_details(webhook_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "update_webhook":
            webhook_id = arguments["webhook_id"]
            name = arguments.get("name")
            target_url = arguments.get("target_url")
            secret = arguments.get("secret")
            result = await client.update_webhook(
                webhook_id=webhook_id, name=name, target_url=target_url, secret=secret
            )
            return [TextContent(type="text", text=format_json(result))]

        elif name == "delete_webhook":
            webhook_id = arguments["webhook_id"]
            result = await client.delete_webhook(webhook_id)
            return [TextContent(type="text", text=format_json(result))]

        # Advanced Features
        elif name == "get_call_forwarding_settings":
            person_id = arguments["person_id"]
            result = await client.get_call_forwarding_settings(person_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "update_call_forwarding_settings":
            person_id = arguments["person_id"]
            always = arguments.get("always")
            busy = arguments.get("busy")
            no_answer = arguments.get("no_answer")
            destination = arguments.get("destination")
            result = await client.update_call_forwarding_settings(
                person_id=person_id,
                always=always,
                busy=busy,
                no_answer=no_answer,
                destination=destination,
            )
            return [TextContent(type="text", text=format_json(result))]

        elif name == "get_call_park_settings":
            person_id = arguments["person_id"]
            result = await client.get_call_park_settings(person_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "get_simultaneous_ring_settings":
            person_id = arguments["person_id"]
            result = await client.get_simultaneous_ring_settings(person_id)
            return [TextContent(type="text", text=format_json(result))]

        elif name == "update_simultaneous_ring_settings":
            person_id = arguments["person_id"]
            enabled = arguments.get("enabled")
            phone_numbers = arguments.get("phone_numbers")
            result = await client.update_simultaneous_ring_settings(
                person_id=person_id, enabled=enabled, phone_numbers=phone_numbers
            )
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

