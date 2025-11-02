#!/bin/bash
# Setup script for Medical Report Analyzer

set -e

echo "🏥 Medical Report Analyzer - Setup Script"
echo "=========================================="

# Check Python
echo "Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.11+"
    exit 1
fi
echo "✅ Python found: $(python3 --version)"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv
echo "✅ Virtual environment created"

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt
echo "✅ Dependencies installed"

# Create uploads directory
echo ""
echo "Creating uploads directory..."
mkdir -p uploads
echo "✅ Uploads directory created"

# Check Docker (optional)
echo ""
if command -v docker &> /dev/null; then
    echo "✅ Docker found: $(docker --version)"
else
    echo "⚠️  Docker not found (optional for containerized deployment)"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run: python backend/app.py"
echo "  3. Access at: http://localhost:5000"
echo ""

