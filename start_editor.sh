#!/bin/bash

# Halal Video Editor - Launcher
# =============================

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║          🎬 HALAL VIDEO EDITOR 🎬                         ║"
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

echo "🚀 Starting Video Editor..."
echo ""
echo "   Opening browser at: http://localhost:8501"
echo ""
echo "   Press Ctrl+C to stop"
echo ""

# Open browser after delay
(sleep 2 && open http://localhost:8501) &

# Run streamlit
streamlit run editor.py --server.headless=true --browser.gatherUsageStats=false
