# 🌍 AI Travel Planner

An intelligent travel planning application powered by AI agents that provides comprehensive travel recommendations with budget-aware suggestions, real-time information, and document export capabilities.

## 🚀 Features

### Core Functionality

- **🤖 AI-Powered Travel Planning**: LangGraph-based agent architecture with intelligent decision making
- **💰 Budget-Aware Recommendations**: Support for multiple budget preferences (cheapest, budget-friendly, luxurious)
- **🌐 Multi-Provider LLM Support**: Compatible with Groq and OpenAI models
- **📊 Real-Time Data Integration**: Live weather, currency rates, and location information
- **✈️ Airport & Distance Calculations**: Accurate airport-to-destination distance and travel time estimates
- **🚗 Car Rental Integration**: Amadeus API integration for car rental options
- **📄 Document Export**: Generate professional Word documents with travel itineraries

### User Interfaces

- **🌐 Streamlit Web App**: Interactive web interface for travel planning
- **🔗 FastAPI Backend**: REST API endpoints for programmatic access
- **📱 Responsive Design**: Mobile-friendly interface

### Advanced Tools

- **🌤️ Weather Information**: Real-time weather data for destinations
- **💱 Currency Conversion**: Live exchange rates and cost calculations  
- **📍 Place Search & Information**: Detailed location data and recommendations
- **🧮 Expense Calculator**: Budget tracking and cost estimation
- **📏 Distance Calculator**: Multi-modal distance and travel time calculations

## 🏗️ Architecture

```text
AI Travel Planner
├── 🌐 Frontend (Streamlit)
├── 🔗 Backend (FastAPI)  
├── 🤖 AI Agent (LangGraph)
├── 🛠️ Tools & Utilities
├── 📊 External APIs
└── 🧪 Testing Suite
```

### Component Overview

- **Agent Layer**: LangGraph-based workflow management with state machines
- **Tools Layer**: Modular tools for weather, currency, distance, and place information
- **Utils Layer**: Core utilities for data processing and external service integration
- **API Layer**: RESTful endpoints and Streamlit web interface
- **Configuration**: YAML-based configuration with environment-specific settings

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- Virtual environment (recommended)
- API keys for external services (see Configuration section)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI_Travel_Planner
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment** (see Configuration section below)

5. **Run the application**
   
   **Option A: Backend + Frontend (Recommended)**
   ```bash
   # Terminal 1: Start FastAPI backend
   uvicorn main:app --reload --port 8000
   
   # Terminal 2: Start Streamlit frontend  
   streamlit run streamlit/app.py
   ```
   
   **Option B: Docker (All-in-one)**
   ```bash
   docker build -t ai-travel-planner .
   docker run -p 8000:8000 -p 8501:8501 ai-travel-planner
   ```

6. **Access the application**
   - **Web Interface**: <http://localhost:8501>
   - **API Documentation**: <http://localhost:8000/docs>
   - **API Endpoints**: <http://localhost:8000>

## ⚙️ Configuration

### Required API Keys

Create a `.streamlit/secrets.toml` file with the following structure:

```toml
[llm]
groq = "your-groq-api-key"
openai = "your-openai-api-key"

[map]
api_key = "your-openrouteservice-api-key"

[weather] 
api_key = "your-openweathermap-api-key"
base_url = "https://api.openweathermap.org/data/2.5"

[amadeus]
api_key = "your-amadeus-api-key"
api_secret = "your-amadeus-api-secret"  
base_url = "https://test.api.amadeus.com/v1"
token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"

[urls]
environment = "local"  # or "production"
local = "http://localhost:8000"
production = "your-production-url"
```

### External Service Setup

