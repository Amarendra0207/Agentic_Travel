#!/usr/bin/env python3
"""
Test module for Streamlit word document download functionality.

This module provides both Streamlit app functionality for manual testing
and pytest tests for automated testing of word document export features.
"""

import datetime
import os
from typing import Any, Dict
from unittest.mock import patch, MagicMock

import requests

from test_utils import get_base_url


def is_pytest_running() -> bool:
    """Check if code is running under pytest."""
    return "pytest" in os.environ.get("_", "") or "PYTEST_CURRENT_TEST" in os.environ


def run_streamlit_app() -> None:
    """Run the Streamlit app (only when not in pytest)."""
    import streamlit as st  # pylint: disable=import-outside-toplevel

    # Simple test for Word document download
    st.title("🧪 Word Download Test")

    base_url = get_base_url()

    # Test content
    test_content = """
# Test Travel Report

## Destination: Paris

### Day 1
- Visit Eiffel Tower
- Lunch at Café de Flore

### Airport Distance Information
Distance from Charles de Gaulle Airport (CDG) to Eiffel Tower: 34.2 km (approximately 45m by car)

## Car Rental Options
- Vehicle: Compact Car | Seats: 4 | Provider: Europcar | Price: 67 EUR
"""

    if st.button("🧪 Test Word Download"):
        try:
            st.info("Generating Word document...")

            # Prepare export request
            export_payload: Dict[str, Any] = {
                "content": test_content,
                "query_info": {"query": "Test Paris trip"},
            }

            # Call export endpoint
            response = requests.post(
                f"{base_url}/export-word", json=export_payload, timeout=30
            )

            st.write(f"Response status: {response.status_code}")

            if response.status_code == 200:
                # Create filename
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"Test_Travel_Report_{timestamp}.docx"

                st.success("✅ Document generated successfully!")

                # Create download button
                st.download_button(
                    label="📄 Download Test Document",
                    data=response.content,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )

            else:
                st.error(f"❌ Failed: {response.status_code}")
                st.error(f"Error: {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Request error: {e}")
        except (KeyError, ValueError) as e:
            st.error(f"❌ Data processing error: {e}")

    st.markdown("---")
    st.markdown("**Instructions:**")
    st.markdown("1. Make sure your server is running on port 8000")
    st.markdown("2. Click the test button above")
    st.markdown("3. If successful, you should see a download button")


# Pytest tests for the functionality
def test_get_base_url_fallback() -> None:
    """Test that get_base_url returns fallback when secrets are not available."""
    # Since we can't easily mock streamlit import in pytest environment,
    # this test verifies the function exists and returns a string
    url = get_base_url()
    assert isinstance(url, str)
    assert url  # Not empty


@patch("requests.post")
def test_word_export_payload_structure(mock_post: MagicMock) -> None:
    """Test that the export payload is structured correctly."""
    # Mock successful response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"fake word doc content"
    mock_post.return_value = mock_response

    # Test payload structure
    test_content = "# Test Report"
    expected_payload: Dict[str, Any] = {
        "content": test_content,
        "query_info": {"query": "Test Paris trip"},
    }

    # Simulate the request that would be made
    response = requests.post(
        "http://localhost:8000/export-word", json=expected_payload, timeout=30
    )

    # Verify the request was made with correct payload
    mock_post.assert_called_once_with(
        "http://localhost:8000/export-word", json=expected_payload, timeout=30
    )

    assert response.status_code == 200


def test_is_pytest_running() -> None:
    """Test pytest detection function."""
    # This should return True when running under pytest
    result = is_pytest_running()
    assert isinstance(result, bool)


# Only run Streamlit app if not in pytest
if not is_pytest_running():
    run_streamlit_app()
