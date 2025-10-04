"""Car rental service utility module.

This module provides a CarRentalService class for searching car rental and transfer
offers using the Amadeus API.
"""

from dotenv import load_dotenv
import os
import requests

load_dotenv()  # Load environment variables from .env file


class CarRentalService:  # pylint: disable=too-few-public-methods
    """Car rental and transfer service using Amadeus API."""

    def __init__(self):
        # Get Amadeus configuration from environment variables
        self.amadeus_api_key = os.getenv("AMADEUS_API_KEY")
        self.amadeus_api_secret = os.getenv("AMADEUS_API_SECRET")
        base_url_from_env = os.getenv("AMADEUS_BASE_URL")
        self.token_url = os.getenv("AMADEUS_TOKEN_URL")

        if not all(
            [
                self.amadeus_api_key,
                self.amadeus_api_secret,
                base_url_from_env,
                self.token_url,
            ]
        ):
            raise ValueError(
                "Amadeus API credentials are not fully configured in the environment."
            )

        self.base_url = base_url_from_env + "/shopping/transfer-offers"
        self.access_token = self._get_access_token()
        print("Access Token for Amadeus:", self.access_token)

    def _get_access_token(self):
        data = {
            "grant_type": "client_credentials",
            "client_id": self.amadeus_api_key,
            "client_secret": self.amadeus_api_secret,
        }
        response = requests.post(self.token_url, data=data, timeout=10)
        if response.status_code != 200:
            raise requests.RequestException(
                f"Failed to get Amadeus access token: {response.text}"
            )
        return response.json()["access_token"]

    def search_cars(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        start_location_code: str,
        end_location_code: str,
        transfer_type: str,
        start_date_time: str,
        duration: str,
        passengers: int,
    ):
        """
        \"\"\"\n        Search for available transfer offers using Amadeus API.
        Args:
            start_location_code (str): IATA code of start location
            end_location_code (str): IATA code of the end location
            transfer_type (str): Type of transfer (e.g., HOURLY, ONE_WAY)
            start_date_time (str): Start date and time in ISO format
            duration (str): Duration in ISO 8601 format (e.g., PT9H30M)
            passengers (int): Number of passengers
        Returns:
            dict: API response with available transfer offers
        """
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        params = {
            "startLocationCode": start_location_code,
            "endLocationCode": end_location_code,
            "transferType": transfer_type,
            "startDateTime": start_date_time,
            "duration": duration,
            "passengers": passengers,
        }
        response = requests.post(
            self.base_url, headers=headers, json=params, timeout=30
        )
        print(f"Request URL: {response.url}")
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")

        if response.status_code != 200:
            raise requests.RequestException(
                f"Car rental API call failed: {response.text}"
            )
        return response.json()
