# MCP Webex Calling Server

An MCP (Model Context Protocol) server that provides comprehensive access to Webex Calling APIs through natural language interactions. This server bridges the gap between AI assistants like Claude and your Webex Calling infrastructure, enabling you to manage your entire calling environment through conversational queries.

## What is MCP?

MCP (Model Context Protocol) is a standardized protocol that allows AI assistants to securely connect to external services and data sources. Instead of manually navigating APIs or writing scripts, MCP servers expose capabilities as tools that AI assistants can understand and use on your behalf.

## Why Use MCP for Webex Calling?

Webex Calling is a powerful cloud-based calling platform with extensive APIs for managing users, devices, locations, call queues, and more. However, interacting with these APIs typically requires:

- Writing custom scripts or applications
- Understanding complex API documentation
- Managing authentication and tokens
- Handling pagination, error handling, and data formatting

This MCP server eliminates these barriers by:

- **Natural Language Interface**: Ask questions in plain English instead of crafting API calls
- **Comprehensive Coverage**: Access to 85+ tools covering all major Webex Calling operations
- **Intelligent Automation**: Let AI assistants handle complex multi-step operations automatically
- **Real-time Insights**: Get instant answers about your calling infrastructure, call analytics, and user configurations
- **Unified Management**: Manage users, devices, locations, queues, hunt groups, and more from a single interface
- **Safe Operations**: Built-in error handling and validation for all API interactions

## Use Cases

- **Quick Queries**: "What call queues do we have configured?" or "Show me all devices for user john@example.com"
- **Administrative Tasks**: "Assign phone number X to user Y" or "Create a new call queue called Support"
- **Analytics & Reporting**: "Get call analytics for last month" or "Show me queue performance metrics"
- **Troubleshooting**: "What are the calling settings for user X?" or "List all devices at location Y"
- **Bulk Operations**: "Update extensions for all users in location X" or "List all licenses in the organization"
- **Voicemail & Recording Management**: "List voicemail messages for user X" or "Get call recordings from the last week"
- **Device Provisioning**: "Provision device ABC123 for user john@example.com at location Main Office" or "Associate device XYZ789 to user jane@example.com"

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

## Connecting to Claude Desktop

Follow these step-by-step instructions to connect the MCP Webex Calling server to Claude Desktop.

### Prerequisites

