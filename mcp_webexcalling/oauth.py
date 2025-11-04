"""OAuth authentication support for Webex Calling MCP Server"""

import httpx
from typing import Optional, Dict, Any
from urllib.parse import urlencode, parse_qs, urlparse
import webbrowser
import http.server
import socketserver
from threading import Thread
import time


class WebexOAuth:
    """Handle OAuth 2.0 flow for Webex authentication"""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str = "http://localhost:8080/callback",
        scope: str = "spark:people_read spark-admin:locations_read spark-admin:organizations_read spark-admin:telephony_config_read spark-admin:read_call_history",
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.auth_url = "https://webexapis.com/v1/authorize"
        self.token_url = "https://webexapis.com/v1/access_token"
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None

    def get_authorization_url(self, state: Optional[str] = None) -> str:
        """Generate the OAuth authorization URL"""
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": self.scope,
        }
        if state:
            params["state"] = state

        return f"{self.auth_url}?{urlencode(params)}"

    async def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            response.raise_for_status()
            return response.json()

    async def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh an access token using refresh token"""
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            response.raise_for_status()
            return response.json()

    def start_local_server(self, port: int = 8080) -> tuple[dict[str, Optional[str]], Thread]:
        """Start a local HTTP server to receive OAuth callback"""
        result = {"code": None, "error": None}

        class OAuthHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path.startswith("/callback"):
                    # Parse query parameters
                    parsed = urlparse(self.path)
                    params = parse_qs(parsed.query)

                    if "code" in params:
                        result["code"] = params["code"][0]
                        self.send_response(200)
                        self.send_header("Content-type", "text/html")
                        self.end_headers()
                        self.wfile.write(
                            b"<html><body><h1>Authorization Successful!</h1><p>You can close this window.</p></body></html>"
                        )
                    elif "error" in params:
                        result["error"] = params["error"][0]
                        self.send_response(400)
                        self.send_header("Content-type", "text/html")
                        self.end_headers()
                        self.wfile.write(
                            f"<html><body><h1>Authorization Failed</h1><p>Error: {result['error']}</p></body></html>".encode()
                        )
                else:
                    self.send_response(404)
                    self.end_headers()

            def log_message(self, format, *args):
                pass  # Suppress server logs

        server = socketserver.TCPServer(("", port), OAuthHandler)
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()

        return result, thread

    def authenticate(self) -> Optional[str]:
        """Complete OAuth flow and return access token"""
        # Generate authorization URL
        auth_url = self.get_authorization_url()

        # Start local server for callback
        result, server_thread = self.start_local_server()

        # Open browser for authorization
        print(f"Opening browser for authorization: {auth_url}")
        webbrowser.open(auth_url)

        # Wait for callback (timeout after 5 minutes)
        timeout = 300
        start_time = time.time()
        while result["code"] is None and result["error"] is None:
            if time.time() - start_time > timeout:
                print("Authorization timeout")
                server_thread.join(timeout=1)
                return None
            time.sleep(0.5)

        if result["error"]:
            print(f"Authorization error: {result['error']}")
            server_thread.join(timeout=1)
            return None

        if result["code"]:
            # Exchange code for token (run async function)
            import asyncio
            token_response = asyncio.run(self.exchange_code_for_token(result["code"]))
            self.access_token = token_response.get("access_token")
            self.refresh_token = token_response.get("refresh_token")
            server_thread.join(timeout=1)
            return self.access_token

        server_thread.join(timeout=1)
        return None

