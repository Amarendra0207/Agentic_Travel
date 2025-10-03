#!/usr/bin/env python3
# pylint: disable=invalid-name
"""
Test one simple distance calculation
"""

import os
import sys

# Add parent directory to path for local imports
# pylint: disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# pylint: disable=import-error,wrong-import-position
from utils.airport_distance_calculator import AirportDistanceCalculator


def test_one_distance():
    """Test one simple distance calculation"""

    print("🧪 Testing One Distance Calculation")
    print("=" * 50)

    # Initialize calculator
    calc = AirportDistanceCalculator()

    # Test: Calculate distance from JFK to Times Square
    print("\n📍 Testing: JFK Airport to Times Square, New York")
    distance_info = calc.get_airport_to_attraction_distance(
        "JFK", "Times Square, New York"
    )

    if distance_info["success"]:
        print("✅ Success!")
        print(f"   Distance: {distance_info['distance_km']} km")
        print(f"   Travel Time: {distance_info['travel_time']}")
        print(f"   Airport: {distance_info['airport_name']}")
    else:
        print(f"❌ Failed: {distance_info['error']}")

    print("\n✅ Test completed!")


if __name__ == "__main__":
    test_one_distance()
