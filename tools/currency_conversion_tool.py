"""Currency conversion tool module.

This module provides a CurrencyConverterTool class that creates LangChain tools
for converting currencies using external currency conversion APIs.
"""

from typing import List

from langchain.tools import tool
import streamlit as st

from utils.currency_convertor import CurrencyConverter


class CurrencyConverterTool:  # pylint: disable=too-few-public-methods
    """Tool class for currency conversion operations.

    This class creates LangChain tools for currency conversion functionality,
    using an external currency conversion service.

    Attributes:
        api_key (str): API key for currency conversion service
        currency_service (CurrencyConverter): Currency conversion service instance
        currency_converter_tool_list (List): List of available currency conversion tools
    """

    def __init__(self):
        self.api_key = st.secrets["exchange_rate"]["api_key"]
        self.currency_service = CurrencyConverter(self.api_key)
        self.currency_converter_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the currency converter tool"""

        @tool
        def convert_currency(amount: float, from_currency: str, to_currency: str):
            """Convert amount from one currency to another"""
            return self.currency_service.convert(amount, from_currency, to_currency)

        return [convert_currency]
