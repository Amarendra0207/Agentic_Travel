"""Expense calculator tool module.

This module provides a CalculatorTool class that creates LangChain tools
for calculating various travel-related expenses including hotel costs,
total trip expenses, and daily budget planning.
"""

from typing import List

from langchain.tools import tool

from utils.expense_calculator import Calculator


class CalculatorTool:  # pylint: disable=too-few-public-methods
    """Tool class for expense calculation operations.

    This class creates LangChain tools for various expense calculations
    including hotel costs, total expenses, and daily budget planning.

    Attributes:
        calculator (Calculator): Expense calculation service instance
        calculator_tool_list (List): List of available calculation tools
    """

    def __init__(self):
        self.calculator = Calculator()
        self.calculator_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the calculator tool"""

        @tool
        def estimate_total_hotel_cost(price_per_night: str, total_days: float) -> float:
            """Calculate total hotel cost"""
            return self.calculator.multiply(price_per_night, total_days)

        @tool
        def calculate_total_expense(*costs: float) -> float:
            """Calculate total expense of the trip"""
            return self.calculator.calculate_total(*costs)

        @tool
        def calculate_daily_expense_budget(total_cost: float, days: int) -> float:
            """Calculate daily expense"""
            return self.calculator.calculate_daily_budget(total_cost, days)

        return [
            estimate_total_hotel_cost,
            calculate_total_expense,
            calculate_daily_expense_budget,
        ]
