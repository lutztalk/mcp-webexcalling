# Usage Guide

## Quick Start

### 1. Set Up Environment

Create a `.env` file in the project root:

```bash
WEBEX_ACCESS_TOKEN=your_token_here
WEBEX_BASE_URL=https://webexapis.com/v1
```

### 2. Get Webex Access Token

1. Go to [Webex Developer Portal](https://developer.webex.com/)
2. Sign in with your Webex account
3. Navigate to [My Webex Apps](https://developer.webex.com/my-apps)
4. Create a new integration or use an existing one
5. Generate a Personal Access Token or set up OAuth

**Required Scopes:**
- `spark:people_read` - Read people information
- `spark-admin:locations_read` - Read location information
- `spark-admin:organizations_read` - Read organization information
- `spark-admin:telephony_config_read` - Read calling configuration
- `spark-admin:read_call_history` - Read call history (optional)

### 3. Run the MCP Server

#### Option A: Direct Python Execution

```bash
python -m mcp_webexcalling.server
```

#### Option B: With MCP Client (Claude Desktop, etc.)

Add to your MCP configuration file (e.g., `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "webex-calling": {
      "command": "python",
      "args": ["-m", "mcp_webexcalling.server"],
      "env": {
        "WEBEX_ACCESS_TOKEN": "your_token_here"
      }
    }
  }
}
```

## Available Tools

### Organization & Location Tools

#### `get_organization_info`
Get information about your Webex organization.

**Example:**
- "What organizations am I part of?"
- "Show me my organization details"

#### `list_locations`
List all locations in your organization.

**Parameters:**
- `org_id` (optional): Filter by organization ID
- `max_results` (optional): Maximum results (default: 100)

**Example:**
- "What locations are in my Webex organization?"
- "List all locations"

#### `get_location_details`
Get detailed information about a specific location.

**Parameters:**
- `location_id` (required): The location ID

**Example:**
- "Show me details for location ID xyz123"
- "What are the settings for location abc456?"

### User Tools

#### `list_users`
List users in your organization.

**Parameters:**
- `org_id` (optional): Filter by organization ID
- `location_id` (optional): Filter by location ID
- `max_results` (optional): Maximum results (default: 100)

**Example:**
- "List all users in my organization"
- "Show me users at location xyz123"

#### `get_user_details`
Get detailed information about a specific user by ID.

**Parameters:**
- `person_id` (required): The user ID

**Example:**
- "Show me details for user ID xyz123"

#### `get_user_by_email`
Get user information by email address.

**Parameters:**
- `email` (required): The user's email address

**Example:**
- "Get information for john.doe@example.com"
- "Show me user details for user@company.com"

#### `get_user_calling_settings`
Get calling settings for a specific user.

**Parameters:**
- `person_id` (required): The user ID

**Example:**
- "What are the calling settings for user xyz123?"
- "Show me calling configuration for john.doe@example.com"

#### `search_users`
Search for users by display name or email.

**Parameters:**
- `query` (required): Search query
- `org_id` (optional): Filter by organization ID
- `max_results` (optional): Maximum results (default: 100)

**Example:**
- "Search for users named John"
- "Find users with email domain example.com"

### Call Queue Tools

#### `list_call_queues`
List all call queues in your organization.

**Parameters:**
- `location_id` (optional): Filter by location ID
- `max_results` (optional): Maximum results (default: 100)

**Example:**
- "What call queues do we have?"
- "List all call queues at location xyz123"

#### `get_call_queue_details`
Get detailed information about a specific call queue.

**Parameters:**
- `queue_id` (required): The call queue ID

**Example:**
- "Show me details for call queue xyz123"

### Auto Attendant Tools

#### `list_auto_attendants`
List all auto attendants in your organization.

**Parameters:**
- `location_id` (optional): Filter by location ID
- `max_results` (optional): Maximum results (default: 100)

**Example:**
- "What auto attendants are configured?"
- "List auto attendants for location xyz123"

#### `get_auto_attendant_details`
Get detailed information about a specific auto attendant.

**Parameters:**
- `auto_attendant_id` (required): The auto attendant ID

**Example:**
- "Show me details for auto attendant xyz123"

### Call History Tools

#### `get_call_history`
Get call history for a user or location.

**Parameters:**
- `person_id` (optional): Filter by user ID
- `location_id` (optional): Filter by location ID
- `start_time` (optional): Start time in ISO 8601 format
- `end_time` (optional): End time in ISO 8601 format
- `max_results` (optional): Maximum results (default: 100)

**Example:**
- "Show me call history for the last week"
- "Get call history for user xyz123"
- "Show calls from location abc456 between January 1 and January 31"

## Example Queries

Here are some example queries you can ask once the MCP server is connected:

1. **Organization Overview:**
   - "What's my Webex organization information?"
   - "How many locations do we have?"

2. **User Management:**
   - "Find the user with email john.doe@example.com"
   - "Show me all users at location Main Office"
   - "What are the calling settings for jane.smith@example.com?"

3. **Call Queue Management:**
   - "List all our call queues"
   - "Show me details for the Support queue"

4. **Auto Attendants:**
   - "What auto attendants are configured?"
   - "Show me the main auto attendant settings"

5. **Call Analytics:**
   - "Get call history for the last 7 days"
   - "Show me calls for user john.doe@example.com this month"

## Testing

You can test the Webex client directly using the example script:

```bash
python examples/basic_usage.py
```

Make sure your `.env` file is configured with a valid access token before running.

## Troubleshooting

### Authentication Errors

If you get authentication errors:
1. Verify your `WEBEX_ACCESS_TOKEN` is correct
2. Check that your token has the required scopes
3. Ensure your token hasn't expired

### API Errors

If you encounter API errors:
1. Check the Webex API status
2. Verify you have the necessary permissions in your Webex organization
3. Some endpoints may require admin privileges

### Connection Issues

If the MCP server won't connect:
1. Verify Python path is correct in your MCP configuration
2. Check that all dependencies are installed: `pip install -r requirements.txt`
3. Look for error messages in the MCP client logs

