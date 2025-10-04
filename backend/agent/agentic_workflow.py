"""Agentic workflow module for building and managing travel planning agents.

This module provides classes for creating LangGraph-based agents that can handle
travel planning queries using various tools and LLM providers.
"""

from dataclasses import dataclass
from typing import List, Optional

from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition

from utils.model_loaders import ModelLoader
from prompt_library.prompt import get_budget_aware_system_prompt

from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConverterTool
from tools.distance_calculator_tool import DistanceCalculatorTool


@dataclass(frozen=True)
class GraphBuilderConfig:
    """Configuration class for GraphBuilder.

    Attributes:
        model_provider: The LLM provider to use ("groq")
        budget_preference: Travel budget preference ("cheapest", "budget_friendly", "luxurious")
    """

    model_provider: str = "groq"
    budget_preference: str = "budget_friendly"


class GraphBuilder:  # pylint: disable=too-many-instance-attributes
    """
    Builds a StateGraph that delegates user messages to an LLM and
    invokes external tools when required.

    Designed for readability and reusability: configuration is encapsulated
    in GraphBuilderConfig and tool initialization is separated into methods.
    """

    def __init__(
        self,
        tavily_api_key: str,
        exchange_rate_api_key: str,
        weather_api_key: str,
        weather_base_url: str,
        openroute_api_key: str,
        model_provider: str = "groq",
        budget_preference: str = "budget_friendly",
    ):
        self.config = GraphBuilderConfig(
            model_provider=model_provider, budget_preference=budget_preference
        )
        self.tavily_api_key = tavily_api_key
        self.exchange_rate_api_key = exchange_rate_api_key
        self.weather_api_key = weather_api_key
        self.weather_base_url = weather_base_url
        self.openroute_api_key = openroute_api_key

        self._model_loader: Optional[ModelLoader] = None
        self._llm = None
        self._llm_with_tools = None

        # system prompt for the agent
        self.system_prompt = get_budget_aware_system_prompt(
            self.config.budget_preference
        )

        # tool instances and flattened tool list
        self._init_tool_instances()
        self.tools = self._collect_tools()

        # compiled graph cache
        self.graph = None

    # ---- Model / LLM helpers ----
    @property
    def model_loader(self) -> ModelLoader:
        """Lazy-loaded ModelLoader instance for managing LLM configuration."""
        if self._model_loader is None:
            self._model_loader = ModelLoader(model_provider=self.config.model_provider)
        return self._model_loader

    @property
    def llm(self):
        """Lazy-loaded LLM instance from the configured provider."""
        if self._llm is None:
            self._llm = self.model_loader.load_llm()
        return self._llm

    @property
    def llm_with_tools(self):
        """LLM instance with tools bound for function calling capabilities."""
        if self._llm_with_tools is None:
            self._llm_with_tools = self.llm.bind_tools(tools=self.tools)
        return self._llm_with_tools

    # ---- Tools initialization ----
    def _init_tool_instances(self) -> None:
        self.weather_tools = WeatherInfoTool(
            api_key=self.weather_api_key, base_url=self.weather_base_url
        )
        self.place_search_tools = PlaceSearchTool(tavily_api_key=self.tavily_api_key)
        self.calculator_tools = CalculatorTool()
        self.currency_converter_tools = CurrencyConverterTool(
            api_key=self.exchange_rate_api_key
        )
        self.distance_calculator_tools = DistanceCalculatorTool(
            openroute_api_key=self.openroute_api_key
        )

    def _collect_tools(self) -> List:
        """
        Flatten all tool lists from tool containers into a single list.
        """
        return [
            *self.weather_tools.weather_tool_list,
            *self.place_search_tools.place_search_tool_list,
            *self.calculator_tools.calculator_tool_list,
            *self.currency_converter_tools.currency_converter_tool_list,
            *self.distance_calculator_tools.distance_tool_list,
        ]

    # ---- Agent logic ----
    def _compose_input(self, user_messages: List[str]) -> List[str]:
        """
        Compose input for the LLM by prepending the system prompt.
        """
        return [self.system_prompt] + user_messages

    def agent_function(self, state: MessagesState):
        """
        The node function invoked by the graph. Receives a MessagesState,
        calls the LLM (with tools bound) and returns a MessagesState-like dict.
        """
        user_messages = state["messages"]
        llm_input = self._compose_input(user_messages)
        response = self.llm_with_tools.invoke(llm_input)
        return {"messages": [response]}

    # ---- Graph construction ----
    def build_graph(self) -> StateGraph:
        """
        Build (or return cached) StateGraph connecting the agent and tool node.
        """
        if self.graph is not None:
            return self.graph

        graph_builder = StateGraph(MessagesState)
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))

        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges("agent", tools_condition)
        graph_builder.add_edge("tools", "agent")
        graph_builder.add_edge("agent", END)

        self.graph = graph_builder.compile()
        return self.graph

    def __call__(self) -> StateGraph:
        return self.build_graph()
