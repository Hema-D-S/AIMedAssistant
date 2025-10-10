#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Starting AI Medical Assistant..."
echo "Working directory: $(pwd)"

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Error: Virtual environment not found at venv/bin/activate"
    exit 1
fi

# Load environment variables from .env file - FIXED VERSION
if [ -f ".env" ]; then
    echo "Loading environment variables from .env..."
    set -a  # automatically export all variables
    source .env
    set +a  # stop automatically exporting
    echo "Environment variables loaded successfully"
else
    echo "Warning: .env file not found"
fi

echo "Checking environment..."

# Check if required environment variables are set
if [ -z "$GROQ_API_KEY" ]; then
    echo "Warning: GROQ_API_KEY not set"
fi

if [ -z "$ELEVENLABS_API_KEY" ]; then
    echo "Warning: ELEVENLABS_API_KEY not set"
fi

# Check if required files exist
required_files=("Themedbot.py" "mainfile.py" "gradio_app_server.py")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "Error: Required file $file not found"
        exit 1
    fi
done

echo "All checks passed. Installing/updating dependencies..."

# Install or update dependencies
pip install -r Requirements.txt

echo "Starting AI Medical Assistant server..."
python3 gradio_app_server.py