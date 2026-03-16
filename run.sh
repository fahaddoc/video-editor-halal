#!/bin/bash

# Quick run script
cd "$(dirname "$0")"

if [ -d "venv" ]; then
    source venv/bin/activate
    python main.py
else
    echo "Virtual environment not found. Run setup.sh first."
    echo "./setup.sh"
fi
