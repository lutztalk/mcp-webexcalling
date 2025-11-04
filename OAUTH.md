# OAuth Authentication Support

The MCP Webex Calling server supports OAuth 2.0 authentication for secure access to Webex Calling APIs.

## Setup

### 1. Create a Webex Integration

1. Go to [Webex Developer Portal](https://developer.webex.com/)
2. Sign in with your Webex account
3. Navigate to [My Webex Apps](https://developer.webex.com/my-apps)
4. Click "Create a New App"
5. Choose "Integration"
6. Fill in the app details:
   - **Name**: Your app name (e.g., "MCP Webex Calling")
   - **Description**: Brief description
   - **Redirect URI**: `http://localhost:8080/callback` (or your custom redirect URI)
7. Save your **Client ID** and **Client Secret**

### 2. Configure OAuth Credentials

Add OAuth credentials to your `.env` file:

```env
WEBEX_CLIENT_ID=your_client_id_here
WEBEX_CLIENT_SECRET=your_client_secret_here
WEBEX_REDIRECT_URI=http://localhost:8080/callback
WEBEX_OAUTH_SCOPE=spark:people_read spark-admin:locations_read spark-admin:organizations_read spark-admin:telephony_config_read spark-admin:read_call_history
```

**Note**: You can still use `WEBEX_ACCESS_TOKEN` for direct token authentication. OAuth is optional.

## OAuth Flow

### Using MCP Tools

1. **Get Authorization URL**:
   ```
   Use tool: get_oauth_authorization_url
   ```
   This returns a URL you need to visit to authorize the application.

2. **Visit the Authorization URL**:
   - Open the URL in your browser
   - Sign in to Webex
   - Authorize the application
   - You'll be redirected to the callback URL with an authorization code

3. **Exchange Code for Token**:
   ```
   Use tool: exchange_oauth_code
   Parameters:
   - code: <authorization_code_from_url>
   ```
   This returns your access token and refresh token.

4. **Update .env File**:
   Add the tokens to your `.env` file:
   ```env
   WEBEX_ACCESS_TOKEN=your_access_token_here
   WEBEX_REFRESH_TOKEN=your_refresh_token_here
   ```

### Using MCP Prompts

If OAuth credentials are configured, you can use the `initiate_webex_oauth` prompt:

```
Use prompt: initiate_webex_oauth
```

This will guide you through the OAuth flow.

## Available OAuth Tools

### `get_oauth_authorization_url`
Get the OAuth authorization URL to initiate authentication.

**Parameters**:
- `redirect_uri` (optional): Custom redirect URI (defaults to configured value)

### `exchange_oauth_code`
Exchange an OAuth authorization code for an access token.

**Parameters**:
- `code` (required): Authorization code from the OAuth callback
- `redirect_uri` (optional): Redirect URI used in authorization (must match)

### `refresh_oauth_token`
Refresh an access token using a refresh token.

**Parameters**:
- `refresh_token` (required): Refresh token from previous authentication

### `get_oauth_status`
Get current OAuth authentication status.

**Returns**:
- `oauth_configured`: Whether OAuth credentials are configured
- `authenticated`: Whether an access token is available
- `has_refresh_token`: Whether a refresh token is available
- `client_id_configured`: Whether client ID is set
- `client_secret_configured`: Whether client secret is set

## MCP Resources

### `webex://oauth/status`
Read the current OAuth authentication status as a JSON resource.

## Token Refresh

Access tokens expire after a period. Use the `refresh_oauth_token` tool to get a new access token:

1. Call `refresh_oauth_token` with your refresh token
2. Update `WEBEX_ACCESS_TOKEN` in your `.env` file with the new token
3. Optionally update `WEBEX_REFRESH_TOKEN` if a new refresh token is provided

## Scopes

The default OAuth scope includes:
- `spark:people_read` - Read people information
- `spark-admin:locations_read` - Read location information
- `spark-admin:organizations_read` - Read organization information
- `spark-admin:telephony_config_read` - Read calling configuration
- `spark-admin:read_call_history` - Read call history

You can customize the scope by setting `WEBEX_OAUTH_SCOPE` in your `.env` file.

## Security Notes

1. **Never commit** your `.env` file or client secrets to version control
2. **Keep refresh tokens secure** - they can be used to obtain new access tokens
3. **Use HTTPS** for production redirect URIs
4. **Rotate credentials** if they are compromised

## Troubleshooting

### "OAuth credentials not configured"
- Ensure `WEBEX_CLIENT_ID` and `WEBEX_CLIENT_SECRET` are set in your `.env` file

### "Invalid redirect URI"
- The redirect URI in the authorization request must match the one configured in your Webex app
- Check that `WEBEX_REDIRECT_URI` matches your app's redirect URI

### "Invalid authorization code"
- Authorization codes expire quickly (usually within minutes)
- Make sure you're using the code immediately after receiving it
- The code can only be used once

### "Token expired"
- Access tokens expire after a period (typically 14 days for Webex)
- Use `refresh_oauth_token` to get a new access token

