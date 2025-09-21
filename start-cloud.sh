#!/bin/bash

# Cloud deployment startup script (no Docker required)
echo "🚀 Starting Legal Document Simplifier (Cloud Mode)..."

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r backend/requirements.txt

# Start the backend server
echo "🌐 Starting backend server..."
cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
