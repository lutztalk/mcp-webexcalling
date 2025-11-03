# Setup Guide

## Installation

### 1. Clone or Navigate to the Project

```bash
cd mcp-webexcalling
```

### 2. Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install in development mode:

```bash
pip install -e .
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env  # If .env.example exists
# Or create manually:
touch .env
```

Edit `.env` and add your Webex credentials:

```env
WEBEX_ACCESS_TOKEN=your_webex_access_token_here
WEBEX_BASE_URL=https://webexapis.com/v1
```

### 5. Get Webex Access Token

#### Option A: Personal Access Token (Easiest)

1. Go to [Webex Developer Portal](https://developer.webex.com/)
2. Sign in with your Webex account
3. Click your profile → Personal Access Tokens
4. Click "Create a Token"
5. Name it (e.g., "MCP Server")
6. Copy the token and add it to your `.env` file

#### Option B: OAuth Integration

1. Go to [My Webex Apps](https://developer.webex.com/my-apps)
2. Create a new integration
3. Set up OAuth redirect URIs
4. Get Client ID and Client Secret
5. Implement OAuth flow to get access token

**Required Scopes for Webex Calling:**
- `spark:people_read` - Read people information
- `spark-admin:locations_read` - Read location information
- `spark-admin:organizations_read` - Read organization information
- `spark-admin:telephony_config_read` - Read calling configuration
- `spark-admin:read_call_history` - Read call history

### 6. Test the Setup

Run the example script to verify everything works:

```bash
python examples/basic_usage.py
```

You should see output showing your organization, locations, users, etc.

## Configure MCP Client

### Claude Desktop

Add to your MCP configuration file:

**macOS:**
`~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows:**
`%APPDATA%\Claude\claude_desktop_config.json`

**Linux:**
`~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "webex-calling": {
      "command": "python",
      "args": ["-m", "mcp_webexcalling.server"],
      "env": {
        "WEBEX_ACCESS_TOKEN": "your_token_here",
        "WEBEX_BASE_URL": "https://webexapis.com/v1"
      }
    }
  }
}
```

**Note:** Use absolute paths if needed:
```json
{
  "mcpServers": {
    "webex-calling": {
      "command": "/path/to/venv/bin/python",
      "args": ["-m", "mcp_webexcalling.server"],
      "cwd": "/path/to/mcp-webexcalling",
      "env": {
        "WEBEX_ACCESS_TOKEN": "your_token_here"
      }
    }
  }
}
```

### Other MCP Clients

The server uses stdio (standard input/output) for communication. Most MCP clients support this format:

```bash
python -m mcp_webexcalling.server
```

The server will read from stdin and write to stdout in the MCP protocol format.

## Troubleshooting

### Import Errors

If you get import errors:
```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Authentication Errors

If you see authentication errors:
1. Verify your token is correct in `.env`
2. Check token expiration
3. Ensure token has required scopes
4. Test token manually:
   ```bash
   curl -H "Authorization: Bearer YOUR_TOKEN" https://webexapis.com/v1/people/me
   ```

### MCP Connection Issues

If the MCP client can't connect:
1. Verify Python path is correct
2. Test server manually:
   ```bash
   python -m mcp_webexcalling.server
   ```
   (Should not output errors immediately)
3. Check MCP client logs for errors
4. Ensure all dependencies are installed

### Permission Errors

Some endpoints require admin privileges. If you get permission errors:
1. Verify your Webex account has admin access
2. Check that your token was generated with admin scopes
3. Contact your Webex administrator if needed

## Next Steps

Once setup is complete:
1. Read [USAGE.md](USAGE.md) for detailed tool documentation
2. Try the example queries in the README
3. Explore the available tools through your MCP client

