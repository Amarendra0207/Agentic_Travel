# Use official Python image as base
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy requirements file if exists
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port (change if your app uses a different port)
EXPOSE 8501

# Start both backend and frontend
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 --reload & streamlit run streamlit/app.py --server.port=8501 --server.address=0.0.0.0"]