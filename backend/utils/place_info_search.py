"""Place information search utility module.

This module provides a TavilyPlaceSearchTool class for searching place information
using the Tavily search engine, including attractions, restaurants, activities,
and transportation options.
"""

from typing import Dict, Any, Union

from langchain_tavily import TavilySearch


class TavilyPlaceSearchTool:
    """Tool for searching place information using Tavily search engine."""

    def __init__(self, tavily_api_key: str):
        if not tavily_api_key:
            raise ValueError("Tavily API key not provided.")
        self.tavily_api_key = tavily_api_key

    def tavily_search_attractions(self, place: str) -> Union[str, Dict[str, Any]]:
        """
        Searches for attractions in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(
            api_key=self.tavily_api_key, topic="general", include_answer="advanced"
        )
        result = tavily_tool.invoke(
            {"query": f"top attractive places in and around {place}"}
        )
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result

    def tavily_search_restaurants(self, place: str) -> Union[str, Dict[str, Any]]:
        """
        Searches for available restaurants in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(
            api_key=self.tavily_api_key, topic="general", include_answer="advanced"
        )
        result = tavily_tool.invoke(
            {
                "query": f"what are the top 10 restaurants and eateries in and around {place}."
            }
        )
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result

    def tavily_search_activity(self, place: str) -> Union[str, Dict[str, Any]]:
        """
        Searches for popular activities in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(
            api_key=self.tavily_api_key, topic="general", include_answer="advanced"
        )
        result = tavily_tool.invoke({"query": f"activities in and around {place}"})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result

    def tavily_search_transportation(self, place: str) -> Union[str, Dict[str, Any]]:
        """
        Searches for available modes of transportation in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(
            api_key=self.tavily_api_key, topic="general", include_answer="advanced"
        )
        result = tavily_tool.invoke(
            {
                "query": f"What are the different modes of transportations available in {place}"
            }
        )
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result
