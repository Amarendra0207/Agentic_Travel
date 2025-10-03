"""Currency converter utility module.

This module provides a CurrencyConverter class for converting between different
currencies using the ExchangeRate-API service.
"""

import requests


class CurrencyConverter:  # pylint: disable=too-few-public-methods
    """Currency converter using ExchangeRate-API service."""

    def __init__(self, api_key: str):
        self.base_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/"

    def convert(self, amount: float, from_currency: str, to_currency: str):
        """Convert the amount from one currency to another"""
        url = f"{self.base_url}/{from_currency}"
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            raise requests.RequestException(f"API call failed: {response.json()}")
        rates = response.json()["conversion_rates"]
        if to_currency not in rates:
            raise ValueError(f"{to_currency} not found in exchange rates.")
        return amount * rates[to_currency]
