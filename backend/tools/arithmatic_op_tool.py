"""Arithmetic operations and currency conversion tools.

This module provides basic arithmetic operations and currency conversion
functionality using LangChain tools and Alpha Vantage API.
"""

import os

from langchain.tools import tool
from langchain_community.utilities.alpha_vantage import AlphaVantageAPIWrapper


@tool
def multiply(a: int, b: int) -> int:
    """
    Multiply two integers.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The product of a and b.
    """
    return a * b


@tool
def add(a: int, b: int) -> int:
    """
    Add two integers.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The sum of a and b.
    """
    return a + b


@tool
def currency_converter(from_curr: str, to_curr: str, value: float) -> float:
    """Convert currency from one type to another using Alpha Vantage API.

    Args:
        from_curr (str): Source currency code (e.g., 'USD')
        to_curr (str): Target currency code (e.g., 'EUR')
        value (float): Amount to convert

    Returns:
        float: Converted currency value
    """
    os.environ["ALPHAVANTAGE_API_KEY"] = os.getenv("ALPHAVANTAGE_API_KEY")
    alpha_vantage = AlphaVantageAPIWrapper()
    # Note: Using private method as it's the available API in langchain_community
    # pylint: disable=protected-access
    response = alpha_vantage._get_exchange_rate(from_curr, to_curr)
    exchange_rate = response["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
    return value * float(exchange_rate)
