"""Main FastAPI application for AI Travel Planner.

This module provides REST API endpoints for travel planning, including:
- Travel query processing with budget preferences
- Car rental integration
- Airport distance calculations
- Word document export functionality
"""

import os
from typing import Optional, Dict, Any

from airportsdata import load
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from agent.agentic_workflow import GraphBuilder
from utils.airport_distance_calculator import AirportDistanceCalculator
from utils.car_rental_service import CarRentalService
from utils.word_document_exporter import WordDocumentExporter

load_dotenv()  # Load environment variables from .env file

app = FastAPI()


class QueryRequest(BaseModel):
    """Request model for travel query with location and budget preferences."""

    query: Optional[str] = None
    question: Optional[str] = None
    budget_preference: str = (
        "budget_friendly"  # New field: cheapest, budget_friendly, luxurious
    )
    startLocationCode: Optional[str] = None  # IATA or city code for origin
    endLocationCode: Optional[str] = None  # IATA or city code for destination
    startCity: Optional[str] = None  # City name for origin (optional)
    endCity: Optional[str] = None  # City name for destination (optional)


class WordExportRequest(BaseModel):
    """Request model for Word document export with content and metadata."""

    content: str
    query_info: Optional[Dict[str, Any]] = None


@app.post("/query")
# pylint: disable=too-many-locals,too-many-branches,too-many-statements
async def query_travel_agent(query: QueryRequest):
    """
    Example request body:
        {
            "query": "Plan a trip from New York to London",
            "startLocationCode": "JFK",
            "endLocationCode": "LHR"
        }
    """
    try:
        # Get budget preference from request
        budget_preference = getattr(query, "budget_preference", "budget_friendly")
        print(f"Budget preference: {budget_preference}")

        # Load API keys from environment variables
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        exchange_rate_api_key = os.getenv("EXCHANGE_RATE_API_KEY")
        weather_api_key = os.getenv("WEATHER_API_KEY")
        weather_base_url = os.getenv("WEATHER_BASE_URL")
        openroute_api_key = os.getenv("OPENROUTE_API_KEY")

        # Initialize graph with budget preference and API keys
        graph = GraphBuilder(
            tavily_api_key=tavily_api_key,
            exchange_rate_api_key=exchange_rate_api_key,
            weather_api_key=weather_api_key,
            weather_base_url=weather_base_url,
            openroute_api_key=openroute_api_key,
            model_provider="groq",
            budget_preference=budget_preference,
        )
        react_app = graph()

        png_graph = react_app.get_graph().draw_mermaid_png()
        with open("my_graph.png", "wb") as f:
            f.write(png_graph)

        print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")

        # Support both 'query' and 'question' fields
        user_query = query.query if query.query is not None else query.question

        # Add budget context to the query
        budget_display = {
            "cheapest": "ultra budget-friendly",
            "budget_friendly": "good value for money",
            "luxurious": "premium luxury",
        }.get(budget_preference, "good value for money")

        # Add airport context to the query if provided
        has_location_context = (
            query.startLocationCode
            or query.endLocationCode
            or query.startCity
            or query.endCity
        )
        if has_location_context:
            context_info = []
            if query.startLocationCode:
                context_info.append(f"Starting from airport: {query.startLocationCode}")
            if query.endLocationCode:
                context_info.append(f"Destination airport: {query.endLocationCode}")
            if query.startCity:
                context_info.append(f"Starting city: {query.startCity}")
            if query.endCity:
                context_info.append(f"Destination city: {query.endCity}")

            context_str = ", ".join(context_info)
            enhanced_query = (
                f"{user_query}\n\n"
                f"Budget Preference: I prefer {budget_display} travel options.\n\n"
                f"Additional Context: {context_str}\n\n"
                "Please include distance information from airports to attractions "
                "in your response and tailor all recommendations to my budget preference."
            )
        else:
            enhanced_query = (
                f"{user_query}\n\n"
                f"Budget Preference: I prefer {budget_display} travel options.\n\n"
                "Please include distance information from airports to attractions "
                "in your response and tailor all recommendations to my budget preference."
            )

        messages = {"messages": [enhanced_query]}

        output = react_app.invoke(messages)

        # If result is dict with messages:
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content  # Last AI response
        else:
            final_output = str(output)

        # --- Car Rental Integration ---
        car_rental_section = "\n\n## Car Rental Options\n"
        try:
            car_rental_service = CarRentalService()
            airports = load("IATA")

            def city_to_iata(city_name):
                city_name = city_name.lower().strip()
                for code, data in airports.items():
                    if data.get("city", "").lower() == city_name:
                        return code
                return None

            # Use codes from request, or try to convert city names, fallback to CCU
            start_code = (
                query.startLocationCode
                or (city_to_iata(query.startCity) if query.startCity else None)
                or "CCU"
            )
            end_code = (
                query.endLocationCode
                or (city_to_iata(query.endCity) if query.endCity else None)
                or "CCU"
            )
            car_rentals = car_rental_service.search_cars(
                start_location_code=start_code,
                end_location_code=end_code,
                transfer_type="HOURLY",
                start_date_time="2025-10-10T10:00:00",
                duration="PT9H30M",
                passengers=1,
            )
            # Handle response according to response.json format
            if isinstance(car_rentals, dict) and "data" in car_rentals:
                for offer in car_rentals["data"]:
                    vehicle = offer.get("vehicle", {})
                    provider = offer.get("serviceProvider", {})
                    partner = offer.get("partnerInfo", {}).get("serviceProvider", {})
                    quotation = offer.get("quotation", {})
                    cancellation_rules = offer.get("cancellationRules", [{}])
                    cancellation = cancellation_rules[0].get("ruleDescription", "N/A")
                    desc = vehicle.get("description", "N/A")
                    seats = vehicle.get("seats", [{}])[0].get("count", "N/A")
                    baggages = vehicle.get("baggages", [{}])[0].get("count", "N/A")
                    provider_name = provider.get("name", partner.get("name", "N/A"))
                    price = quotation.get("monetaryAmount", "N/A")
                    currency = quotation.get("currencyCode", "N/A")
                    car_rental_section += (
                        f"- Vehicle: {desc} | Seats: {seats} | "
                        f"Baggage: {baggages} | Provider: {provider_name} | "
                        f"Price: {price} {currency}\n"
                        f"  Cancellation: {cancellation}\n"
                    )
            else:
                car_rental_section += str(car_rentals) + "\n"
        except (KeyError, ValueError, TypeError, ConnectionError) as e:
            car_rental_section += f"Car rental info unavailable: {e}\n"

        # --- Distance Information Integration ---
        distance_section = "\n\n"
        try:
            distance_calculator = AirportDistanceCalculator(
                api_key=openroute_api_key
            )

            # If airport codes are provided, calculate distances
            if query.startLocationCode or query.endLocationCode:
                airport_code = query.startLocationCode or query.endLocationCode
                destination_city = query.endCity or query.startCity or "the destination"

                distance_section += "### Airport Distance Information\n\n"

                # Find major attractions in the destination city and calculate distances
                major_attractions = [
                    f"{destination_city} city center",
                    f"downtown {destination_city}",
                    f"main tourist area {destination_city}",
                ]

                for attraction in major_attractions:
                    distance_info = (
                        distance_calculator.get_airport_to_attraction_distance(
                            airport_code, attraction
                        )
                    )
                    formatted_info = distance_calculator.format_distance_info(
                        distance_info
                    )
                    distance_section += formatted_info + "\n\n"

                # Find nearest airports to destination
                if query.endCity:
                    nearest_airports = (
                        distance_calculator.find_nearest_airports_to_city(query.endCity)
                    )
                    if nearest_airports:
                        distance_section += (
                            f"### Nearest Airports to {query.endCity}\n\n"
                        )
                        for airport in nearest_airports[:3]:
                            airport_info = (
                                f"Airport: {airport['name']} ({airport['code']}) - "
                                f"{airport['distance_km']} km away\n"
                            )
                            distance_section += airport_info
                        distance_section += "\n"

        except (KeyError, ValueError, TypeError, ConnectionError) as e:
            distance_section += f"Distance information unavailable: {e}\n"

        # Append distance info to the report
        final_output += distance_section

        # Append car rental info to the report
        final_output += car_rental_section

        return {"answer": final_output}
    except (ValueError, TypeError, ConnectionError, RuntimeError) as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/export-word")
