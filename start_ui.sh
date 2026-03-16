#!/bin/bash

# Halal Video Generator - UI Launcher
# ====================================

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║          🌙 HALAL VIDEO GENERATOR - UI 🌙                 ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Run ./setup.sh first"
    exit 1
fi

# Activate venv
source venv/bin/activate

echo "🚀 Starting UI..."
echo ""
echo "   Opening browser at: http://localhost:8501"
echo ""
echo "   Press Ctrl+C to stop the server"
echo ""

# Open browser after delay
(sleep 2 && open http://localhost:8501) &

# Run streamlit
streamlit run app.py --server.headless=true --browser.gatherUsageStats=false
