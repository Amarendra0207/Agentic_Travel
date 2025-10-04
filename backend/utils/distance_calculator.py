"""Distance calculator utility module.

This module provides functions for calculating driving distances between coordinates
using the OpenRouteService API.
"""

from typing import Tuple, Optional

import requests


def get_driving_distance(
    api_key: str, start_coords: Tuple[float, float], end_coords: Tuple[float, float]
) -> Optional[float]:
    """
    Returns driving distance in kilometers between two (lat, lon) pairs using OpenRouteService.
    """
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {"Authorization": api_key}
    body = {
        "coordinates": [
            [start_coords[1], start_coords[0]],  # [lon, lat]
            [end_coords[1], end_coords[0]],
        ]
    }
    response = requests.post(url, json=body, headers=headers, timeout=15)
    if response.status_code == 200:
        data = response.json()
        # distance in meters
        return data["features"][0]["properties"]["segments"][0]["distance"] / 1000
    return None
