#!/bin/bash

# Horse Racing Management System - Setup Script

echo "🐴 Horse Racing Management System - Setup"
echo "==========================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
echo "✓ Dependencies installed"

# Create database
echo "Initializing database..."
if [ -f "horse_races.db" ]; then
    echo "Old database found. Backing up to horse_races.db.bak"
    cp horse_races.db horse_races.db.bak
fi

python3 << 'EOF'
from app import app, db

with app.app_context():
    db.create_all()
    print("✓ Database created/updated")
EOF

echo ""
echo "Setup complete! 🎉"
echo ""
echo "To run the application:"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "Then open http://127.0.0.1:5000 in your browser"
