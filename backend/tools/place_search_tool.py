"""Place search tool module.

This module provides a PlaceSearchTool class that creates LangChain tools
for searching information about places including attractions, restaurants,
activities, and transportation options using Tavily search.
"""

from typing import List

from langchain.tools import tool

from utils.place_info_search import TavilyPlaceSearchTool


class PlaceSearchTool:  # pylint: disable=too-few-public-methods
    """Tool class for place search operations.

    This class creates LangChain tools for searching various information
    about places including attractions, restaurants, activities, and
    transportation options using Tavily search API.

    Attributes:
        tavily_search (TavilyPlaceSearchTool): Tavily search service instance
        place_search_tool_list (List): List of available place search tools
    """

    def __init__(self, tavily_api_key: str):
        self.tavily_search = TavilyPlaceSearchTool(tavily_api_key=tavily_api_key)
        self.place_search_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the place search tool"""

        @tool
        def search_attractions(place: str) -> str:
            """Search attractions of a place"""
            tavily_result = self.tavily_search.tavily_search_attractions(place)
            return f"Following are the attractions of {place}: {tavily_result}"

        @tool
        def search_restaurants(place: str) -> str:
            """Search restaurants of a place"""
            tavily_result = self.tavily_search.tavily_search_restaurants(place)
            return f"Following are the restaurants of {place}: {tavily_result}"

        @tool
        def search_activities(place: str) -> str:
            """Search activities of a place"""
            tavily_result = self.tavily_search.tavily_search_activity(place)
            return (
                f"Following are the activities in and around {place}: {tavily_result}"
            )

        @tool
        def search_transportation(place: str) -> str:
            """Search transportation of a place"""
            tavily_result = self.tavily_search.tavily_search_transportation(place)
            return (
                f"Following are the modes of transportation available in {place}: "
                f"{tavily_result}"
            )

        return [
            search_attractions,
            search_restaurants,
            search_activities,
            search_transportation,
        ]
