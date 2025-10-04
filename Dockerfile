# Use official Python image as base
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy backend requirements file
COPY backend/requirements.txt ./

# Install backend dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend project files
COPY backend/ .

# Expose port for the backend
EXPOSE 8000

# Start the backend server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
