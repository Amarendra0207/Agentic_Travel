"""Simple download interface for AI Travel Planner.

This module provides a simplified Streamlit interface for generating
travel plans and downloading them as Word documents.
"""

import datetime

import requests
import streamlit as st

# Get BASE_URL from Streamlit secrets
if st.secrets["urls"]["environment"] == "production":
    BASE_URL = st.secrets["urls"]["production"]
else:
    BASE_URL = st.secrets["urls"]["local"]

st.title("🌍 Travel Planner - Fixed Download")

# Input form
with st.form("travel_form"):
    user_input = st.text_input(
        "Where do you want to travel?", placeholder="e.g. Plan a trip to Paris"
    )
    submit = st.form_submit_button("Generate Travel Plan")

if submit and user_input:
    with st.spinner("Generating travel plan..."):
        try:
            # Get travel report
            response = requests.post(
                f"{BASE_URL}/query", json={"query": user_input}, timeout=60
            )

            if response.status_code == 200:
                answer = response.json().get("answer", "")

                # Display the report
                st.markdown("## 🌍 Your Travel Plan")
                st.markdown(answer)

                # Prepare Word document data immediately
                st.markdown("---")

                export_payload = {
                    "content": answer,
                    "query_info": {"query": user_input},
                }

                # Generate Word document
                word_response = requests.post(
                    f"{BASE_URL}/export-word", json=export_payload, timeout=30
                )

                if word_response.status_code == 200:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    FILENAME = f"Travel_Plan_{timestamp}.docx"

                    st.download_button(
                        label="📄 Download as Word Document",
                        data=word_response.content,
                        file_name=FILENAME,
                        mime="application/vnd.openxmlformats-officedocument."
                        "wordprocessingml.document",
                        type="primary",
                    )

                else:
                    st.error("Could not generate Word document")

            else:
                st.error("Failed to generate travel plan")

        except requests.exceptions.RequestException as e:
            st.error(f"Network error: {e}")
        except ValueError as e:
            st.error(f"Invalid response format: {e}")
        except (KeyError, AttributeError) as e:
            st.error(f"Data processing error: {e}")
