"""Model loaders utility module.

This module provides classes for loading and configuring LLM models from different
providers (Groq, OpenAI) based on configuration settings.
"""

from typing import Literal, Optional, Any

from pydantic import BaseModel, Field, model_validator
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
import streamlit as st

from utils.config_loaders import load_config


class ConfigLoader:  # pylint: disable=too-few-public-methods
    """Configuration loader for model settings."""

    def __init__(self):
        print("Loaded config.....")
        self.config = load_config()

    def __getitem__(self, key: str) -> Any:
        return self.config[key]


class ModelLoader(BaseModel):
    """Model loader for LLM providers with configuration support."""

    model_provider: Literal["groq", "openai"] = "groq"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    @model_validator(mode='after')
    def initialize_config(self) -> 'ModelLoader':
        """Initialize configuration after model creation."""
        if self.config is None:
            self.config = ConfigLoader()
        return self

    class Config:  # pylint: disable=too-few-public-methods
        """Pydantic configuration class."""

        arbitrary_types_allowed = True

    def load_llm(self):
        """Load and return the LLM model."""
        print("LLM loading...")
        print("Loading model from provider:", self.model_provider)

        if self.config is None:
            raise ValueError("Configuration not loaded. Ensure model validation ran correctly.")

        llm = None

        if self.model_provider == "groq":
            print("Loading LLM from Groq..............")
            groq_api_key = st.secrets["llm"]["groq"]
            model_name: str = str(self.config["llm"]["groq"]["model_name"])
            llm = ChatGroq(model=model_name, api_key=groq_api_key)
        elif self.model_provider == "openai":
            print("Loading LLM from OpenAI..............")
            openai_api_key = st.secrets["llm"]["openai"]
            llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key)

        return llm
