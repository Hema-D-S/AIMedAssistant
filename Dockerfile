# Use official lightweight Python base image
FROM python:3.10-slim

# Prevent interactive prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    portaudio19-dev \
    libportaudio2 \
    libportaudiocpp0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better Docker caching
COPY Requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r Requirements.txt

# Copy the rest of the project
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Ensure start.sh is executable
RUN chmod +x start.sh

# Start the app
CMD ["bash", "start.sh"]
