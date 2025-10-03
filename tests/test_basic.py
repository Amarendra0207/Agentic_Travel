#!/usr/bin/env python3
# pylint: disable=invalid-name
"""
Simple test script for distance calculation functionality
"""

import os
import sys

import requests

# Add parent directory to path for local imports
# pylint: disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# pylint: disable=import-error,wrong-import-position
from utils.airport_distance_calculator import AirportDistanceCalculator


def get_map_key():
    """Get MAP_KEY with fallback for testing environments."""
    try:
        import streamlit as st  # pylint: disable=import-outside-toplevel

        return str(st.secrets["map"]["api_key"])
    except ImportError:
        # Streamlit not available
        return None
    except (KeyError, AttributeError):
        # Secrets structure issues
        return None
    except Exception:  # pylint: disable=broad-except
        # Catch StreamlitSecretNotFoundError and other Streamlit exceptions
        return None


def test_basic_functionality():
    """Test basic functionality without API calls"""

    print("🧪 Testing Basic Distance Calculation Features")
    print("=" * 50)

    # Get API key with fallback
    map_key = get_map_key()

    # Initialize calculator
    calc = AirportDistanceCalculator(api_key=map_key)

    # Test 1: Airport coordinates lookup (no API call needed)
    print("\n1️⃣ Testing Airport Coordinates Lookup:")
    coords = calc.get_airport_coordinates("DEL")
    print(f"📍 DEL (Delhi) Airport coordinates: {coords}")

    coords = calc.get_airport_coordinates("JFK")
    print(f"📍 JFK (New York) Airport coordinates: {coords}")

    coords = calc.get_airport_coordinates("LHR")
    print(f"📍 LHR (London) Airport coordinates: {coords}")

    # Test 2: Check MAP_KEY
    print("\n2️⃣ MAP_KEY Status:")

    if map_key:
        print(f"✅ MAP_KEY found: {map_key[:10]}...{map_key[-10:]}")
    else:
        print("❌ MAP_KEY not found in secrets")

    # Test 3: Test one simple geocoding call (only if API key is available)
    print("\n3️⃣ Testing Simple Geocoding (with timeout):")
    if not map_key:
        print("⚠️ Skipping API test - no API key available")
    else:
        try:
            url = "https://api.openrouteservice.org/geocode/search"
            headers = {"Authorization": map_key}
            params = {"text": "New York", "size": 1}

            response = requests.get(url, headers=headers, params=params, timeout=10)
            print(f"📡 API Response Status: {response.status_code}")
            if response.status_code == 200:
                print("✅ OpenRouteService API is working")
            else:
                print(f"❌ API Error: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"❌ API Connection Error: {e}")
        except (KeyError, ValueError) as e:
            print(f"❌ Configuration Error: {e}")

    print("\n✅ Basic test completed!")


if __name__ == "__main__":
    test_basic_functionality()