- Python 3.9+ installed
- Claude Desktop installed
- Webex access token (see [Setup](#setup) above)

### Step 1: Install the Server

1. **Clone or download the repository:**
   ```bash
   git clone https://github.com/lutztalk/mcp-webexcalling.git
   cd mcp-webexcalling
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the package (optional but recommended):**
   ```bash
   pip install -e .
   ```

### Step 2: Get Your Webex Access Token

1. Go to [Webex Developer Portal](https://developer.webex.com/)
2. Sign in with your Webex account
3. Click your profile icon → **Personal Access Tokens**
4. Click **"Create a Token"**
5. Name it (e.g., "MCP Server")
6. Copy the token (you won't be able to see it again)

**Required Scopes:**
- `spark:people_read` - Read people information
- `spark-admin:locations_read` - Read location information
- `spark-admin:organizations_read` - Read organization information
- `spark-admin:telephony_config_read` - Read calling configuration
- `spark-admin:read_call_history` - Read call history (optional)

### Step 3: Find Your Python Path

You need the full path to your Python executable. Run this command:

**macOS/Linux:**
```bash
which python3
# or if using venv:
which python
```

**Windows (PowerShell):**
```powershell
where.exe python
```

**Windows (CMD):**
```cmd
where python
```

Note the full path (e.g., `/Users/yourname/mcp-webexcalling/venv/bin/python3` or `C:\Users\yourname\mcp-webexcalling\venv\Scripts\python.exe`)

### Step 4: Configure Claude Desktop

1. **Locate the Claude Desktop configuration file:**

   **macOS:**
   ```
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```

   **Windows:**
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```
   (Typically: `C:\Users\YourName\AppData\Roaming\Claude\claude_desktop_config.json`)

   **Linux:**
   ```
   ~/.config/Claude/claude_desktop_config.json
   ```

2. **Open the configuration file in a text editor**

   If the file doesn't exist, create it. If it exists, you'll see a JSON structure like:
   ```json
   {
     "mcpServers": {
       // existing servers...
     }
   }
   ```

3. **Add the Webex Calling server configuration:**

   Replace the following placeholders:
   - `YOUR_PYTHON_PATH` - The full path to your Python executable from Step 3
   - `YOUR_PROJECT_PATH` - The full path to the `mcp-webexcalling` directory
   - `YOUR_WEBEX_TOKEN` - Your Webex access token from Step 2

   **macOS/Linux Example:**
   ```json
   {
     "mcpServers": {
       "webex-calling": {
         "command": "/Users/yourname/mcp-webexcalling/venv/bin/python3",
         "args": ["-m", "mcp_webexcalling.server"],
         "cwd": "/Users/yourname/mcp-webexcalling",
         "env": {
           "WEBEX_ACCESS_TOKEN": "YOUR_WEBEX_TOKEN_HERE",
           "WEBEX_BASE_URL": "https://webexapis.com/v1"
         }
       }
     }
   }
   ```

   **Windows Example:**
   ```json
   {
     "mcpServers": {
       "webex-calling": {
         "command": "C:\\Users\\YourName\\mcp-webexcalling\\venv\\Scripts\\python.exe",
         "args": ["-m", "mcp_webexcalling.server"],
         "cwd": "C:\\Users\\YourName\\mcp-webexcalling",
         "env": {
           "WEBEX_ACCESS_TOKEN": "YOUR_WEBEX_TOKEN_HERE",
           "WEBEX_BASE_URL": "https://webexapis.com/v1"
         }
       }
     }
   }
   ```

   **Important Notes:**
   - Use forward slashes `/` on macOS/Linux, backslashes `\\` on Windows
   - On Windows, escape backslashes in JSON strings as `\\`
   - Make sure the `cwd` path matches your actual project directory
   - The `command` should point to the Python executable in your virtual environment

4. **Save the configuration file**

### Step 5: Restart Claude Desktop

1. **Quit Claude Desktop completely:**
   - macOS: Right-click the Claude icon in the dock → Quit
   - Windows: Close the application or use Task Manager
   - Linux: Close the application

2. **Reopen Claude Desktop**

3. **Verify the connection:**
   - Open a new chat in Claude Desktop
   - You should see "webex-calling" in the MCP servers list (if visible)
   - Try asking: "What locations are in my Webex organization?"
   - If it works, you're connected!

### Troubleshooting

#### "Server disconnected" Error

1. **Check Python path:**
   - Verify the `command` path is correct and points to an executable Python
   - Try using the full path to `python3.12` or `python3.11` instead of just `python3`

2. **Check project path:**
   - Verify the `cwd` path is correct and points to the project root
   - Make sure the directory contains `mcp_webexcalling/` folder

3. **Check dependencies:**
   - Make sure you've installed requirements: `pip install -r requirements.txt`
   - Try installing in editable mode: `pip install -e .`

4. **Check token:**
   - Verify your `WEBEX_ACCESS_TOKEN` is correct
   - Test the token manually:
     ```bash
     curl -H "Authorization: Bearer YOUR_TOKEN" https://webexapis.com/v1/people/me
     ```

5. **Check logs:**
   - Look for error messages in Claude Desktop's console/logs
   - On macOS, check Console.app for Claude Desktop errors

#### "Module not found" Error

1. Make sure you're using the Python from your virtual environment
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Install in editable mode: `pip install -e .`

#### Path Issues on Windows

- Use double backslashes `\\` in JSON strings
- Or use forward slashes `/` (Windows accepts both)
- Make sure paths don't have trailing slashes

#### Still Having Issues?

1. **Test the server manually:**
   ```bash
   cd /path/to/mcp-webexcalling
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   python -m mcp_webexcalling.server
   ```
   If this works, the server is fine and the issue is with Claude Desktop configuration.

2. **Check the configuration file syntax:**
   - Use a JSON validator to ensure your config file is valid JSON
   - Make sure all quotes are properly escaped

3. **Try absolute paths:**
   - Use full absolute paths for both `command` and `cwd`
   - Avoid relative paths or `~` shortcuts

For more detailed troubleshooting, see [SETUP.md](SETUP.md).

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

