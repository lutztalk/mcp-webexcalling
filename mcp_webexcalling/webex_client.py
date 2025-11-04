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

    # ========== License Management ==========
    
    async def list_licenses(
        self, org_id: Optional[str] = None, max_results: int = 100
    ) -> List[Dict[str, Any]]:
        """List all licenses in the organization"""
        params = {"max": max_results}
        if org_id:
            params["orgId"] = org_id

        response = await self._request("GET", "/licenses", params=params)
        return response.get("items", [])

    async def get_license_details(self, license_id: str) -> Dict[str, Any]:
        """Get details about a specific license"""
        return await self._request("GET", f"/licenses/{license_id}")

    async def list_user_licenses(
        self, person_id: str
    ) -> List[Dict[str, Any]]:
        """List licenses assigned to a user"""
        response = await self._request("GET", f"/people/{person_id}/licenses")
        return response.get("items", [])

    async def assign_license_to_user(
        self, person_id: str, license_id: str
    ) -> Dict[str, Any]:
        """Assign a license to a user"""
        return await self._request(
            "POST",
            f"/people/{person_id}/licenses",
            json_data={"id": license_id}
        )

    async def remove_license_from_user(
        self, person_id: str, license_id: str
    ) -> Dict[str, Any]:
        """Remove a license from a user"""
        return await self._request(
            "DELETE",
            f"/people/{person_id}/licenses/{license_id}"
        )

    # ========== Device Management ==========

    async def list_devices(
        self,
        person_id: Optional[str] = None,
        location_id: Optional[str] = None,
        max_results: int = 100,
    ) -> List[Dict[str, Any]]:
        """List devices"""
        params = {"max": max_results}
        if person_id:
            params["personId"] = person_id
        if location_id:
            params["locationId"] = location_id

        response = await self._request("GET", "/devices", params=params)
        return response.get("items", [])

    async def get_device_details(self, device_id: str) -> Dict[str, Any]:
        """Get details about a specific device"""
        return await self._request("GET", f"/devices/{device_id}")

    # ========== Phone Numbers ==========

    async def list_phone_numbers(
        self,
        location_id: Optional[str] = None,
        org_id: Optional[str] = None,
        number: Optional[str] = None,
        max_results: int = 100,
    ) -> List[Dict[str, Any]]:
        """List phone numbers"""
        params = {"max": max_results}
        if location_id:
            params["locationId"] = location_id
        if org_id:
            params["orgId"] = org_id
        if number:
            params["number"] = number

        response = await self._request("GET", "/telephony/config/numbers", params=params)
        return response.get("items", [])

    async def get_phone_number_details(self, number_id: str) -> Dict[str, Any]:
        """Get details about a specific phone number"""
        return await self._request("GET", f"/telephony/config/numbers/{number_id}")

    # ========== User Extension Management ==========

    async def update_user_extension(
        self,
        person_id: str,
        extension: Optional[str] = None,
        extension_dial: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone_number: Optional[str] = None,
        mobile_number: Optional[str] = None,
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update user calling extension and settings"""
        # First get current settings
        current_settings = await self.get_user_calling_settings(person_id)
        
        # Build update payload
        update_data = {}
        if extension is not None:
            update_data["extension"] = extension
        if extension_dial is not None:
            update_data["extensionDial"] = extension_dial
        if first_name is not None:
            update_data["firstName"] = first_name
        if last_name is not None:
            update_data["lastName"] = last_name
        if phone_number is not None:
            update_data["phoneNumber"] = phone_number
        if mobile_number is not None:
            update_data["mobileNumber"] = mobile_number
        if location_id is not None:
            update_data["locationId"] = location_id

        # Merge with existing settings
        update_data = {**current_settings, **update_data}

        return await self._request(
            "PUT",
            f"/telephony/config/people/{person_id}",
            json_data=update_data
        )

    async def assign_phone_number_to_user(
        self, person_id: str, phone_number_id: str
    ) -> Dict[str, Any]:
        """Assign a phone number to a user"""
        # Get current settings
        current_settings = await self.get_user_calling_settings(person_id)
        
        # Get phone number details
        number_details = await self.get_phone_number_details(phone_number_id)
        
        # Update with new phone number
        update_data = {**current_settings}
        update_data["phoneNumber"] = number_details.get("number")

        return await self._request(
            "PUT",
            f"/telephony/config/people/{person_id}",
            json_data=update_data
        )

    async def update_user_calling_features(
        self,
        person_id: str,
        call_park_enabled: Optional[bool] = None,
        call_forwarding_enabled: Optional[bool] = None,
        voicemail_enabled: Optional[bool] = None,
        call_recording_enabled: Optional[bool] = None,
        call_waiting_enabled: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Update user calling features"""
        current_settings = await self.get_user_calling_settings(person_id)
        
        update_data = {**current_settings}
        
        # Update features if provided
        if "features" not in update_data:
            update_data["features"] = {}
        
        if call_park_enabled is not None:
            update_data["features"]["callPark"] = {"enabled": call_park_enabled}
        if call_forwarding_enabled is not None:
            update_data["features"]["callForwarding"] = {"enabled": call_forwarding_enabled}
        if voicemail_enabled is not None:
            update_data["features"]["voicemail"] = {"enabled": voicemail_enabled}
        if call_recording_enabled is not None:
            update_data["features"]["callRecording"] = {"enabled": call_recording_enabled}
        if call_waiting_enabled is not None:
            update_data["features"]["callWaiting"] = {"enabled": call_waiting_enabled}

        return await self._request(
            "PUT",
            f"/telephony/config/people/{person_id}",
            json_data=update_data
        )

    # ========== Reporting and Analytics ==========

    async def get_call_detail_records(
        self,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        person_id: Optional[str] = None,
        location_id: Optional[str] = None,
        max_results: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get call detail records (CDRs) for reporting"""
        params = {"max": max_results}
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        if person_id:
            params["personId"] = person_id
        if location_id:
            params["locationId"] = location_id

        response = await self._request("GET", "/telephony/calls/callHistory", params=params)
        return response.get("items", [])

    async def get_call_analytics(
        self,
        start_time: str,
        end_time: str,
        location_id: Optional[str] = None,
        org_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get call analytics and statistics"""
        params = {
            "startTime": start_time,
            "endTime": end_time,
        }
        if location_id:
            params["locationId"] = location_id
        if org_id:
            params["orgId"] = org_id

        # Aggregate call history data for analytics
        call_history = await self.get_call_detail_records(
            start_time=start_time,
            end_time=end_time,
            location_id=location_id,
            max_results=1000
        )

        # Calculate basic analytics
        total_calls = len(call_history)
        completed_calls = sum(1 for call in call_history if call.get("status") == "completed")
        missed_calls = sum(1 for call in call_history if call.get("status") == "missed")
        total_duration = sum(
            call.get("duration", 0) for call in call_history
            if call.get("duration")
        )

        return {
            "totalCalls": total_calls,
            "completedCalls": completed_calls,
            "missedCalls": missed_calls,
            "totalDuration": total_duration,
            "averageDuration": total_duration / completed_calls if completed_calls > 0 else 0,
            "callHistory": call_history[:100],  # Return first 100 for details
        }

    async def get_queue_analytics(
        self,
        queue_id: str,
        start_time: str,
        end_time: str,
    ) -> Dict[str, Any]:
        """Get analytics for a specific call queue"""
        params = {
            "startTime": start_time,
            "endTime": end_time,
        }

        # Get queue details
        queue_details = await self.get_call_queue_details(queue_id)
        
        # Get call history filtered by queue
        # Note: This may require additional API endpoints depending on Webex API
        call_history = await self.get_call_detail_records(
            start_time=start_time,
            end_time=end_time,
            max_results=1000
        )

        # Filter calls related to this queue (if queue information is in call history)
        queue_calls = [
            call for call in call_history
            if queue_id in str(call.get("queueId", ""))
        ]

        return {
            "queueId": queue_id,
            "queueName": queue_details.get("name"),
            "totalCalls": len(queue_calls),
            "calls": queue_calls[:100],
        }

    # ========== Additional Data Retrieval ==========

    async def list_trunk_groups(
        self, location_id: Optional[str] = None, max_results: int = 100
    ) -> List[Dict[str, Any]]:
        """List trunk groups"""
        params = {"max": max_results}
        if location_id:
            params["locationId"] = location_id

        response = await self._request("GET", "/telephony/config/trunkGroups", params=params)
        return response.get("items", [])

    async def get_trunk_group_details(self, trunk_group_id: str) -> Dict[str, Any]:
        """Get details about a specific trunk group"""
        return await self._request("GET", f"/telephony/config/trunkGroups/{trunk_group_id}")

    async def list_hunt_groups(
        self, location_id: Optional[str] = None, max_results: int = 100
    ) -> List[Dict[str, Any]]:
        """List hunt groups"""
        params = {"max": max_results}
        if location_id:
            params["locationId"] = location_id

        response = await self._request("GET", "/telephony/config/huntGroups", params=params)
        return response.get("items", [])

    async def get_hunt_group_details(self, hunt_group_id: str) -> Dict[str, Any]:
        """Get details about a specific hunt group"""
        return await self._request("GET", f"/telephony/config/huntGroups/{hunt_group_id}")

    async def list_call_park_extensions(
        self, location_id: Optional[str] = None, max_results: int = 100
    ) -> List[Dict[str, Any]]:
        """List call park extensions"""
        params = {"max": max_results}
        if location_id:
            params["locationId"] = location_id

        response = await self._request("GET", "/telephony/config/callPark", params=params)
        return response.get("items", [])

    async def get_location_features(self, location_id: str) -> Dict[str, Any]:
        """Get available features for a location"""
        location = await self.get_location_details(location_id)
        return location.get("features", {})

