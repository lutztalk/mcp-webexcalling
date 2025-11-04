# MCP Webex Calling Server

An MCP (Model Context Protocol) server for interacting with Webex Calling APIs. This server enables you to query Webex Calling data and perform functions within your Webex organization.

## Features

### Data Retrieval
- Query Webex Calling users, locations, and organizations
- Retrieve call queue information, auto attendants, hunt groups, and trunk groups
- Get device and phone number information
- Query call history and detailed call records
- List licenses and user assignments

### User & Location Management
- Create, update, and delete users
- Create, update, and delete locations
- Update user extensions and calling settings
- Assign phone numbers to users
- Manage user calling features (call park, forwarding, voicemail, recording, etc.)
- Search and filter users by various criteria

### Device Management
- List and get device details
- Associate/unassociate devices to users
- Provision devices with full configuration
- Activate/deactivate devices
- Get device associations and status
- List all devices for a user

### License Management
- List all licenses in the organization
- View license details and user assignments
- Assign and remove licenses from users

### Call Queue Management
- Create, update, and delete call queues
- Add/remove agents from queues
- List queue agents with skill levels
- Get queue analytics and performance metrics

### Auto Attendant & Hunt Group Management
- Create, update, and delete auto attendants
- Configure business schedules and menus
- Create, update, and delete hunt groups
- Add/remove members from hunt groups

### Phone Number Management
- List phone numbers and search available numbers
- Assign/unassign phone numbers to users
- Assign phone numbers to locations

### Voicemail & Call Recording
- Get and update voicemail settings
- List, get, and delete voicemail messages
- List call recordings and get recording details

### Reporting & Analytics
- Get call detail records (CDRs) for reporting
- Export call records in CSV/JSON formats
- Real-time call metrics
- Generate call analytics and statistics with grouping
- User-specific call statistics
- Queue-specific analytics and performance metrics
- Time-based reporting with flexible date ranges

### Webhook & Event Management
- List, create, update, and delete webhooks
- Complete webhook lifecycle management

### Advanced Calling Features
- Call forwarding settings (get/update)
- Call park settings
- Simultaneous ring settings (get/update)

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

The server provides **85 MCP tools** organized by category:

### Organization & Location Tools
- `get_organization_info` - Get information about your Webex organization
- `list_locations` - List all locations in your organization
- `get_location_details` - Get detailed information about a specific location
- `get_location_features` - Get available features for a location
- `create_location` - Create a new location
- `update_location` - Update a location
- `delete_location` - Delete a location

### User Management Tools
- `list_users` - List users in your organization
- `get_user_details` - Get detailed information about a specific user
- `get_user_by_email` - Get user information by email address
- `get_user_calling_settings` - Get calling settings for a user
- `search_users` - Search for users by email or display name
- `create_user` - Create a new user
- `update_user` - Update a user
- `delete_user` - Delete a user

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
- `associate_device_to_user` - Associate a device to a user
- `unassociate_device` - Unassociate a device from a user
- `provision_device` - Provision a device for a user
- `activate_device` - Activate a device
- `deactivate_device` - Deactivate a device
- `get_device_associations` - Get device associations and status
- `list_user_devices` - List all devices associated with a user

### Phone Number Tools
- `list_phone_numbers` - List phone numbers in your organization
- `get_phone_number_details` - Get details about a specific phone number
- `unassign_phone_number` - Unassign a phone number from a user
- `assign_phone_number_to_location` - Assign a phone number to a location
- `search_available_phone_numbers` - Search for available phone numbers

### Call Queue Management Tools
- `list_call_queues` - List all call queues
- `get_call_queue_details` - Get details about a specific call queue
- `create_call_queue` - Create a new call queue
- `update_call_queue` - Update a call queue
- `delete_call_queue` - Delete a call queue
- `add_agent_to_queue` - Add an agent to a call queue
- `remove_agent_from_queue` - Remove an agent from a call queue
- `list_queue_agents` - List all agents in a call queue

