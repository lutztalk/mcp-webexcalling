# MCP Webex Calling Server

An MCP (Model Context Protocol) server for interacting with Webex Calling APIs. This server enables you to query Webex Calling data and perform administrative functions within your Webex organization through natural language conversations with AI assistants like Claude Desktop.

## What is MCP?

MCP (Model Context Protocol) is a standardized protocol that allows AI assistants to securely connect to external services and data sources. Instead of manually navigating APIs or writing scripts, MCP servers expose capabilities as tools that AI assistants can understand and use on your behalf.

## Why Use MCP for Webex Calling?

Managing Webex Calling through traditional methods can be time-consuming:
- **Manual API calls**: Requires understanding complex API documentation and writing code
- **Web interfaces**: Point-and-click can be slow for bulk operations or repetitive tasks
- **Scripts**: Need to be written, maintained, and updated for each use case

**With MCP, you can:**
- Ask questions in natural language: *"What call queues do we have configured?"*
- Get instant answers without writing code
- Perform administrative tasks through conversation: *"Assign phone number X to user Y"*
- Access real-time data from your Webex organization
- Automate workflows through AI assistants

This makes Webex Calling management accessible to anyone, regardless of technical expertise.

## What Can It Do?

The MCP Webex Calling server provides **85+ tools** organized into the following categories:

### Data Retrieval
- Query Webex Calling users, locations, and organizations
- Retrieve call queue information, auto attendants, hunt groups, and trunk groups
- Get device and phone number information
- Query call history and detailed call records
- List licenses and user assignments

### User Management
- Create, update, and delete users
- Manage user extensions and phone numbers
- Assign and unassign licenses
- Search for users by name, email, or extension

### Location Management
- Create, update, and delete locations
- Manage location settings and configurations
- List all locations in the organization

### Call Queue Management
- Create, update, and delete call queues
- Manage queue members and settings
- Configure queue routing and overflow

### Auto Attendant Management
- Create, update, and delete auto attendants
- Configure menu options and greetings
- Manage business hours and schedules

### Hunt Group Management
- Create, update, and delete hunt groups
- Configure hunt group routing strategies
- Manage group members

### Device Management
- List and manage devices
- Associate devices with users
- Get device details and configurations
- Generate activation codes for device registration (no MAC address required)
- Create/provision devices by MAC address and model

### Reporting & Analytics
- Get call detail records (CDRs)
- Calculate call statistics (minutes, seconds, call count)
- Retrieve call analytics and metrics
- Generate reports for users, locations, or time periods

### Voicemail Management
- Configure voicemail settings
- Manage voicemail greetings and notifications

### Webhook & Event Management
- List and manage webhooks
- Configure event subscriptions
- Handle real-time notifications

## Use Cases

- **Quick Queries**: "What call queues do we have configured?" or "Show me all devices for user john@example.com"
- **Administrative Tasks**: "Assign phone number X to user Y" or "Create a new call queue called Support"
- **Device Provisioning**: "Generate an activation code for user john@example.com" or "Create a device with MAC address AABBCCDDEEFF"
- **Analytics & Reporting**: "Get call analytics for last month" or "Show me queue performance metrics"
- **Troubleshooting**: "What are the calling settings for user X?" or "List all devices at location Y"
- **Bulk Operations**: "Update extensions for all users in location X" or "List all licenses in the organization"

## Device Management

The server provides two methods for device provisioning:

### Activation Code Method (Recommended)

The simplest way to provision a device is by generating an activation code. This method requires only the user's person ID and doesn't need a MAC address:

1. **Generate an activation code** for the user
2. **Provide the code to the user** - they enter it on their device during setup
3. The device automatically registers and associates with their account

**Example:**
- *"Generate an activation code for user john@example.com"*

The activation code expires after a set period (typically several months), so users have plenty of time to set up their devices.

### MAC Address Method

For devices where you know the MAC address in advance, you can create the device entry directly:

1. **Create the device** using MAC address and model
2. **Associate the device** with a user (optional, can be done later)
3. The device will be ready for registration

**Example:**
- *"Create a device with MAC address AABBCCDDEEFF and model Cisco 8841"*

