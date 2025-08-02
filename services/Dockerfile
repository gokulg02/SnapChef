# Use a slim Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /services

# Install system-level dependencies
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your app code
COPY . .

# Expose the Flask port
EXPOSE 8000

# Start the Flask API
CMD ["python", "services/app.py"]
