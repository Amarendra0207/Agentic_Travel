"""Car rental service utility module.

This module provides a CarRentalService class for searching car rental and transfer
offers using the Amadeus API.
"""

import requests
import streamlit as st


class CarRentalService:  # pylint: disable=too-few-public-methods
    """Car rental and transfer service using Amadeus API."""

    def __init__(self):
        # Get Amadeus configuration from Streamlit secrets
        self.amadeus_api_key = st.secrets["amadeus"]["api_key"]
        self.amadeus_api_secret = st.secrets["amadeus"]["api_secret"]
        self.base_url = st.secrets["amadeus"]["base_url"] + "/shopping/transfer-offers"
        self.token_url = st.secrets["amadeus"]["token_url"]
        self.access_token = self._get_access_token()
        print(f"Access Token: '{self.access_token}'")

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