### Auto Attendant Tools
- `list_auto_attendants` - List all auto attendants
- `get_auto_attendant_details` - Get details about a specific auto attendant
- `create_auto_attendant` - Create a new auto attendant
- `update_auto_attendant` - Update an auto attendant
- `delete_auto_attendant` - Delete an auto attendant

### Hunt Group Tools
- `list_hunt_groups` - List hunt groups in your organization
- `get_hunt_group_details` - Get details about a specific hunt group
- `create_hunt_group` - Create a new hunt group
- `update_hunt_group` - Update a hunt group
- `delete_hunt_group` - Delete a hunt group
- `add_member_to_hunt_group` - Add a member to a hunt group
- `remove_member_from_hunt_group` - Remove a member from a hunt group

### Additional Group Tools
- `list_trunk_groups` - List trunk groups in your organization
- `get_trunk_group_details` - Get details about a specific trunk group
- `list_call_park_extensions` - List call park extensions

### Voicemail Management Tools
- `get_user_voicemail_settings` - Get voicemail settings for a user
- `update_user_voicemail_settings` - Update voicemail settings for a user
- `list_voicemail_messages` - List voicemail messages for a user
- `get_voicemail_message` - Get a specific voicemail message
- `delete_voicemail_message` - Delete a voicemail message

### Call Recording Tools
- `list_call_recordings` - List call recordings
- `get_call_recording` - Get details about a call recording

### Reporting & Analytics Tools
- `get_call_history` - Get call history for a user or location
- `get_call_detail_records` - Get call detail records (CDRs) for reporting
- `get_call_analytics` - Get call analytics and statistics for a time period
- `get_queue_analytics` - Get analytics for a specific call queue
- `export_call_records` - Export call records in various formats
- `get_real_time_call_metrics` - Get real-time call metrics
- `get_call_statistics` - Get detailed call statistics with grouping
- `get_user_call_statistics` - Get call statistics for a specific user

### Webhook Management Tools
- `list_webhooks` - List all webhooks
- `create_webhook` - Create a webhook
- `get_webhook_details` - Get webhook details
- `update_webhook` - Update a webhook
- `delete_webhook` - Delete a webhook

### Advanced Calling Features
- `get_call_forwarding_settings` - Get call forwarding settings for a user
- `update_call_forwarding_settings` - Update call forwarding settings
- `get_call_park_settings` - Get call park settings for a user
- `get_simultaneous_ring_settings` - Get simultaneous ring settings for a user
- `update_simultaneous_ring_settings` - Update simultaneous ring settings

## Example Usage

Once connected to an MCP client, you can ask questions like:

### Data Queries
- "What locations are in my Webex organization?"
- "Show me the details for user john.doe@example.com"
- "What call queues do we have configured?"
- "List all devices in the organization"
- "Show me all phone numbers at location X"

### User & Location Management
- "Create a new user with email john.doe@example.com"
- "Update user john.doe@example.com extension to 1234"
- "Assign phone number ID xyz to user jane.smith@example.com"
- "Create a new location called Main Office"
- "Delete location ID xyz"

### Device Management
- "Associate device ID xyz to user john.doe@example.com"
- "Provision device ID xyz for user jane.smith@example.com at location abc"
- "List all devices for user bob@example.com"
- "Get device associations for device ID xyz"

### License Management
- "List all licenses in the organization"
- "What licenses does user john.doe@example.com have?"
- "Assign license ID xyz to user jane.smith@example.com"
- "Remove license ID xyz from user bob@example.com"

### Queue & Group Management
- "Create a new call queue called Support"
- "Add agent jane.smith@example.com to queue ID xyz"
- "Create a new auto attendant for after-hours"
- "Add member bob@example.com to hunt group ID xyz"

### Reporting & Analytics
- "Show me call history for the last week"
- "Get call analytics for January 2024"
- "Export call records for the last month as CSV"
- "Get real-time call metrics for location ID xyz"
- "Show me queue analytics for queue ID xyz for the last month"
- "Get call statistics grouped by user for January 2024"

### Voicemail & Recordings
- "List voicemail messages for user john.doe@example.com"
- "Get voicemail settings for user jane.smith@example.com"
- "List call recordings from the last week"

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