async def export_to_word(request: WordExportRequest):
    """
    Export travel report to Word document

    Example request body:
        {
            "content": "Travel report content here...",
            "query_info": {
                "startCity": "New York",
                "endCity": "London",
                "startLocationCode": "JFK",
                "endLocationCode": "LHR"
            }
        }
    """
    try:
        word_exporter = WordDocumentExporter()

        # Create Word document
        doc_path = word_exporter.create_travel_report_doc(
            content=request.content, query_info=request.query_info
        )

        # Get filename for response
        filename = os.path.basename(doc_path)

        # Return file as download
        return FileResponse(
            path=doc_path,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    except (OSError, IOError, ValueError) as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to create Word document: {str(e)}"},
        )


@app.get("/download-sample-report")
async def download_sample_report():
    """Download a sample travel report in Word format"""
    try:
        word_exporter = WordDocumentExporter()

        sample_content = """
# Sample Travel Plan - New York City

## Day 1: Arrival and Manhattan Exploration
- Arrive at JFK Airport
- Check into hotel in Times Square area
- Visit Central Park
- Dinner at local restaurant

### Airport Distance Information
Distance from John F Kennedy International Airport (JFK) to Times Square: 26.45 km (approximately 31m by car)

## Day 2: Museums and Culture
- Visit Metropolitan Museum of Art
- Lunch in Upper East Side
- Broadway show in the evening

## Car Rental Options
- Vehicle: Economy Car | Seats: 4 | Provider: Hertz | Price: $89 USD
"""

        query_info = {
            "startCity": "New York",
            "endCity": "New York",
            "startLocationCode": "JFK",
            "endLocationCode": "JFK",
        }

        doc_path = word_exporter.create_travel_report_doc(sample_content, query_info)
        filename = os.path.basename(doc_path)

        return FileResponse(
            path=doc_path,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    except (OSError, IOError, ValueError) as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to create sample document: {str(e)}"},
        )
