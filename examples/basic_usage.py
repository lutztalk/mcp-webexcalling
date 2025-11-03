"""Example usage of the MCP Webex Calling Server

This script demonstrates how to interact with the Webex Calling APIs
directly using the WebexClient.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path to import mcp_webexcalling
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_webexcalling.webex_client import WebexClient
from mcp_webexcalling.config import get_settings


async def main():
    """Example usage of WebexClient"""
    try:
        # Initialize client
        client = WebexClient()

        print("=== Webex Calling API Examples ===\n")

        # Example 1: Get organization info
        print("1. Getting organization information...")
        org_info = await client.get_organization_info()
        print(f"   Organizations found: {len(org_info.get('items', []))}\n")

        # Example 2: Get authenticated user info
        print("2. Getting authenticated user information...")
        my_info = await client.get_my_info()
        print(f"   User: {my_info.get('displayName')} ({my_info.get('emails', [None])[0]})\n")

        # Example 3: List locations
        print("3. Listing locations...")
        locations = await client.list_locations(max_results=10)
        print(f"   Found {len(locations)} locations")
        for loc in locations[:3]:  # Show first 3
            print(f"   - {loc.get('name')} (ID: {loc.get('id')})")
        print()

        # Example 4: List users
        print("4. Listing users...")
        users = await client.list_users(max_results=10)
        print(f"   Found {len(users)} users")
        for user in users[:3]:  # Show first 3
            print(f"   - {user.get('displayName')} ({user.get('emails', [None])[0]})")
        print()

        # Example 5: Search for a user (if you have a test email)
        # Uncomment and modify the email below to test
        # print("5. Searching for user by email...")
        # user = await client.get_user_by_email("user@example.com")
        # if user:
        #     print(f"   Found: {user.get('displayName')}")
        # else:
        #     print("   User not found")
        # print()

        # Example 6: List call queues
        print("6. Listing call queues...")
        queues = await client.list_call_queues(max_results=10)
        print(f"   Found {len(queues)} call queues")
        for queue in queues[:3]:  # Show first 3
            print(f"   - {queue.get('name')} (ID: {queue.get('id')})")
        print()

        # Example 7: List auto attendants
        print("7. Listing auto attendants...")
        auto_attendants = await client.list_auto_attendants(max_results=10)
        print(f"   Found {len(auto_attendants)} auto attendants")
        for aa in auto_attendants[:3]:  # Show first 3
            print(f"   - {aa.get('name')} (ID: {aa.get('id')})")
        print()

        print("=== Examples completed successfully! ===")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

