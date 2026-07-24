# Use the modern official lightweight Python 3.13 slim image
FROM python:3.13-slim

# Set working directory inside the container
WORKDIR /app

# Prevent Python from writing .pyc files and enable unbuffered terminal logging for instant outputs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy only requirements to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Declare a volume for persistent storage of local cache JSONL files
# This prevents data loss if the container is recreated mid-day
VOLUME ["/app/local_cache"]

# Execute the application orchestrator
CMD ["python", "main.py"]
