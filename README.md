# 🌍 AI Travel Planner

An intelligent travel planning application powered by AI agents that provides comprehensive travel recommendations with budget-aware suggestions, real-time information, and document export capabilities.

## 🏗️ Architecture

This project is now split into two main components:

-   **`/frontend`**: A Streamlit application that serves as the user interface.
-   **`/backend`**: A FastAPI application that runs the AI agent, manages tools, and handles all business logic.

This separation makes the project more organized, scalable, and easier to maintain.

## 🚀 Quick Start

Here’s how to get the application running.

### Prerequisites

-   Python 3.13+
-   A virtual environment tool (e.g., `venv`)
-   API keys for the required external services (see Backend Configuration).

### 1. Backend Setup

First, set up and run the backend server.

```bash
# 1. Navigate to the backend directory
cd backend

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install backend dependencies
pip install -r requirements.txt

# 4. Configure API Keys (see Backend Configuration below)

# 5. Run the backend server
uvicorn main:app --host 0.0.0.0 --port 8000
```

The backend API will be available at `http://localhost:8000`.

### 2. Frontend Setup

In a **new terminal**, set up and run the Streamlit frontend.

```bash
# 1. Navigate to the frontend directory
cd frontend

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install frontend dependencies
pip install -r requirements.txt

# 4. Run the frontend application
streamlit run streamlit_app.py
```

The frontend will be available at `http://localhost:8501`.

## ⚙️ Configuration

### Backend Configuration (Required)

The backend requires API keys to connect to various services. The recommended way is to create a `.env` file inside the `backend/` directory.

1.  Create a file named `.env` in the `backend/` folder.
2.  Add your secrets to it like this:

    ```env
    # Groq LLM
    GROQ_API_KEY="your-groq-api-key"

    # Tavily Search API
    TAVILY_API_KEY="your-tavily-api-key"

    # Exchange Rate APIs
    EXCHANGE_RATE_API_KEY="your-exchangerate-api-key"
    ALPHAVANTAGE_API_KEY="your-alphavantage-api-key"

    # OpenWeatherMap API
    WEATHER_API_KEY="your-openweathermap-api-key"
    WEATHER_BASE_URL="https://api.openweathermap.org/data/2.5"

    # OpenRouteService API
    OPENROUTE_API_KEY="your-openrouteservice-api-key"

    # Amadeus API
    AMADEUS_API_KEY="your-amadeus-api-key"
    AMADEUS_API_SECRET="your-amadeus-api-secret"
    AMADEUS_BASE_URL="https://test.api.amadeus.com/v1"
    AMADEUS_TOKEN_URL="https://test.api.amadeus.com/v1/security/oauth2/token"
    ```

    The application uses `python-dotenv` to load these variables automatically.

### Frontend Configuration

The frontend needs to know the URL of the backend. This is configured in `.streamlit/secrets.toml` within the `frontend` directory. You can create this file if it doesn't exist.

```toml
[urls]
environment = "local"
local = "http://localhost:8000"
production = "your-deployed-backend-url"
```

## 🧪 Testing

All tests are located in the `backend/tests/` directory and should be run from within the `backend` folder.

```bash
# Navigate to the backend directory
cd backend

# Run all tests
pytest -v
```

## 🐳 Docker

The included `Dockerfile` is configured to build and run the **backend** service.

```bash
# Build the Docker image from the project root
docker build -t ai-travel-planner-backend .

# Run the container, exposing the backend port
docker run -p 8000:8000 -v ./.env:/app/.env ai-travel-planner-backend
```

## 🏢 New Project Structure

```
AI_Travel_Planner/
├── 📁 backend/                  # FastAPI Backend Application
│   ├── 📁 agent/
│   ├── 📁 config/
│   ├── 📁 prompt_library/
│   ├── 📁 tests/
│   ├── 📁 tools/
│   ├── 📁 utils/
│   ├── main.py                 # FastAPI entry point
│   └── requirements.txt
│
├── 📁 frontend/                 # Streamlit Frontend Application
│   ├── 📁 .streamlit/
│   ├── 📁 streamlit/
│   ├── streamlit_app.py        # Streamlit entry point
│   └── requirements.txt
│
├── 📄 .gitignore
├── 📄 Dockerfile               # For the backend
└── 📄 README.md                # This file
```