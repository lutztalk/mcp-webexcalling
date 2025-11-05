#!/usr/bin/env python3
"""
Diagnostic script to discover the correct Webex Calling API endpoint for detailed call history
"""

import asyncio
import os
import sys
from datetime import datetime, timedelta
from mcp_webexcalling.webex_client import WebexClient
import httpx

async def test_endpoint_discovery():
    """Test various endpoint structures to find the correct one"""
    
    access_token = os.getenv("WEBEX_ACCESS_TOKEN")
    if not access_token:
        print("❌ ERROR: WEBEX_ACCESS_TOKEN environment variable not set")
        return False
    
    client = WebexClient(access_token=access_token)
    
    # Get organization and location info
    print("🔍 Gathering organization information...")
    try:
        org_info = await client.get_organization_info()
        org_id = None
        if org_info and "items" in org_info and org_info["items"]:
            org_id = org_info["items"][0].get("id")
            print(f"   ✓ Organization ID: {org_id}")
        
        locations = await client.list_locations(max_results=1)
        location_id = None
        if locations:
            location_id = locations[0].get("id")
            print(f"   ✓ Location ID: {location_id}")
    except Exception as e:
        print(f"   ⚠️  Could not get org/location info: {e}")
        org_id = None
        location_id = None
    
    # Calculate date range (last 7 days)
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=7)
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    
    print(f"\n📅 Testing Endpoints (Last 7 days)")
    print(f"   Start: {start_time_str}")
    print(f"   End: {end_time_str}")
    print()
    
    # Build comprehensive list of endpoints to try
    endpoints_to_test = []
    
    # Location-scoped endpoints
    if location_id:
        endpoints_to_test.extend([
            f"/telephony/config/locations/{location_id}/calls/reports/detailedCallHistory",
            f"/telephony/config/locations/{location_id}/reports/detailedCallHistory",
            f"/telephony/config/locations/{location_id}/calls/detailedCallHistory",
            f"/locations/{location_id}/telephony/calls/reports/detailedCallHistory",
            f"/telephony/config/locations/{location_id}/callHistory",
        ])
    
    # Org-scoped endpoints
    if org_id:
        endpoints_to_test.extend([
            f"/organizations/{org_id}/telephony/calls/reports/detailedCallHistory",
            f"/organizations/{org_id}/telephony/reports/detailedCallHistory",
            f"/telephony/config/organizations/{org_id}/calls/reports/detailedCallHistory",
        ])
    
    # Standard endpoints
    endpoints_to_test.extend([
        "/telephony/calls/reports/detailedCallHistory",
        "/telephony/reports/detailedCallHistory",
        "/telephony/calls/detailedCallHistory",
        "/calls/reports/detailedCallHistory",
        "/telephony/config/calls/reports/detailedCallHistory",
        "/telephony/analytics/calls/detailedCallHistory",
        "/telephony/calls/callHistory",
        "/telephony/callHistory",
    ])
    
    # Test with minimal parameters first
    params_minimal = {
        "startTime": start_time_str,
        "endTime": end_time_str,
    }
    
    print(f"🧪 Testing {len(endpoints_to_test)} endpoint variations...")
    print()
    
    success_count = 0
    for i, endpoint in enumerate(endpoints_to_test, 1):
        try:
            url = f"{client.base_url}{endpoint}"
            print(f"[{i}/{len(endpoints_to_test)}] Testing: {endpoint}")
            
            async with httpx.AsyncClient() as http_client:
                response = await http_client.get(
                    url,
                    headers=client.headers,
                    params=params_minimal,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    print(f"   ✅ SUCCESS! Status: {response.status_code}")
                    try:
                        data = response.json()
                        if isinstance(data, list):
                            print(f"   📊 Returned {len(data)} items")
                        elif "items" in data:
                            print(f"   📊 Returned {len(data.get('items', []))} items")
                        else:
                            print(f"   📊 Response structure: {list(data.keys()) if isinstance(data, dict) else type(data)}")
                        print(f"   ✅ WORKING ENDPOINT: {endpoint}")
                        success_count += 1
                        break
                    except:
                        print(f"   📊 Response: {response.text[:200]}")
                elif response.status_code == 400:
                    print(f"   ⚠️  Status 400 (Bad Request) - endpoint exists but parameters may be wrong")
                    try:
                        error_data = response.json()
                        print(f"   Error: {error_data}")
                    except:
                        print(f"   Error: {response.text[:200]}")
                elif response.status_code == 403:
                    print(f"   ⚠️  Status 403 (Forbidden) - endpoint exists but permission denied")
                elif response.status_code == 404:
                    print(f"   ❌ Status 404 (Not Found)")
                else:
                    print(f"   ⚠️  Status {response.status_code}")
                    print(f"   Response: {response.text[:200]}")
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:100]}")
        
        print()
    
    print("=" * 60)
    if success_count > 0:
        print(f"✅ Found {success_count} working endpoint(s)")
    else:
        print("❌ No working endpoints found")
        print("\n💡 Next steps:")
        print("   1. Check the Webex Calling API documentation for the exact endpoint")
        print("   2. Verify your organization has Webex Calling enabled")
        print("   3. Ensure you have the 'Webex Calling Detailed Call History API access' role")
        print("   4. Check if your organization uses a different base URL")
    print("=" * 60)
    
    return success_count > 0

async def main():
    print("=" * 60)
    print("Webex Calling API - Endpoint Discovery")
    print("=" * 60)
    print()
    
    success = await test_endpoint_discovery()
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

