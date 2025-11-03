"""Webex API Client for interacting with Webex Calling APIs"""

import httpx
from typing import Optional, Dict, Any, List
from .config import get_settings


class WebexClient:
    """Client for interacting with Webex APIs"""

    def __init__(self, access_token: Optional[str] = None, base_url: Optional[str] = None):
        settings = get_settings()
        self.access_token = access_token or settings.webex_access_token
        self.base_url = base_url or settings.webex_base_url
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make an HTTP request to the Webex API"""
        url = f"{self.base_url}{endpoint}"

        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=json_data,
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()

    async def get_organization_info(self) -> Dict[str, Any]:
        """Get information about the organization"""
        return await self._request("GET", "/organizations")

    async def get_my_info(self) -> Dict[str, Any]:
        """Get information about the authenticated user"""
        return await self._request("GET", "/people/me")

    async def list_locations(
        self, org_id: Optional[str] = None, max_results: int = 100
    ) -> List[Dict[str, Any]]:
        """List all locations in the organization"""
        params = {"max": max_results}
        if org_id:
            params["orgId"] = org_id

        response = await self._request("GET", "/locations", params=params)
        return response.get("items", [])

    async def get_location_details(self, location_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific location"""
        return await self._request("GET", f"/locations/{location_id}")

    async def list_users(
        self,
        org_id: Optional[str] = None,
        location_id: Optional[str] = None,
        max_results: int = 100,
    ) -> List[Dict[str, Any]]:
        """List users in the organization"""
        params = {"max": max_results}
        if org_id:
            params["orgId"] = org_id
        if location_id:
            params["locationId"] = location_id

        response = await self._request("GET", "/people", params=params)
        return response.get("items", [])

    async def get_user_details(self, person_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific user"""
        return await self._request("GET", f"/people/{person_id}")

    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user information by email address"""
        params = {"email": email}
        response = await self._request("GET", "/people", params=params)
        items = response.get("items", [])
        return items[0] if items else None

    async def get_user_calling_settings(self, person_id: str) -> Dict[str, Any]:
        """Get calling settings for a user"""
        return await self._request("GET", f"/telephony/config/people/{person_id}")

    async def list_call_queues(
        self, location_id: Optional[str] = None, max_results: int = 100
    ) -> List[Dict[str, Any]]:
        """List all call queues"""
        params = {"max": max_results}
        if location_id:
            params["locationId"] = location_id

        response = await self._request("GET", "/telephony/config/queues", params=params)
        return response.get("items", [])

    async def get_call_queue_details(self, queue_id: str) -> Dict[str, Any]:
        """Get details about a specific call queue"""
        return await self._request("GET", f"/telephony/config/queues/{queue_id}")

    async def list_auto_attendants(
        self, location_id: Optional[str] = None, max_results: int = 100
    ) -> List[Dict[str, Any]]:
        """List all auto attendants"""
        params = {"max": max_results}
        if location_id:
            params["locationId"] = location_id

        response = await self._request("GET", "/telephony/config/autoAttendants", params=params)
        return response.get("items", [])

    async def get_auto_attendant_details(self, auto_attendant_id: str) -> Dict[str, Any]:
        """Get details about a specific auto attendant"""
        return await self._request(
            "GET", f"/telephony/config/autoAttendants/{auto_attendant_id}"
        )

    async def get_call_history(
        self,
        person_id: Optional[str] = None,
        location_id: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        max_results: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get call history"""
        params = {"max": max_results}
        if person_id:
            params["personId"] = person_id
        if location_id:
            params["locationId"] = location_id
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time

        response = await self._request("GET", "/telephony/calls/callHistory", params=params)
        return response.get("items", [])

    async def search_users(
        self, query: str, org_id: Optional[str] = None, max_results: int = 100
    ) -> List[Dict[str, Any]]:
        """Search for users by display name or email"""
        params = {"displayName": query, "max": max_results}
        if org_id:
            params["orgId"] = org_id

        response = await self._request("GET", "/people", params=params)
        # Also try searching by email
        email_response = await self._request("GET", "/people", params={"email": query, "max": max_results})
        
        # Combine and deduplicate results
        results = {}
        for item in response.get("items", []):
            results[item.get("id")] = item
        for item in email_response.get("items", []):
            results[item.get("id")] = item
        
        return list(results.values())

