#!/bin/bash

# Dual Source Financial News Scraper - Simplified Execution Script
# This script runs the CNBC and CNN news scraper with proper environment setup

echo "==========================================="
echo "Starting Dual Source Financial News Scraper"
echo "Date: $(date)"
echo "==========================================="

# Set script directory as the project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Verify Python interpreter
PYTHON_VERSION=$(python --version 2>&1)
echo "Python version: $PYTHON_VERSION"

# Activate virtual environment if it exists
if [ -d "./.venv" ]; then
    echo "Activating virtual environment..."
    source ./.venv/bin/activate
elif [ -d "./venv" ]; then
    echo "Activating virtual environment..."
    source ./venv/bin/activate
else
    echo "Creating and activating new virtual environment..."
    python -m venv ./venv
    source ./venv/bin/activate
fi

# Install dependencies if not already installed
echo "Installing required dependencies..."
pip install -r requirements.txt || pip install httpx beautifulsoup4 python-dateutil pytest

# Run the scraper and redirect output to log file
echo "Running news scraper..."
python -c "from src.scraper import run_scraper; run_scraper()" "$@" 2>&1 | tee -a scraper_run.log

EXIT_CODE=${PIPESTATUS[0]}

if [ $EXIT_CODE -eq 0 ]; then
    echo "==========================================="
    echo "News scraping completed successfully!"
    echo "Date: $(date)"
    echo "Check output files in current directory"
    echo "Log file: scraper_run.log"
    echo "==========================================="
else
    echo "==========================================="
    echo "News scraping encountered errors!"
    echo "Exit code: $EXIT_CODE"
    echo "Check log file for details: scraper_run.log"
    echo "==========================================="
    exit $EXIT_CODE
fi