**MAC Address Format:**
- Accepts 12-digit hexadecimal format (e.g., `AABBCCDDEEFF`)
- Also accepts colon or dash separators (e.g., `AA:BB:CC:DD:EE:FF` or `AA-BB-CC-DD-EE-FF`)
- Automatically normalizes to uppercase format

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Webex access token (see [Configuration](#configuration) below)
- Claude Desktop (optional, for AI assistant integration)

### Installation

1. **Clone the repository:**
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

4. **Install the package:**
   ```bash
   pip install -e .
   ```

### Configuration

#### Getting a Webex Access Token

1. Go to [developer.webex.com](https://developer.webex.com)
2. Sign in with your Webex account
3. Click on your profile → **Personal Access Tokens**
4. Click **Generate Token**
5. Copy the generated token (it will only be shown once)

**Note:** Personal Access Tokens expire after 12 hours. For production use, see [Production Setup](#production-setup) below.

#### Setting Up Environment Variables

Create a `.env` file in the project root:

```bash
WEBEX_ACCESS_TOKEN=your_token_here
WEBEX_BASE_URL=https://webexapis.com/v1
```

**Security Note:** Never commit your `.env` file to version control. It's already in `.gitignore`.

### Running the Server

The server can be run directly:

```bash
python -m mcp_webexcalling.server
```

Or used with Claude Desktop (see [Connecting to Claude Desktop](#connecting-to-claude-desktop) below).

## Connecting to Claude Desktop

Follow these step-by-step instructions to connect the MCP Webex Calling server to Claude Desktop.

### Prerequisites

- Python 3.9+ installed
- Claude Desktop installed
- Webex access token (see [Configuration](#configuration) above)

### Step 1: Find Your Python Path

**macOS/Linux:**
```bash
which python3
# or
which python
```

**Windows (PowerShell):**
```powershell
where python
```

Note the path (e.g., `/opt/homebrew/bin/python3.12` or `C:\Python312\python.exe`).

### Step 2: Locate Claude Desktop Configuration

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

### Step 3: Configure Claude Desktop

Edit the configuration file and add the MCP server configuration:

```json
{
  "mcpServers": {
    "webex-calling": {
      "command": "/path/to/your/venv/bin/python",
      "args": ["-m", "mcp_webexcalling.server"],
      "cwd": "/path/to/mcp-webexcalling",
      "env": {
        "WEBEX_ACCESS_TOKEN": "your_token_here",
        "WEBEX_BASE_URL": "https://webexapis.com/v1"
      }
    }
  }
}
```

**Important:**
- Replace `/path/to/your/venv/bin/python` with your actual Python path from Step 1
- Replace `/path/to/mcp-webexcalling` with the actual path to this project
- Replace `your_token_here` with your Webex access token

### Step 4: Restart Claude Desktop

Close and reopen Claude Desktop to load the new configuration.

### Step 5: Verify Connection

Open Claude Desktop and check if the server is connected. You should see "webex-calling" in the MCP servers list.

### Troubleshooting

**Server disconnected:**
- Verify the Python path is correct and points to your virtual environment
- Check that the `cwd` path is correct
- Ensure the `.env` file has the correct token (or use the `env` section in the config)
- Check Claude Desktop logs for error messages

**Import errors:**
- Make sure you've installed the package: `pip install -e .`
- Verify all dependencies are installed: `pip install -r requirements.txt`

**Permission errors:**
- Ensure the Python executable has execute permissions
- Check that the project directory has read permissions

## Production Setup

Personal Access Tokens expire after 12 hours, making them unsuitable for production use. This section explains how to set up a permanent Webex Bot or Integration for long-term, production-ready authentication.

### Option 1: Webex Bot (Recommended)

1. Go to [developer.webex.com](https://developer.webex.com)
2. Navigate to **My Apps** → **Bots**
3. Click **Create a Bot**
4. Fill in the bot details:
   - **Name**: Your bot name
   - **Username**: Unique bot username (e.g., `mcp-webex-calling-bot`)
   - **Icon**: Optional bot icon
5. Click **Add Bot**
6. Copy the **Bot Access Token** (keep it secure!)
7. Add the bot to a Webex space where it will operate
8. Use the bot token in your `.env` file:
   ```
   WEBEX_ACCESS_TOKEN=your_bot_token_here
   ```

**Benefits:**
- Token never expires
- Can be assigned to specific spaces
- Easy to manage and revoke

### Option 2: Webex Integration

1. Go to [developer.webex.com](https://developer.webex.com)
2. Navigate to **My Apps** → **Integrations**
3. Click **Create an Integration**
4. Choose **Webex Calling** integration type
5. Fill in the required OAuth scopes:
   - `spark-admin:people_read`
   - `spark-admin:people_write`
   - `spark-admin:devices_read`
   - `spark-admin:devices_write`
   - `spark-admin:telephony_config_read`
   - `spark-admin:telephony_config_write`
6. Complete the OAuth flow to get a refresh token
7. Use the integration credentials in your application

**Benefits:**
- More granular permissions
- Better for enterprise deployments
- Supports OAuth refresh tokens

## GitHub Actions Integration: Webex Notifications

Set up automated notifications to a Webex space whenever code is pushed to the main branch using GitHub Actions.

### Setup

1. **Create a Webex Bot** (see [Production Setup](#production-setup) above)
2. **Get the Bot Token and Room ID:**
   - Bot Token: From the bot creation page
   - Room ID: Right-click the Webex space → **Copy Link** → Extract the room ID from the URL
3. **Add GitHub Secrets:**
   - Go to your repository → **Settings** → **Secrets and variables** → **Actions**
   - Add secret: `WEBEX_BOT_TOKEN` (your bot token)
   - Add secret: `WEBEX_ROOM_ID` (your room ID)
4. **The workflow is already configured** in `.github/workflows/webex-notifications.yml`

The workflow will automatically send notifications when code is pushed to `main`.

## Available Tools

The server provides **85+ MCP tools** organized by category. See the full list in the [What Can It Do?](#what-can-it-do) section above.

## Example Usage

### Through Claude Desktop

Once connected, you can ask questions like:

- *"Show me all call queues in the organization"*
- *"Get call statistics for the last 24 hours"*
- *"List all users at location X"*
- *"Create a new call queue called Support"*
- *"Assign phone number +1234567890 to user john@example.com"*
- *"Generate an activation code for user john@example.com"*
- *"Create a device with MAC address AABBCCDDEEFF and model Cisco 8841"*

### Direct API Usage

You can also use the client directly in Python:

```python
from mcp_webexcalling.webex_client import WebexClient

client = WebexClient(access_token="your_token")

# Get organization info
org_info = await client.get_organization_info()

# Get call queues
queues = await client.list_call_queues()

# Get call statistics
stats = await client.get_call_statistics_from_cdr(
    start_time="2024-01-01T00:00:00Z",
    end_time="2024-01-31T23:59:59Z"
)

# Generate activation code for a user
activation_code = await client.generate_activation_code(person_id="user_id_here")
print(f"Activation code: {activation_code['code']}")
print(f"Expires: {activation_code['expiryTime']}")

# Create a device by MAC address
device = await client.create_device_by_mac(
    mac_address="AABBCCDDEEFF",
    model="Cisco 8841"
)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
