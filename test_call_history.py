#!/usr/bin/env python3
"""
Test script for Webex Calling API - Call Detail Records
Copy and paste this into your terminal to test the call history endpoint
"""

import asyncio
import os
import sys
from datetime import datetime, timedelta
from mcp_webexcalling.webex_client import WebexClient

async def test_call_detail_records():
    """Test the call detail records endpoint"""
    
    # Get access token from environment
    access_token = os.getenv("WEBEX_ACCESS_TOKEN")
    if not access_token:
        print("❌ ERROR: WEBEX_ACCESS_TOKEN environment variable not set")
        print("   Set it with: export WEBEX_ACCESS_TOKEN='your_token_here'")
        return False
    
    # Initialize client
    print("🔧 Initializing Webex Client...")
    client = WebexClient(access_token=access_token)
    
    # Calculate date range
    # IMPORTANT: API requires dates to be between 5 minutes ago and 48 hours ago
    from datetime import timezone
    now = datetime.now(timezone.utc)
    
    # Use a range within the last 24 hours (well within the 48 hour limit)
    # End time: 1 hour ago (more than 5 minutes)
    end_time = now - timedelta(hours=1)
    # Start time: 24 hours ago (within 48 hour limit)
    start_time = now - timedelta(hours=24)
    
    # Format as ISO 8601 with milliseconds (API requires this format)
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    
    print(f"\n📅 Testing Call Detail Records API")
    print(f"   ⚠️  Note: API requires dates between 5 minutes and 48 hours ago")
    print(f"   Start Time: {start_time_str} (24 hours ago)")
    print(f"   End Time: {end_time_str} (1 hour ago)")
    print(f"   Base URL: https://analytics.webexapis.com/v1")
    print(f"   Endpoint: /cdr_feed")
    print(f"   Full URL: https://analytics.webexapis.com/v1/cdr_feed")
    print()
    
    try:
        # Test 1: Get call detail records
        print("🔍 Test 1: Retrieving call detail records...")
        records = await client.get_call_detail_records(
            start_time=start_time_str,
            end_time=end_time_str,
            max_results=10
        )
        
        print(f"✅ SUCCESS! Retrieved {len(records)} call records")
        
        if records:
            print(f"\n📊 Sample Call Record:")
            sample = records[0]
            
            # Debug: Print the actual structure to see what fields are available
            print(f"   📋 Record structure (first 3 keys): {list(sample.keys())[:10]}")
            print()
            
            # Use the actual field names from the API response
            call_id = sample.get('Call ID') or sample.get('id') or sample.get('callId')
            direction = sample.get('Direction') or sample.get('direction')
            duration = sample.get('Duration') or sample.get('duration')
            start_time = sample.get('Start time') or sample.get('startTime')
            answered = sample.get('Answered') or sample.get('answered')
            call_type = sample.get('Call type') or sample.get('callType')
            calling_line_id = sample.get('Calling line ID') or sample.get('callingLineId')
            called_line_id = sample.get('Called line ID') or sample.get('calledLineId')
            
            # Handle 'from' and 'to' - could be objects or strings
            from_info = sample.get('from') or sample.get('fromNumber') or sample.get('caller')
            to_info = sample.get('to') or sample.get('toNumber') or sample.get('called')
            
            if isinstance(from_info, dict):
                from_number = from_info.get('phoneNumber') or from_info.get('number') or from_info.get('phone') or from_info.get('address')
            elif isinstance(from_info, str):
                from_number = from_info
            else:
                from_number = None
            
            if isinstance(to_info, dict):
                to_number = to_info.get('phoneNumber') or to_info.get('number') or to_info.get('phone') or to_info.get('address')
            elif isinstance(to_info, str):
                to_number = to_info
            else:
                to_number = None
            
            status = sample.get('status') or sample.get('callStatus') or sample.get('call_status') or sample.get('result')
            
            print(f"   Call ID: {call_id or 'N/A'}")
            print(f"   Direction: {direction or 'N/A'}")
            print(f"   Duration: {duration or 'N/A'} seconds")
            print(f"   Start Time: {start_time or 'N/A'}")
            print(f"   From: {from_number or 'N/A'}")
            print(f"   To: {to_number or 'N/A'}")
            print(f"   Status: {status or 'N/A'}")
            
            # Print full record for debugging (first 500 chars)
            print(f"\n   🔍 Full record (sample):")
            import json
            print(f"   {json.dumps(sample, indent=2, default=str)[:500]}...")
        else:
            print("   ⚠️  No call records found in the specified time range")
        
        # Test 2: Get PSTN minutes
        print(f"\n🔍 Test 2: Calculating PSTN minutes...")
        pstn_data = await client.get_pstn_minutes(
            start_time=start_time_str,
            end_time=end_time_str
        )
        
        print(f"✅ PSTN Calculation Complete!")
        print(f"   Total PSTN Minutes: {pstn_data.get('totalPSTNMinutes', 0)}")
        print(f"   Total PSTN Calls: {pstn_data.get('totalPSTNCalls', 0)}")
        print(f"   Total PSTN Seconds: {pstn_data.get('totalPSTNSeconds', 0)}")
        
        return True
        
    except ValueError as e:
        print(f"❌ VALIDATION ERROR: {str(e)}")
        return False
    except Exception as e:
        error_msg = str(e)
        print(f"❌ ERROR: {error_msg}")
        
        # Provide helpful troubleshooting
        if "403" in error_msg or "Forbidden" in error_msg:
            print("\n💡 TROUBLESHOOTING:")
            print("   1. You need the 'Webex Calling Detailed Call History API access' role")
            print("   2. This role must be assigned by another administrator")
            print("   3. Contact your Webex administrator to assign this role")
            print("   4. Once assigned, wait a few minutes and try again")
        elif "401" in error_msg or "Unauthorized" in error_msg:
            print("\n💡 TROUBLESHOOTING:")
            print("   1. Check that your WEBEX_ACCESS_TOKEN is valid")
            print("   2. Verify the token hasn't expired")
            print("   3. Ensure the token has the required scopes")
        elif "404" in error_msg:
            print("\n💡 TROUBLESHOOTING:")
            print("   1. The endpoint may not be available for your organization")
            print("   2. Check if your organization has Webex Calling enabled")
            print("   3. Verify you're using the correct API base URL")
        
        return False

async def main():
    """Main test function"""
    print("=" * 60)
    print("Webex Calling API - Call Detail Records Test")
    print("=" * 60)
    print()
    
    success = await test_call_detail_records()
    
    print()
    print("=" * 60)
    if success:
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ TESTS FAILED - See error messages above")
    print("=" * 60)
    
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

