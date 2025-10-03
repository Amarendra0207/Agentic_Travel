"""Weather information utility module.

This module provides a WeatherForecastTool class for retrieving current weather
and forecast information using the OpenWeatherMap API.
"""

import requests
import streamlit as st


class WeatherForecastTool:
    """Weather forecast tool using OpenWeatherMap API."""

    def __init__(self):
        self.api_key = st.secrets["weather"]["api_key"]
        self.base_url = st.secrets["weather"]["base_url"]

    def get_current_weather(self, place: str):
        """Get current weather of a place"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": place,
                "appid": self.api_key,
            }
            response = requests.get(url, params=params, timeout=10)
            return response.json() if response.status_code == 200 else {}
        except Exception as e:
            raise e

    def get_forecast_weather(self, place: str):
        """Get weather forecast of a place"""
        try:
            url = f"{self.base_url}/forecast"
            params = {"q": place, "appid": self.api_key, "cnt": 10, "units": "metric"}
            response = requests.get(url, params=params, timeout=10)
            return response.json() if response.status_code == 200 else {}
        except Exception as e:
            raise e
