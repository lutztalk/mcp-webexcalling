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
            try:
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
            except httpx.HTTPStatusError as e:
                # Provide detailed error information
                error_msg = f"HTTP {e.response.status_code} error for {method} {endpoint}"
                
                # Try to get full error details from response
                try:
                    error_body = e.response.json()
                    # Include full error body for debugging
                    full_error = str(error_body)
                    if "message" in error_body:
                        error_msg += f": {error_body['message']}"
                    elif "errors" in error_body:
                        error_msg += f": {error_body['errors']}"
                    elif "error" in error_body:
                        error_msg += f": {error_body['error']}"
                    elif "description" in error_body:
                        error_msg += f": {error_body['description']}"
                    else:
                        # Include full error body if no standard fields found
                        error_msg += f": {full_error[:500]}"
                except:
                    error_msg += f": {e.response.text[:500]}"
                
                # For 400 errors, include the actual request URL and params for debugging
                if e.response.status_code == 400:
                    import urllib.parse
                    if params:
                        query_string = urllib.parse.urlencode(params)
                        error_msg += f"\n   Request URL: {url}?{query_string}"
                    else:
                        error_msg += f"\n   Request URL: {url}"
                
                # Provide helpful context for common errors
                if e.response.status_code == 400:
                    error_msg += " (Bad Request - check parameter formats, especially date/time formats)"
                elif e.response.status_code == 401:
                    error_msg += " (Authentication failed - check your access token)"
                elif e.response.status_code == 403:
                    error_msg += " (Permission denied - ensure you have admin access and required scopes)"
                elif e.response.status_code == 404:
                    error_msg += f" (Endpoint not found - {endpoint} may not exist or be available for your organization)"
                elif e.response.status_code == 429:
                    error_msg += " (Rate limit exceeded - wait before retrying)"
                
                raise Exception(error_msg) from e
            except httpx.RequestError as e:
                raise Exception(f"Request failed for {method} {endpoint}: {str(e)}") from e

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
        """Get call history - uses the same endpoint as get_call_detail_records"""
        return await self.get_call_detail_records(
            start_time=start_time,
            end_time=end_time,
            person_id=person_id,
            location_id=location_id,
            max_results=max_results,
        )

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
        """Get call detail records (CDRs) for reporting
        
        Uses the Webex Calling API detailed call history endpoint:
        https://developer.webex.com/calling/docs/api/v1/reports-detailed-call-history/get-detailed-call-history
        
        Endpoint: /cdr_feed
        Base URL: https://analytics.webexapis.com/v1
        
        Requires: "Webex Calling Detailed Call History API access" role assigned by an administrator.
        """
        # Required parameters
        if not start_time:
            raise ValueError("start_time is required for call detail records")
        if not end_time:
            raise ValueError("end_time is required for call detail records")
        
        # Build query parameters according to API documentation
        # The API expects ISO 8601 format dates in UTC
        # Format dates properly - ensure they're strings in correct format
        
        def format_date_for_api(date_val, format_type='iso_ms'):
            """Format date for API - handles both string and datetime objects
            
            format_type options:
            - 'iso_ms': ISO 8601 with actual milliseconds (YYYY-MM-DDTHH:MM:SS.mmmZ) - PREFERRED
            - 'iso': ISO 8601 without milliseconds (YYYY-MM-DDTHH:MM:SSZ)
            - 'epoch': Unix epoch timestamp in milliseconds
            """
            from datetime import datetime, timezone
            
            if isinstance(date_val, str):
                # If it's already a string, validate and clean it
                cleaned = date_val.strip()
                
                # Convert to datetime first for consistent handling
                try:
                    # Try parsing as ISO 8601
                    if 'T' in cleaned:
                        # Parse ISO format with or without milliseconds
                        if '.' in cleaned and 'Z' in cleaned:
                            # Has milliseconds: 2022-06-09T23:27:18.604Z or 2022-06-09T23:27:18.000Z
                            dt_str = cleaned.replace('Z', '+00:00')
                            dt = datetime.fromisoformat(dt_str)
                        elif 'Z' in cleaned:
                            # No milliseconds: 2022-06-09T23:27:18Z
                            dt_str = cleaned.replace('Z', '+00:00')
                            dt = datetime.fromisoformat(dt_str)
                        elif '+' in cleaned or '-' in cleaned[-6:]:
                            dt = datetime.fromisoformat(cleaned)
                        else:
                            dt = datetime.fromisoformat(cleaned)
                            dt = dt.replace(tzinfo=timezone.utc)
                    else:
                        # Try other formats
                        dt = datetime.fromisoformat(cleaned)
                        if dt.tzinfo is None:
                            dt = dt.replace(tzinfo=timezone.utc)
                except Exception as e:
                    # If parsing fails and format_type is 'iso_ms', we MUST add milliseconds
                    # Don't return a string without milliseconds - API requires them
                    if format_type == 'iso_ms':
                        # Try to extract date parts and add milliseconds
                        # If it has .000Z, keep it but we'll replace with actual milliseconds
                        if cleaned.endswith(".000Z") or cleaned.endswith("Z"):
                            # Try to parse without the Z and add milliseconds
                            try:
                                clean_no_z = cleaned.replace('Z', '').replace('.000', '')
                                if 'T' in clean_no_z:
                                    dt_temp = datetime.fromisoformat(clean_no_z)
                                    dt_temp = dt_temp.replace(tzinfo=timezone.utc)
                                    milliseconds = dt_temp.microsecond // 1000
                                    if milliseconds == 0:
                                        milliseconds = 1
                                    return dt_temp.strftime(f"%Y-%m-%dT%H:%M:%S.{milliseconds:03d}Z")
                            except:
                                pass
                    # If we can't parse, return as-is (but this should rarely happen)
                    return cleaned
            else:
                # Already a datetime object
                dt = date_val
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
            
            # Format based on requested type
            if format_type == 'iso_ms':
                # Include actual milliseconds (3 digits) - API REQUIRES this format
                # Format: YYYY-MM-DDTHH:MM:SS.mmmZ (e.g., 2022-06-08T21:27:00.604Z)
                # Convert microseconds to milliseconds (0-999)
                milliseconds = dt.microsecond // 1000
                # If microseconds are 0, use a small random value to ensure we have actual milliseconds
                # This prevents .000Z which might not be accepted
                if milliseconds == 0:
                    # Use a small offset to ensure we have non-zero milliseconds
                    # This is better than .000Z which the API might reject
                    milliseconds = 1
                return dt.strftime(f"%Y-%m-%dT%H:%M:%S.{milliseconds:03d}Z")
            elif format_type == 'iso':
                return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
            elif format_type == 'epoch':
                # Return epoch timestamp in milliseconds
                return str(int(dt.timestamp() * 1000))
            else:
                return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # API REQUIRES ISO 8601 format with milliseconds: YYYY-MM-DDTHH:MM:SS.mmmZ
        # According to API docs: "Must be formatted as YYYY-MM-DDTHH:MM:SS.mmmZ"
        # Example: "2022-06-08T21:27:00.604Z"
        # DO NOT use formats without milliseconds - API will reject them
        
        # Format with actual milliseconds (REQUIRED by API - no exceptions)
        start_time_iso_ms = format_date_for_api(start_time, format_type='iso_ms')
        end_time_iso_ms = format_date_for_api(end_time, format_type='iso_ms')
        
        # Build base parameters (using ISO format WITH milliseconds - API REQUIRES this)
        base_params = {
            "startTime": start_time_iso_ms,
            "endTime": end_time_iso_ms,
        }
        
        # Optional filters
        if location_id:
            # API uses "locations" parameter (may accept comma-separated list)
            base_params["locations"] = location_id
        
        if max_results:
            base_params["max"] = max_results
        
        # Try different parameter variations
        # API REQUIRES: YYYY-MM-DDTHH:MM:SS.mmmZ format (ISO 8601 with milliseconds)
        # DO NOT try formats without milliseconds - API will reject with "Invalid input string"
        param_variations = [
            # 1. Minimal parameters with ISO format WITH milliseconds (REQUIRED by API) - try this first
            {
                "startTime": start_time_iso_ms,
                "endTime": end_time_iso_ms,
            },
            # 2. Standard format with all parameters (ISO with ms)
            base_params.copy(),
            # 3. Without max parameter
            {k: v for k, v in base_params.items() if k != "max"},
            # 4. Without location parameter
            {k: v for k, v in base_params.items() if k != "locations"},
            # Note: We do NOT try without milliseconds - API explicitly requires .mmm format
        ]
        
        # Note: person_id is not directly supported by /cdr_feed endpoint
        # We'll filter by person_id after retrieving records if needed
        
        # Use the correct endpoint and base URL
        # Base URL: https://analytics.webexapis.com/v1
        # Endpoint: /cdr_feed
        endpoint = "/cdr_feed"
        analytics_base_url = "https://analytics.webexapis.com/v1"
        
        # Temporarily switch to analytics base URL
        original_base = self.base_url
        last_error = None
        
        try:
            self.base_url = analytics_base_url
            
            # Try different parameter variations
            response = None
            attempt_count = 0
            for param_set in param_variations:
                attempt_count += 1
                try:
                    response = await self._request("GET", endpoint, params=param_set)
                    # If successful, break out of loop
                    break
                except Exception as e:
                    last_error = e
                    error_str = str(e)
                    # If it's a 400 error about invalid input/string, try next parameter variation
                    # (but all variations use milliseconds format as required by API)
                    if "400" in error_str and ("invalid" in error_str.lower() or "input" in error_str.lower() or "string" in error_str.lower()):
                        # Try next variation (different parameter combinations, but all with milliseconds)
                        if attempt_count < len(param_variations):
                            continue
                    # For other errors (401, 403, etc.), raise immediately
                    raise
            
            if response is None and last_error:
                # All parameter variations failed
                # Provide helpful error message with what we tried
                error_msg = str(last_error)
                
                # Check if dates are in valid range (API requires 5 minutes to 48 hours ago)
                from datetime import datetime, timezone, timedelta
                now = datetime.now(timezone.utc)
                min_time = now - timedelta(hours=48)
                max_time = now - timedelta(minutes=5)
                
                try:
                    start_dt = datetime.fromisoformat(start_time_iso_ms.replace('Z', '+00:00'))
                    end_dt = datetime.fromisoformat(end_time_iso_ms.replace('Z', '+00:00'))
                    
                    date_range_issues = []
                    if start_dt < min_time:
                        date_range_issues.append(f"startTime ({start_time_iso_ms}) is more than 48 hours ago")
                    if start_dt > max_time:
                        date_range_issues.append(f"startTime ({start_time_iso_ms}) is less than 5 minutes ago")
                    if end_dt < min_time:
                        date_range_issues.append(f"endTime ({end_time_iso_ms}) is more than 48 hours ago")
                    if end_dt > max_time:
                        date_range_issues.append(f"endTime ({end_time_iso_ms}) is less than 5 minutes ago")
                    if start_dt > end_dt:
                        date_range_issues.append(f"startTime must be before endTime")
                    
                    if date_range_issues:
                        range_msg = "\n".join([f"  - {issue}" for issue in date_range_issues])
                        raise Exception(
                            f"Failed to retrieve call detail records. "
                            f"Date range validation failed:\n{range_msg}\n\n"
                            f"API requires: startTime and endTime must be between 5 minutes ago and 48 hours ago. "
                            f"Last API error: {error_msg}"
                        )
                except:
                    pass  # If we can't parse dates, just show the original error
                
                raise Exception(
                    f"Failed to retrieve call detail records after trying {len(param_variations)} different parameter combinations. "
                    f"Last error: {error_msg}. "
                    f"\n\nDate format used: {start_time_iso_ms} to {end_time_iso_ms} "
                    f"(ISO 8601 with milliseconds as required by API). "
                    f"\n\nNote: API requires dates to be between 5 minutes ago and 48 hours ago. "
                    f"If dates are in range, the format may still be incorrect. "
                    f"Please check the API documentation for the exact expected format."
                )
            
            # The API returns a list of call records directly
            records = []
            if isinstance(response, list):
                records = response
            elif isinstance(response, dict):
                # Try common response structures
                if "items" in response:
                    records = response.get("items", [])
                elif "data" in response:
                    records = response.get("data", [])
                elif "calls" in response:
                    records = response.get("calls", [])
                elif "cdr" in response:
                    records = response.get("cdr", [])
                else:
                    # Return the response as a single-item list if unexpected structure
                    records = [response] if response else []
            
            # Filter by person_id if provided (since API doesn't support it directly)
            if person_id and records:
                # Filter records where the person matches
                filtered_records = []
                for record in records:
                    # Check various fields where person_id might appear
                    from_person = record.get("from", {}).get("personId") if isinstance(record.get("from"), dict) else None
                    to_person = record.get("to", {}).get("personId") if isinstance(record.get("to"), dict) else None
                    record_person_id = record.get("personId") or record.get("person_id")
                    
                    if person_id in [from_person, to_person, record_person_id]:
                        filtered_records.append(record)
                records = filtered_records
            
            return records
            
        except Exception as e:
            error_msg = str(e)
            # Provide helpful error message based on common issues
            if "403" in error_msg or "Forbidden" in error_msg:
                raise Exception(
                    f"Access denied (403 Forbidden). "
                    f"You need the 'Webex Calling Detailed Call History API access' role. "
                    f"This role must be assigned by another administrator - you cannot assign it to yourself. "
                    f"Contact your Webex administrator to assign this role to your account. "
                    f"Original error: {error_msg}"
                )
            elif "401" in error_msg or "Unauthorized" in error_msg:
                raise Exception(
                    f"Authentication failed. Check your access token and ensure it has the required scopes. "
                    f"Original error: {error_msg}"
                )
            elif "404" in error_msg:
                raise Exception(
                    f"Endpoint not found (404). "
                    f"Using endpoint: {analytics_base_url}{endpoint}. "
                    f"Verify your organization has Webex Calling enabled and the endpoint is available. "
                    f"Original error: {error_msg}"
                )
            else:
                raise Exception(
                    f"Failed to retrieve call detail records from {analytics_base_url}{endpoint}. "
                    f"Error: {error_msg}. "
                    f"Ensure you have the 'Webex Calling Detailed Call History API access' role assigned."
                )
        finally:
            # Always restore original base URL
            self.base_url = original_base

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

    # ========== Enhanced Device Management ==========

    async def associate_device_to_user(
        self, device_id: str, person_id: str
    ) -> Dict[str, Any]:
        """Associate a device to a user"""
        return await self._request(
            "PUT",
            f"/devices/{device_id}",
            json_data={"personId": person_id}
        )

    async def unassociate_device(self, device_id: str) -> Dict[str, Any]:
        """Unassociate a device from a user"""
        return await self._request(
            "PUT",
            f"/devices/{device_id}",
            json_data={"personId": None}
        )

    async def provision_device(
        self, device_id: str, person_id: str, location_id: str
    ) -> Dict[str, Any]:
        """Provision a device for a user"""
        return await self._request(
            "PUT",
            f"/devices/{device_id}",
            json_data={
                "personId": person_id,
                "locationId": location_id,
                "provisioning": {"method": "automatic"}
            }
        )

    async def activate_device(self, device_id: str) -> Dict[str, Any]:
        """Activate a device"""
        return await self._request(
            "POST",
            f"/devices/{device_id}/activate"
        )

    async def deactivate_device(self, device_id: str) -> Dict[str, Any]:
        """Deactivate a device"""
        return await self._request(
            "POST",
            f"/devices/{device_id}/deactivate"
        )

    async def get_device_associations(self, device_id: str) -> Dict[str, Any]:
        """Get device associations and status"""
        device = await self.get_device_details(device_id)
        return {
            "deviceId": device_id,
            "personId": device.get("personId"),
            "locationId": device.get("locationId"),
            "status": device.get("status"),
            "provisioning": device.get("provisioning"),
            "features": device.get("features", {}),
        }

    async def list_user_devices(self, person_id: str) -> List[Dict[str, Any]]:
        """List all devices associated with a user"""
        return await self.list_devices(person_id=person_id)

    # ========== Location CRUD Operations ==========

    async def create_location(
        self,
        name: str,
        address: Dict[str, Any],
        org_id: Optional[str] = None,
        emergency_location: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Create a new location"""
        data = {
            "name": name,
            "address": address,
        }
        if org_id:
            data["orgId"] = org_id
        if emergency_location is not None:
            data["emergencyLocation"] = emergency_location

        return await self._request("POST", "/locations", json_data=data)

    async def update_location(
        self,
        location_id: str,
        name: Optional[str] = None,
        address: Optional[Dict[str, Any]] = None,
        emergency_location: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Update a location"""
        current = await self.get_location_details(location_id)
        update_data = {**current}
        
        if name:
            update_data["name"] = name
        if address:
            update_data["address"] = address
        if emergency_location is not None:
            update_data["emergencyLocation"] = emergency_location

        return await self._request("PUT", f"/locations/{location_id}", json_data=update_data)

    async def delete_location(self, location_id: str) -> Dict[str, Any]:
        """Delete a location"""
        return await self._request("DELETE", f"/locations/{location_id}")

    # ========== User CRUD Operations ==========

    async def create_user(
        self,
        emails: List[str],
        display_name: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        org_id: Optional[str] = None,
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new user"""
        data = {
            "emails": emails,
            "displayName": display_name,
        }
        if first_name:
            data["firstName"] = first_name
        if last_name:
            data["lastName"] = last_name
        if org_id:
            data["orgId"] = org_id
        if location_id:
            data["locationId"] = location_id

        return await self._request("POST", "/people", json_data=data)

    async def update_user(
        self,
        person_id: str,
        display_name: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        emails: Optional[List[str]] = None,
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update a user"""
        current = await self.get_user_details(person_id)
        update_data = {**current}
        
        if display_name:
            update_data["displayName"] = display_name
        if first_name:
            update_data["firstName"] = first_name
        if last_name:
            update_data["lastName"] = last_name
        if emails:
            update_data["emails"] = emails
        if location_id:
            update_data["locationId"] = location_id

        return await self._request("PUT", f"/people/{person_id}", json_data=update_data)

    async def delete_user(self, person_id: str) -> Dict[str, Any]:
        """Delete a user"""
        return await self._request("DELETE", f"/people/{person_id}")

    # ========== Call Queue Management ==========

    async def create_call_queue(
        self,
        name: str,
        location_id: str,
        phone_number: Optional[str] = None,
        call_policies: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a new call queue"""
        data = {
            "name": name,
            "locationId": location_id,
        }
        if phone_number:
            data["phoneNumber"] = phone_number
        if call_policies:
            data["callPolicies"] = call_policies

        return await self._request("POST", "/telephony/config/queues", json_data=data)

    async def update_call_queue(
        self,
        queue_id: str,
        name: Optional[str] = None,
        phone_number: Optional[str] = None,
        call_policies: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Update a call queue"""
        current = await self.get_call_queue_details(queue_id)
        update_data = {**current}
        
        if name:
            update_data["name"] = name
        if phone_number:
            update_data["phoneNumber"] = phone_number
        if call_policies:
            update_data["callPolicies"] = call_policies

        return await self._request("PUT", f"/telephony/config/queues/{queue_id}", json_data=update_data)

    async def delete_call_queue(self, queue_id: str) -> Dict[str, Any]:
        """Delete a call queue"""
        return await self._request("DELETE", f"/telephony/config/queues/{queue_id}")

    async def add_agent_to_queue(
        self, queue_id: str, person_id: str, skill_level: Optional[int] = None
    ) -> Dict[str, Any]:
        """Add an agent to a call queue"""
        queue = await self.get_call_queue_details(queue_id)
        agents = queue.get("agents", [])
        
        agent_data = {"personId": person_id}
        if skill_level is not None:
            agent_data["skillLevel"] = skill_level
        
        agents.append(agent_data)
        
        return await self._request(
            "PUT",
            f"/telephony/config/queues/{queue_id}",
            json_data={"agents": agents}
        )

    async def remove_agent_from_queue(
        self, queue_id: str, person_id: str
    ) -> Dict[str, Any]:
        """Remove an agent from a call queue"""
        queue = await self.get_call_queue_details(queue_id)
        agents = [
            agent for agent in queue.get("agents", [])
            if agent.get("personId") != person_id
        ]
        
        return await self._request(
            "PUT",
            f"/telephony/config/queues/{queue_id}",
            json_data={"agents": agents}
        )

    async def list_queue_agents(self, queue_id: str) -> List[Dict[str, Any]]:
        """List all agents in a call queue"""
        queue = await self.get_call_queue_details(queue_id)
        return queue.get("agents", [])

    # ========== Auto Attendant CRUD Operations ==========

    async def create_auto_attendant(
        self,
        name: str,
        location_id: str,
        phone_number: Optional[str] = None,
        business_schedule: Optional[Dict[str, Any]] = None,
        menu: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a new auto attendant"""
        data = {
            "name": name,
            "locationId": location_id,
        }
        if phone_number:
            data["phoneNumber"] = phone_number
        if business_schedule:
            data["businessSchedule"] = business_schedule
        if menu:
            data["menu"] = menu

        return await self._request("POST", "/telephony/config/autoAttendants", json_data=data)

    async def update_auto_attendant(
        self,
        auto_attendant_id: str,
        name: Optional[str] = None,
        phone_number: Optional[str] = None,
        business_schedule: Optional[Dict[str, Any]] = None,
        menu: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Update an auto attendant"""
        current = await self.get_auto_attendant_details(auto_attendant_id)
        update_data = {**current}
        
        if name:
            update_data["name"] = name
        if phone_number:
            update_data["phoneNumber"] = phone_number
        if business_schedule:
            update_data["businessSchedule"] = business_schedule
        if menu:
            update_data["menu"] = menu

        return await self._request(
            "PUT",
            f"/telephony/config/autoAttendants/{auto_attendant_id}",
            json_data=update_data
        )

    async def delete_auto_attendant(self, auto_attendant_id: str) -> Dict[str, Any]:
        """Delete an auto attendant"""
        return await self._request(
            "DELETE", f"/telephony/config/autoAttendants/{auto_attendant_id}"
        )

    # ========== Hunt Group CRUD Operations ==========

    async def create_hunt_group(
        self,
        name: str,
        location_id: str,
        phone_number: Optional[str] = None,
        distribution: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new hunt group"""
        data = {
            "name": name,
            "locationId": location_id,
        }
        if phone_number:
            data["phoneNumber"] = phone_number
        if distribution:
            data["distribution"] = distribution

        return await self._request("POST", "/telephony/config/huntGroups", json_data=data)

    async def update_hunt_group(
        self,
        hunt_group_id: str,
        name: Optional[str] = None,
        phone_number: Optional[str] = None,
        distribution: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update a hunt group"""
        current = await self.get_hunt_group_details(hunt_group_id)
        update_data = {**current}
        
        if name:
            update_data["name"] = name
        if phone_number:
            update_data["phoneNumber"] = phone_number
        if distribution:
            update_data["distribution"] = distribution

        return await self._request(
            "PUT", f"/telephony/config/huntGroups/{hunt_group_id}", json_data=update_data
        )

    async def delete_hunt_group(self, hunt_group_id: str) -> Dict[str, Any]:
        """Delete a hunt group"""
        return await self._request("DELETE", f"/telephony/config/huntGroups/{hunt_group_id}")

    async def add_member_to_hunt_group(
        self, hunt_group_id: str, person_id: str
    ) -> Dict[str, Any]:
        """Add a member to a hunt group"""
        group = await self.get_hunt_group_details(hunt_group_id)
        members = group.get("members", [])
        
        if person_id not in members:
            members.append(person_id)
        
        return await self._request(
            "PUT",
            f"/telephony/config/huntGroups/{hunt_group_id}",
            json_data={"members": members}
        )

    async def remove_member_from_hunt_group(
        self, hunt_group_id: str, person_id: str
    ) -> Dict[str, Any]:
        """Remove a member from a hunt group"""
        group = await self.get_hunt_group_details(hunt_group_id)
        members = [
            member for member in group.get("members", [])
            if member != person_id
        ]
        
        return await self._request(
            "PUT",
            f"/telephony/config/huntGroups/{hunt_group_id}",
            json_data={"members": members}
        )

    # ========== Enhanced Phone Number Management ==========

    async def unassign_phone_number(self, number_id: str) -> Dict[str, Any]:
        """Unassign a phone number from a user"""
        number = await self.get_phone_number_details(number_id)
        update_data = {**number}
        update_data["owner"] = None
        
        return await self._request(
            "PUT", f"/telephony/config/numbers/{number_id}", json_data=update_data
        )

    async def assign_phone_number_to_location(
        self, number_id: str, location_id: str
    ) -> Dict[str, Any]:
        """Assign a phone number to a location"""
        number = await self.get_phone_number_details(number_id)
        update_data = {**number}
        update_data["locationId"] = location_id
        
        return await self._request(
            "PUT", f"/telephony/config/numbers/{number_id}", json_data=update_data
        )

    async def search_available_phone_numbers(
        self,
        location_id: str,
        area_code: Optional[str] = None,
        state: Optional[str] = None,
        country: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Search for available phone numbers"""
        params = {"locationId": location_id}
        if area_code:
            params["areaCode"] = area_code
        if state:
            params["state"] = state
        if country:
            params["country"] = country

        response = await self._request("GET", "/telephony/config/availableNumbers", params=params)
        return response.get("items", [])

    # ========== Voicemail Management ==========

    async def get_user_voicemail_settings(self, person_id: str) -> Dict[str, Any]:
        """Get voicemail settings for a user"""
        settings = await self.get_user_calling_settings(person_id)
        return settings.get("voicemail", {})

    async def update_user_voicemail_settings(
        self,
        person_id: str,
        enabled: Optional[bool] = None,
        greeting: Optional[Dict[str, Any]] = None,
        pin: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update voicemail settings for a user"""
        current = await self.get_user_calling_settings(person_id)
        update_data = {**current}
        
        if "voicemail" not in update_data:
            update_data["voicemail"] = {}
        
        if enabled is not None:
            update_data["voicemail"]["enabled"] = enabled
        if greeting:
            update_data["voicemail"]["greeting"] = greeting
        if pin:
            update_data["voicemail"]["pin"] = pin

        return await self._request(
            "PUT", f"/telephony/config/people/{person_id}", json_data=update_data
        )

    async def list_voicemail_messages(
        self,
        person_id: str,
        max_results: int = 100,
    ) -> List[Dict[str, Any]]:
        """List voicemail messages for a user"""
        params = {"max": max_results}
        response = await self._request(
            "GET", f"/telephony/voicemail/messages", params=params
        )
        return response.get("items", [])

    async def get_voicemail_message(self, message_id: str) -> Dict[str, Any]:
        """Get a specific voicemail message"""
        return await self._request("GET", f"/telephony/voicemail/messages/{message_id}")

    async def delete_voicemail_message(self, message_id: str) -> Dict[str, Any]:
        """Delete a voicemail message"""
        return await self._request("DELETE", f"/telephony/voicemail/messages/{message_id}")

    # ========== Call Recording Management ==========

    async def list_call_recordings(
        self,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        person_id: Optional[str] = None,
        max_results: int = 100,
    ) -> List[Dict[str, Any]]:
        """List call recordings"""
        params = {"max": max_results}
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        if person_id:
            params["personId"] = person_id

        response = await self._request("GET", "/telephony/calls/recordings", params=params)
        return response.get("items", [])

    async def get_call_recording(self, recording_id: str) -> Dict[str, Any]:
        """Get details about a call recording"""
        return await self._request("GET", f"/telephony/calls/recordings/{recording_id}")

    async def download_call_recording(self, recording_id: str) -> bytes:
        """Download a call recording"""
        url = f"{self.base_url}/telephony/calls/recordings/{recording_id}/download"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, timeout=60.0)
            response.raise_for_status()
            return response.content

    # ========== Enhanced Reporting & Analytics ==========

    async def export_call_records(
        self,
        start_time: str,
        end_time: str,
        format: str = "csv",
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Export call records in various formats"""
        data = {
            "startTime": start_time,
            "endTime": end_time,
            "format": format,
        }
        if location_id:
            data["locationId"] = location_id

        return await self._request("POST", "/telephony/calls/export", json_data=data)

    async def get_real_time_call_metrics(
        self, location_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get real-time call metrics"""
        params = {}
        if location_id:
            params["locationId"] = location_id

        response = await self._request("GET", "/telephony/calls/metrics", params=params)
        return response.get("metrics", {})

    async def get_pstn_minutes(
        self,
        person_id: Optional[str] = None,
        location_id: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get PSTN (Public Switched Telephone Network) minutes for a person or location
        
        Calculates total PSTN minutes from call detail records by filtering for external calls.
        """
        # Get call detail records
        call_records = await self.get_call_detail_records(
            person_id=person_id,
            location_id=location_id,
            start_time=start_time,
            end_time=end_time,
            max_results=1000
        )
        
        # Filter for PSTN calls (external calls, not internal)
        # Based on actual API response structure with field names like "Call type", "Direction", etc.
        pstn_calls = []
        total_minutes = 0
        total_seconds = 0
        
        for call in call_records:
            # Use actual field names from API response
            call_duration = call.get("Duration", 0) or call.get("duration", 0)  # in seconds
            call_type = call.get("Call type", "") or call.get("callType", "") or ""
            direction = call.get("Direction", "") or call.get("direction", "") or ""
            calling_line_id = call.get("Calling line ID", "") or call.get("callingLineId", "") or ""
            called_line_id = call.get("Called line ID", "") or call.get("calledLineId", "") or ""
            
            # PSTN calls are typically:
            # - Call type is PSTN or has PSTN indicators
            # - Not SIP_ENTERPRISE (internal calls)
            # - Has duration > 0 (completed calls)
            # - May have external/international indicators
            is_pstn = False
            
            # Check call type - PSTN calls typically have PSTN in the type
            call_type_lower = call_type.upper()
            if "PSTN" in call_type_lower:
                is_pstn = True
            elif "SIP_ENTERPRISE" in call_type_lower or "ENTERPRISE" in call_type_lower:
                # Internal enterprise calls are not PSTN
                is_pstn = False
            elif "TRUNK" in call_type_lower:
                # Trunk calls are typically PSTN
                is_pstn = True
            
            # Also check if calling/called line IDs indicate external numbers
            # (e.g., not internal extensions, may have country codes, etc.)
            if not is_pstn and calling_line_id and called_line_id:
                # If line IDs are not "NA" and don't look like internal extensions, might be PSTN
                if calling_line_id != "NA" and called_line_id != "NA":
                    # Check if they look like phone numbers (have + or country codes)
                    if "+" in calling_line_id or "+" in called_line_id:
                        is_pstn = True
            
            # Only count completed calls with duration > 0
            if is_pstn and call_duration > 0:
                pstn_calls.append(call)
                total_seconds += call_duration
        
        # Convert seconds to minutes
        total_minutes = total_seconds / 60.0
        
        return {
            "personId": person_id,
            "locationId": location_id,
            "startTime": start_time,
            "endTime": end_time,
            "totalPSTNMinutes": round(total_minutes, 2),
            "totalPSTNSeconds": total_seconds,
            "totalPSTNCalls": len(pstn_calls),
            "calls": pstn_calls[:100]  # Return first 100 for details
        }

    async def get_call_statistics(
        self,
        start_time: str,
        end_time: str,
        location_id: Optional[str] = None,
        group_by: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get detailed call statistics with grouping"""
        params = {
            "startTime": start_time,
            "endTime": end_time,
        }
        if location_id:
            params["locationId"] = location_id
        if group_by:
            params["groupBy"] = group_by

        try:
            response = await self._request("GET", "/telephony/calls/statistics", params=params)
            return response.get("statistics", {})
        except Exception:
            # Fallback: calculate from call detail records
            call_records = await self.get_call_detail_records(
                start_time=start_time,
                end_time=end_time,
                location_id=location_id,
                max_results=1000
            )
            return {
                "totalCalls": len(call_records),
                "calls": call_records[:100]
            }

    async def get_user_call_statistics(
        self,
        person_id: str,
        start_time: str,
        end_time: str,
    ) -> Dict[str, Any]:
        """Get call statistics for a specific user"""
        return await self.get_call_statistics(
            start_time=start_time,
            end_time=end_time,
            group_by="user",
        )

    # ========== Webhook & Event Management ==========

    async def list_webhooks(
        self, max_results: int = 100
    ) -> List[Dict[str, Any]]:
        """List all webhooks"""
        params = {"max": max_results}
        response = await self._request("GET", "/webhooks", params=params)
        return response.get("items", [])

    async def create_webhook(
        self,
        name: str,
        target_url: str,
        resource: str,
        event: str,
        secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a webhook"""
        data = {
            "name": name,
            "targetUrl": target_url,
            "resource": resource,
            "event": event,
        }
        if secret:
            data["secret"] = secret

        return await self._request("POST", "/webhooks", json_data=data)

    async def get_webhook_details(self, webhook_id: str) -> Dict[str, Any]:
        """Get webhook details"""
        return await self._request("GET", f"/webhooks/{webhook_id}")

    async def update_webhook(
        self,
        webhook_id: str,
        name: Optional[str] = None,
        target_url: Optional[str] = None,
        secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update a webhook"""
        current = await self.get_webhook_details(webhook_id)
        update_data = {**current}
        
        if name:
            update_data["name"] = name
        if target_url:
            update_data["targetUrl"] = target_url
        if secret:
            update_data["secret"] = secret

        return await self._request("PUT", f"/webhooks/{webhook_id}", json_data=update_data)

    async def delete_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """Delete a webhook"""
        return await self._request("DELETE", f"/webhooks/{webhook_id}")

    # ========== Advanced Features ==========

    async def get_call_forwarding_settings(self, person_id: str) -> Dict[str, Any]:
        """Get call forwarding settings for a user"""
        settings = await self.get_user_calling_settings(person_id)
        return settings.get("callForwarding", {})

    async def update_call_forwarding_settings(
        self,
        person_id: str,
        always: Optional[bool] = None,
        busy: Optional[bool] = None,
        no_answer: Optional[bool] = None,
        destination: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update call forwarding settings"""
        current = await self.get_user_calling_settings(person_id)
        update_data = {**current}
        
        if "callForwarding" not in update_data:
            update_data["callForwarding"] = {}
        
        if always is not None:
            update_data["callForwarding"]["always"] = always
        if busy is not None:
            update_data["callForwarding"]["busy"] = busy
        if no_answer is not None:
            update_data["callForwarding"]["noAnswer"] = no_answer
        if destination:
            update_data["callForwarding"]["destination"] = destination

        return await self._request(
            "PUT", f"/telephony/config/people/{person_id}", json_data=update_data
        )

    async def get_call_park_settings(self, person_id: str) -> Dict[str, Any]:
        """Get call park settings for a user"""
        settings = await self.get_user_calling_settings(person_id)
        return settings.get("callPark", {})

    async def get_simultaneous_ring_settings(self, person_id: str) -> Dict[str, Any]:
        """Get simultaneous ring settings for a user"""
        settings = await self.get_user_calling_settings(person_id)
        return settings.get("simultaneousRing", {})

    async def update_simultaneous_ring_settings(
        self,
        person_id: str,
        enabled: Optional[bool] = None,
        phone_numbers: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Update simultaneous ring settings"""
        current = await self.get_user_calling_settings(person_id)
        update_data = {**current}
        
        if "simultaneousRing" not in update_data:
            update_data["simultaneousRing"] = {}
        
        if enabled is not None:
            update_data["simultaneousRing"]["enabled"] = enabled
        if phone_numbers:
            update_data["simultaneousRing"]["phoneNumbers"] = phone_numbers

        return await self._request(
            "PUT", f"/telephony/config/people/{person_id}", json_data=update_data
        )

