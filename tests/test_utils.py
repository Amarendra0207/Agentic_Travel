#!/usr/bin/env python3
"""
Shared test utilities to avoid code duplication across test files.

This module provides common functionality used by multiple test files,
particularly for handling Streamlit secrets in CI environments.
"""


def get_base_url() -> str:
    """Get base URL with fallback for testing environments."""
    try:
        import streamlit as st  # pylint: disable=import-outside-toplevel
        if st.secrets["urls"]["environment"] == "production":
            return str(st.secrets["urls"]["production"])
        return str(st.secrets["urls"]["local"])
    except ImportError:
        # Streamlit not available
        return "http://localhost:8000"
    except (KeyError, AttributeError):
        # Secrets structure issues
        return "http://localhost:8000"
    except Exception:  # pylint: disable=broad-except
        # Catch StreamlitSecretNotFoundError and other Streamlit exceptions
        return "http://localhost:8000"


def get_map_api_key() -> str:
    """Get MAP API key with fallback for testing environments."""
    try:
        import streamlit as st  # pylint: disable=import-outside-toplevel
        return str(st.secrets["map"]["api_key"])
    except ImportError:
        # Streamlit not available
        return ""
    except (KeyError, AttributeError):
        # Secrets structure issues
        return ""
    except Exception:  # pylint: disable=broad-except
        # Catch StreamlitSecretNotFoundError and other Streamlit exceptions
        return ""
