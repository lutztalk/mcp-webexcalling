# MCP Webex Calling Server

An MCP (Model Context Protocol) server for interacting with Webex Calling APIs. This server enables you to query Webex Calling data and perform functions within your Webex organization.

## Features

- Query Webex Calling users, locations, and organizations
- Retrieve call queue information
- Get auto attendant details
- Query call history and analytics
- Manage Webex Calling settings

## Setup

See [SETUP.md](SETUP.md) for detailed installation and configuration instructions.

### Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   Create a `.env` file with your Webex access token:
   ```env
   WEBEX_ACCESS_TOKEN=your_token_here
   ```

3. **Get Webex access token:**
   - Go to [Webex Developer Portal](https://developer.webex.com/)
   - Create a Personal Access Token with required scopes

4. **Run the server:**
   ```bash
   python -m mcp_webexcalling.server
   ```

## Configuration

The server uses environment variables for configuration:

- `WEBEX_ACCESS_TOKEN`: Your Webex API access token (required)
- `WEBEX_BASE_URL`: Webex API base URL (default: https://webexapis.com/v1)

## Available Tools

The server provides the following MCP tools:

- `get_organization_info` - Get information about your Webex organization
- `list_locations` - List all locations in your organization
- `get_location_details` - Get detailed information about a specific location
- `list_users` - List users in your organization
- `get_user_details` - Get detailed information about a specific user
- `get_user_calling_settings` - Get calling settings for a user
- `list_call_queues` - List all call queues
- `get_call_queue_details` - Get details about a specific call queue
- `list_auto_attendants` - List all auto attendants
- `get_auto_attendant_details` - Get details about a specific auto attendant
- `get_call_history` - Get call history for a user or location
- `search_users` - Search for users by email or display name

## Example Usage

Once connected to an MCP client, you can ask questions like:

- "What locations are in my Webex organization?"
- "Show me the details for user john.doe@example.com"
- "What call queues do we have configured?"
- "Get the calling settings for user jane.smith@example.com"
- "Show me call history for the last week"

For detailed usage examples and tool documentation, see [USAGE.md](USAGE.md).

## Testing

Test the Webex client directly:

```bash
python examples/basic_usage.py
```

## API Documentation

For detailed information about Webex Calling APIs, see:
- [Webex Calling API Documentation](https://developer.cisco.com/docs/webex-calling/)
- [Webex Admin API Documentation](https://developer.webex.com/docs/api/v1)

## License

MIT

