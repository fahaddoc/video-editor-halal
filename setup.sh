#!/bin/bash

# Halal Video Generator - Setup Script
# =====================================

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║          🌙 HALAL VIDEO GENERATOR - SETUP 🌙              ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check Python
echo "Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Found $PYTHON_VERSION"
else
    echo "✗ Python 3 not found!"
    echo "  Please install Python from: https://python.org"
    exit 1
fi

# Check pip
echo "Checking pip..."
if command -v pip3 &> /dev/null; then
    echo "✓ pip3 found"
else
    echo "✗ pip3 not found. Installing..."
    python3 -m ensurepip --upgrade
fi

# Check FFmpeg
echo "Checking FFmpeg..."
if command -v ffmpeg &> /dev/null; then
    echo "✓ FFmpeg found"
else
    echo "✗ FFmpeg not found!"
    echo ""
    echo "  Install FFmpeg:"
    echo "  - macOS:   brew install ffmpeg"
    echo "  - Ubuntu:  sudo apt install ffmpeg"
    echo "  - Windows: Download from https://ffmpeg.org"
    echo ""
    read -p "Continue without FFmpeg? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p output assets templates

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "✅ SETUP COMPLETE!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "To run the application:"
echo ""
echo "  1. Activate virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the app:"
echo "     python main.py"
echo ""
echo "Optional: Set Pexels API key for stock footage:"
echo "  export PEXELS_API_KEY=your_key_here"
echo ""
echo "Get free Pexels API key at: https://www.pexels.com/api/"
echo ""
