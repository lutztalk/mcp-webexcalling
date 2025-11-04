# MCP Webex Calling Server

An MCP (Model Context Protocol) server for interacting with Webex Calling APIs. This server enables you to query Webex Calling data and perform functions within your Webex organization.

## Features

### Data Retrieval
- Query Webex Calling users, locations, and organizations
- Retrieve call queue information, auto attendants, hunt groups, and trunk groups
- Get device and phone number information
- Query call history and detailed call records
- List licenses and user assignments

### User Management
- Update user extensions and calling settings
- Assign phone numbers to users
- Manage user calling features (call park, forwarding, voicemail, recording, etc.)
- Search and filter users by various criteria

### License Management
- List all licenses in the organization
- View license details and user assignments
- Assign and remove licenses from users

### Reporting & Analytics
- Get call detail records (CDRs) for reporting
- Generate call analytics and statistics
- Queue-specific analytics and performance metrics
- Time-based reporting with flexible date ranges

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

The server provides **35+ MCP tools** organized by category:

### Organization & Location Tools
- `get_organization_info` - Get information about your Webex organization
- `list_locations` - List all locations in your organization
- `get_location_details` - Get detailed information about a specific location
- `get_location_features` - Get available features for a location

### User Management Tools
- `list_users` - List users in your organization
- `get_user_details` - Get detailed information about a specific user
- `get_user_by_email` - Get user information by email address
- `get_user_calling_settings` - Get calling settings for a user
- `search_users` - Search for users by email or display name

### User Extension & Feature Management
- `update_user_extension` - Update user extension and calling settings
- `assign_phone_number_to_user` - Assign a phone number to a user
- `update_user_calling_features` - Update calling features (park, forwarding, voicemail, etc.)

### License Management Tools
- `list_licenses` - List all licenses in your organization
- `get_license_details` - Get details about a specific license
- `list_user_licenses` - List licenses assigned to a user
- `assign_license_to_user` - Assign a license to a user
- `remove_license_from_user` - Remove a license from a user

### Device Management Tools
- `list_devices` - List devices in your organization
- `get_device_details` - Get details about a specific device

### Phone Number Tools
- `list_phone_numbers` - List phone numbers in your organization
- `get_phone_number_details` - Get details about a specific phone number

### Call Queue & Auto Attendant Tools
- `list_call_queues` - List all call queues
- `get_call_queue_details` - Get details about a specific call queue
- `list_auto_attendants` - List all auto attendants
- `get_auto_attendant_details` - Get details about a specific auto attendant

### Additional Group Tools
- `list_hunt_groups` - List hunt groups in your organization
- `get_hunt_group_details` - Get details about a specific hunt group
- `list_trunk_groups` - List trunk groups in your organization
- `get_trunk_group_details` - Get details about a specific trunk group
- `list_call_park_extensions` - List call park extensions

### Reporting & Analytics Tools
- `get_call_history` - Get call history for a user or location
- `get_call_detail_records` - Get call detail records (CDRs) for reporting
- `get_call_analytics` - Get call analytics and statistics for a time period
- `get_queue_analytics` - Get analytics for a specific call queue

## Example Usage

Once connected to an MCP client, you can ask questions like:

### Data Queries
- "What locations are in my Webex organization?"
- "Show me the details for user john.doe@example.com"
- "What call queues do we have configured?"
- "List all devices in the organization"
- "Show me all phone numbers at location X"

### User Management
- "Update user john.doe@example.com extension to 1234"
- "Assign phone number ID xyz to user jane.smith@example.com"
- "Enable call forwarding for user bob@example.com"
- "Update calling features for user alice@example.com"

### License Management
- "List all licenses in the organization"
- "What licenses does user john.doe@example.com have?"
- "Assign license ID xyz to user jane.smith@example.com"
- "Remove license ID xyz from user bob@example.com"

### Reporting & Analytics
- "Show me call history for the last week"
- "Get call analytics for January 2024"
- "Show me queue analytics for queue ID xyz for the last month"
- "Get call detail records for user john.doe@example.com"

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