1. **Groq API**: Get your API key from [Groq Console](https://console.groq.com/)
2. **OpenAI API**: Get your API key from [OpenAI Platform](https://platform.openai.com/)
3. **OpenRouteService**: Get your API key from [OpenRouteService](https://openrouteservice.org/)
4. **OpenWeatherMap**: Get your API key from [OpenWeatherMap](https://openweathermap.org/api)
5. **Amadeus**: Get your API credentials from [Amadeus for Developers](https://developers.amadeus.com/)

### Model Configuration

Edit `config/config.yaml` to customize LLM providers and models:

```yaml
llm:
  openai:
    provider: "openai"
    model_name: "gpt-4o-mini"
  groq:
    provider: "groq" 
    model_name: "deepseek-r1-distill-llama-70b"
```

## 📖 Usage

### Web Interface (Streamlit)

1. Navigate to <http://localhost:8501>
2. Select your budget preference (Cheapest/Budget Friendly/Luxurious)
3. Enter your travel query (e.g., "Plan a 3-day trip to Paris")
4. Optionally specify start/end locations
5. Click "Get Travel Plan" to generate recommendations
6. Export results to Word document if needed

### API Usage (FastAPI)

**Travel Query Example:**
```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "Plan a 3-day trip to Tokyo",
       "budget_preference": "budget_friendly",
       "startCity": "New York",
       "endCity": "Tokyo"
     }'
```

**Word Export Example:**
```bash
curl -X POST "http://localhost:8000/export-word" \
     -H "Content-Type: application/json" \
     -d '{
       "content": "# My Travel Plan\n\nDetailed itinerary...",
       "query_info": {"query": "Tokyo trip"}
     }' \
     --output travel_plan.docx
```

### Budget Preferences

- **cheapest**: Focuses on budget accommodations, public transport, free activities
- **budget_friendly**: Balance of cost and comfort with moderate spending
- **luxurious**: Premium accommodations, private transport, exclusive experiences

## 🧪 Testing

The project includes comprehensive test coverage with both unit and integration tests.

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test Categories
```bash
# API endpoint tests
pytest tests/test_api_endpoint.py -v

# Distance calculation tests  
pytest tests/test_distance.py -v

# Basic functionality tests
pytest tests/test_basic.py -v

# Budget integration tests
pytest tests/test_budget_integration.py -v
```

### Test Features

- **CI/CD Compatible**: All tests run successfully in GitHub Actions
- **Fast Offline Tests**: Distance calculations with known coordinates
- **API Integration Tests**: Real API testing with proper fallbacks
- **Mock Support**: Comprehensive mocking for external dependencies

## 🏢 Project Structure

```
AI_Travel_Planner/
├── 📁 agent/                    # AI agent and workflow management
│   ├── __init__.py
│   └── agentic_workflow.py      # LangGraph state machine
├── 📁 config/                   # Configuration files
│   ├── __init__.py
│   └── config.yaml              # LLM and model settings  
├── 📁 prompt_library/           # AI prompt templates
│   ├── __init__.py
│   └── prompt.py                # System prompts for agents
├── 📁 streamlit/               # Web interface
│   ├── app.py                  # Main Streamlit application
│   └── simple_download.py      # Document download interface
├── 📁 tests/                   # Test suite
│   ├── test_*.py              # Individual test modules
│   └── test_utils.py          # Shared test utilities
├── 📁 tools/                  # AI agent tools
│   ├── currency_conversion_tool.py
│   ├── distance_calculator_tool.py
│   ├── expense_calculator_tool.py  
│   ├── place_search_tool.py
│   └── weather_info_tool.py
├── 📁 utils/                  # Core utilities
│   ├── airport_distance_calculator.py
│   ├── car_rental_service.py
│   ├── config_loaders.py
│   ├── currency_convertor.py
│   ├── model_loaders.py
│   ├── place_info_search.py
│   ├── weather_info.py
│   └── word_document_exporter.py
├── 📄 main.py                 # FastAPI backend server
├── 📄 requirements.txt        # Python dependencies
├── 📄 Dockerfile             # Container configuration
└── 📄 README.md              # This file
```

## 🔧 Development

### Code Quality

The project maintains high code quality standards:

- **Pylint Score**: 10.00/10 across all modules
- **Type Annotations**: Comprehensive typing with mypy compatibility
- **Documentation**: Detailed docstrings following Google/Numpy style
- **Error Handling**: Robust exception handling with proper fallbacks

### Development Workflow

1. **Setup Development Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run Code Quality Checks**
   ```bash
   # Pylint check
   pylint utils/ tools/ agent/ tests/
   
   # Run tests
   pytest tests/ -v
   ```

3. **Local Development Server**
   ```bash
   # Backend (with auto-reload)
   uvicorn main:app --reload --port 8000
   
   # Frontend (with auto-reload)
   streamlit run streamlit/app.py
   ```

### Adding New Tools

1. Create tool in `tools/` directory following existing patterns
2. Implement proper error handling and type annotations  
3. Add tool to agent workflow in `agent/agentic_workflow.py`
4. Add corresponding tests in `tests/`
5. Update documentation

### CI/CD

GitHub Actions workflow automatically:
- Runs full test suite on Python 3.13
- Validates code quality with pylint
- Tests in CI environment without external API dependencies
- Supports both Ubuntu and other platforms

## 📚 API Reference

### FastAPI Endpoints

#### POST /query
Generate travel recommendations based on user input.

**Request Body:**
```json
{
  "question": "string",
  "budget_preference": "cheapest|budget_friendly|luxurious", 
  "startCity": "string (optional)",
  "endCity": "string (optional)",
  "startLocationCode": "string (optional)",
  "endLocationCode": "string (optional)"
}
```

**Response:**
```json
{
  "response": "string",
  "airport_distances": [...],
  "car_rentals": [...]
}
```

#### POST /export-word
Export travel plan to Word document.

**Request Body:**
```json
{
  "content": "string",
  "query_info": {
    "query": "string"
  }
}
```

**Response:** Binary Word document (.docx)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following the code quality standards
4. Add tests for new functionality
5. Ensure all tests pass (`pytest tests/`)
6. Ensure code quality (`pylint` score 10.00/10)
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

## 🙋‍♂️ Support & Contact

- **Issues**: Create an issue on GitHub for bug reports or feature requests
- **Documentation**: Comprehensive API docs available at `/docs` endpoint
- **Examples**: See `tests/` directory for usage examples

## 🎯 Roadmap

### Upcoming Features
- [ ] Multi-language support
- [ ] Mobile application
- [ ] Advanced budget optimization algorithms
- [ ] Integration with booking platforms
- [ ] Real-time collaboration features
- [ ] Enhanced AI personalization

### Performance Improvements
- [ ] Caching layer for external API calls
- [ ] Async processing for large queries
- [ ] Database integration for user preferences
- [ ] Advanced error recovery mechanisms

---

---

*Built with ❤️ using Python, FastAPI, Streamlit, LangGraph, and modern AI technologies*
