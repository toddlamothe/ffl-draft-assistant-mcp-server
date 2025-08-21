#!/bin/bash

# Fantasy Football MCP Server Startup Script
# This script starts the MCP server for testing in Cursor

echo "🚀 Starting Fantasy Football MCP Server..."
echo "=========================================="

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not detected. Activating..."
    source venv/bin/activate
fi

# Check if we're in the right directory
if [[ ! -f "app/server.py" ]]; then
    echo "❌ Error: app/server.py not found. Please run this script from the project root."
    exit 1
fi

echo "✅ Virtual environment: $VIRTUAL_ENV"
echo "✅ Project directory: $(pwd)"
echo ""
echo "Starting MCP server..."
echo "Press Ctrl+C to stop the server"
echo ""

# Start the MCP server
python app/server.py
