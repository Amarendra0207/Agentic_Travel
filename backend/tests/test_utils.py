#!/usr/bin/env python3
"""
Shared test utilities to avoid code duplication across test files.

This module provides common functionality used by multiple test files,
particularly for handling Streamlit secrets in CI environments.
"""


import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_base_url() -> str:
    """Get base URL from environment variables with a fallback for local testing."""
    return os.getenv("BASE_URL", "http://localhost:8000")


def get_map_api_key() -> str:
    """Get MAP API key from environment variables with a fallback for local testing."""
    return os.getenv("OPENROUTE_API_KEY", "")
