#!/bin/bash

echo "Basketball Highlights Extractor"
echo "============================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH."
    echo "Please install Python 3.8 or later."
    exit 1
fi

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "Error: FFmpeg is not installed or not in PATH."
    echo "Please install FFmpeg (e.g., 'sudo apt install ffmpeg' on Ubuntu)."
    exit 1
fi

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Ask for YouTube URL if not provided
URL=$1
if [ -z "$URL" ]; then
    echo
    read -p "Enter YouTube URL of the basketball game: " URL
fi

# Ask for number of highlights
read -p "Enter number of highlights to extract [default: 10]: " NUM_HIGHLIGHTS
NUM_HIGHLIGHTS=${NUM_HIGHLIGHTS:-10}

# Ask for output directory
read -p "Enter output directory [default: highlights]: " OUTPUT_DIR
OUTPUT_DIR=${OUTPUT_DIR:-highlights}

# Run the highlight extractor
echo
echo "Running highlight extractor..."
python highlight_extractor.py --url "$URL" --num_highlights $NUM_HIGHLIGHTS --output "$OUTPUT_DIR"

# Check if the extraction was successful
if [ $? -ne 0 ]; then
    echo
    echo "Extraction failed with error code $?."
    exit $?
fi

# Open the output directory (platform-specific)
echo
echo "Highlights extraction complete!"
echo "Opening output directory..."

# Try to open the output directory based on the platform
if [ "$(uname)" == "Darwin" ]; then
    # macOS
    open "$OUTPUT_DIR"
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    # Linux
    if command -v xdg-open &> /dev/null; then
        xdg-open "$OUTPUT_DIR"
    else
        echo "Output directory: $OUTPUT_DIR"
    fi
else
    echo "Output directory: $OUTPUT_DIR"
fi 