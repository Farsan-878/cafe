#!/bin/bash
# Cafe Management App - Automatic Setup and Launcher (macOS/Linux)
# Make executable: chmod +x run.sh
# Run: ./run.sh

echo ""
echo "============================================================"
echo "    Cafe Management Web Application - Auto Setup"
echo "============================================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found. Please install Python 3.8+"
    exit 1
fi
echo "✅ Python installed: $(python3 --version)"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt --quiet
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Check/create .env file
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created"
else
    echo "✅ .env file exists"
fi

# Create data directory
mkdir -p ./data
echo "✅ Data directory ready"

# Check MongoDB
echo ""
echo "🔍 Checking for MongoDB..."
if command -v mongod &> /dev/null; then
    echo "✅ MongoDB found"
    echo "🚀 Starting MongoDB..."
    mongod --dbpath ./data &
    MONGO_PID=$!
    sleep 2
    echo "✅ MongoDB started (PID: $MONGO_PID)"
else
    echo "⚠️  MongoDB not found locally"
    echo ""
    echo "MongoDB Options:"
    echo ""
    echo "Option 1: Install MongoDB Community Edition"
    echo "  macOS:  brew install mongodb-community"
    echo "  Linux:  sudo apt install mongodb"
    echo ""
    echo "Option 2: Use MongoDB Atlas (Cloud - Recommended)"
    echo "  1. Go to https://www.mongodb.com/cloud/atlas"
    echo "  2. Create free account and cluster"
    echo "  3. Get connection string"
    echo "  4. Update MONGODB_URI in .env"
    echo ""
    read -p "Continue with current setup? (yes/no): " mongo_choice
    if [ "$mongo_choice" != "yes" ] && [ "$mongo_choice" != "y" ]; then
        exit 1
    fi
fi

# Start Flask app
echo ""
echo "============================================================"
echo "    Starting Flask Application"
echo "============================================================"
echo ""
echo "🌐 App will be available at: http://localhost:5000"
echo "📝 Press Ctrl+C to stop the application"
echo ""

python3 app.py

# Cleanup MongoDB if we started it
if [ ! -z "$MONGO_PID" ]; then
    kill $MONGO_PID 2>/dev/null
    echo "🛑 MongoDB stopped"
fi
