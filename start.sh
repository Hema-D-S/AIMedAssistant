#!/bin/bash

echo "Starting AI Medical Assistant..."
echo "Checking environment..."

# Check if required environment variables are set
if [ -z "$GROQ_API_KEY" ]; then
    echo "Warning: GROQ_API_KEY not set"
fi

if [ -z "$ELEVENLABS_API_KEY" ]; then
    echo "Warning: ELEVENLABS_API_KEY not set"
fi

echo "Launching Gradio app..."
python gradio_app.py
