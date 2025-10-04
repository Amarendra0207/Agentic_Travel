#!/usr/bin/env python3
# pylint: disable=invalid-name
"""
Fast offline test script for distance calculation functionality
"""

import os
import sys
import math

# Add parent directory to path for local imports
# pylint: disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def calculate_haversine_distance(coord1, coord2):
    """Calculate straight-line distance using Haversine formula"""
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # Convert to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))

    # Earth's radius in kilometers
    r = 6371

    distance = r * c
    return round(distance, 2)


# Test data constants
AIRPORTS = {
    "JFK": (40.6413, -73.7781),  # John F Kennedy International
    "LAX": (33.9425, -118.4081),  # Los Angeles International
    "LHR": (51.4700, -0.4543),  # London Heathrow
    "DEL": (28.5665, 77.1031),  # Indira Gandhi International
    "DXB": (25.2532, 55.3657),  # Dubai International
    "CDG": (49.0097, 2.5479),  # Charles de Gaulle
}

CITIES = {
    "New York": (40.7128, -74.0060),
    "London": (51.5074, -0.1278),
    "Paris": (48.8566, 2.3522),
    "Dubai": (25.2048, 55.2708),
    "Delhi": (28.7041, 77.1025),
    "Los Angeles": (34.0522, -118.2437),
}


def _test_airport_coordinates():
    """Test airport coordinates display"""
    print("\n1️⃣ Testing Airport Coordinates (Offline Data):")
    for code, coords in AIRPORTS.items():
        print(f"📍 {code}: {coords}")


def _test_airport_city_distances():
    """Test airport to city distances"""
    print("\n2️⃣ Testing Airport to City Distances:")
    test_pairs = [
        ("JFK", "New York"), ("LAX", "Los Angeles"), ("LHR", "London"),
        ("DEL", "Delhi"), ("DXB", "Dubai"), ("CDG", "Paris"),
    ]

    for airport_code, city_name in test_pairs:
        distance = calculate_haversine_distance(AIRPORTS[airport_code], CITIES[city_name])
        # Estimate driving time (assuming 50 km/h average in city)
        hours, minutes = divmod(int((distance / 50) * 60), 60)
        print(f"✈️ {airport_code} to {city_name}: {distance} km (~{hours}h {minutes}m)")


def _test_long_distances():
    """Test long distance calculations"""
    print("\n3️⃣ Testing Long Distance Calculations:")
    long_pairs = [
        ("JFK", "LHR", "New York to London"),
        ("LAX", "DXB", "Los Angeles to Dubai"),
        ("DEL", "CDG", "Delhi to Paris"),
    ]

    for airport1, airport2, description in long_pairs:
        distance = calculate_haversine_distance(AIRPORTS[airport1], AIRPORTS[airport2])
        print(f"🌍 {description}: {distance} km")


def _test_distance_accuracy():
    """Test distance calculation accuracy"""
    print("\n4️⃣ Testing Distance Calculation Accuracy:")
    calculated = calculate_haversine_distance(AIRPORTS["JFK"], AIRPORTS["LAX"])
    expected = 3944  # Known approximate distance
    error = abs(calculated - expected) / expected * 100

    print(f"🔍 JFK to LAX calculated: {calculated} km")
    print(f"🔍 Expected distance: {expected} km")
    print(f"🔍 Accuracy: {100 - error:.1f}% (error: {error:.1f}%)")


def test_offline_distance_calculations():
    """Test distance calculations without any API calls - runs instantly"""
    print("⚡ Fast Offline Distance Calculator Test")
    print("=" * 50)

    _test_airport_coordinates()
    _test_airport_city_distances()
    _test_long_distances()
    _test_distance_accuracy()

    print("\n✅ All offline tests completed in milliseconds!")
    print("💡 For real API testing, run the full test suite.")


if __name__ == "__main__":
    test_offline_distance_calculations()
