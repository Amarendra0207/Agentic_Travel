#!/usr/bin/env python3
"""
Test the Word export API endpoint directly.

This module provides API endpoint testing with fallback for CI environments.
"""

from typing import Dict, Any

import requests

from test_utils import get_base_url


def test_word_export_api() -> None:
    """Test the Word export API endpoint."""
    print("🧪 Testing Word Export API Endpoint")
    print("=" * 50)

    # Get base URL with fallback
    base_url = get_base_url()

    # Test content
    test_content = """
# Test Travel Report

## Destination: New York

### Day 1
- Arrive at JFK Airport
- Check into hotel in Manhattan
- Visit Times Square

### Airport Distance Information
Distance from John F Kennedy International Airport (JFK) to Times Square: 26.45 km (approximately 31m by car)

## Car Rental Options
- Vehicle: Economy Car | Seats: 4 | Provider: Hertz | Price: 89 USD
"""

    # Test payload
    payload: Dict[str, Any] = {
        "content": test_content,
        "query_info": {
            "query": "Test New York trip",
            "startCity": "New York",
            "endCity": "New York",
        },
    }

    try:
        print("📡 Sending request to /export-word endpoint...")

        response = requests.post(f"{base_url}/export-word", json=payload, timeout=30)

        print(f"   Status Code: {response.status_code}")
        print(f"   Content Type: {response.headers.get('content-type', 'N/A')}")
        print(f"   Content Length: {len(response.content)} bytes")

        if response.status_code == 200:
            # Save the file
            filename = "test_export.docx"
            with open(filename, "wb") as f:
                f.write(response.content)

            print(f"✅ Success! Word document saved as: {filename}")
            print(f"   File size: {len(response.content)} bytes")

        else:
            print(f"❌ Failed with status {response.status_code}")
            print(f"   Error: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Server is not running or not accessible")
        print(
            "   Make sure to start the server with: uvicorn main:app --reload --port 8000"
        )
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
    except (IOError, OSError) as e:
        print(f"❌ File operation error: {e}")
    except (KeyError, ValueError) as e:
        print(f"❌ Data processing error: {e}")

    print("\n✅ Test completed!")


if __name__ == "__main__":
    test_word_export_api()
