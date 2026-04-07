#!/usr/bin/env python3
"""
Cafe Management App - Automatic Setup and Launcher
This script handles MongoDB setup and launches the Flask app
"""

import os
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def check_mongodb():
    """Check if MongoDB is installed"""
    try:
        result = subprocess.run(['mongod', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ MongoDB is installed")
            return True
    except FileNotFoundError:
        pass

    print("❌ MongoDB not found")
    return False

def install_mongodb_instructions():
    """Provide MongoDB installation instructions"""
    print("\n" + "="*60)
    print("📦 MongoDB Installation Required")
    print("="*60)
    print("""
MongoDB is not installed. Choose one of the following:

Option 1: MongoDB Community Edition (Local)
  Windows: Download from https://www.mongodb.com/try/download/community
  macOS:   brew install mongodb-community
  Linux:   sudo apt install mongodb

Option 2: MongoDB Atlas (Cloud - Recommended for Production)
  1. Go to https://www.mongodb.com/cloud/atlas
  2. Create free account
  3. Create cluster
  4. Copy connection string
  5. Update MONGODB_URI in .env with:
     mongodb+srv://username:password@cluster.mongodb.net/cafe_db

For quick local setup, download MongoDB Community Edition from:
https://www.mongodb.com/try/download/community
""")
    print("="*60 + "\n")

def start_mongodb():
    """Try to start MongoDB service"""
    print("🚀 Starting MongoDB...")
    try:
        # Try Windows service
        subprocess.Popen(['mongod', '--dbpath', './data'],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
        print("✅ MongoDB started successfully")
        time.sleep(2)
        return True
    except Exception as e:
        print(f"⚠️  Could not start MongoDB: {e}")
        return False

def start_flask_app():
    """Start the Flask application"""
    print("\n" + "="*60)
    print("🚀 Starting Cafe Management Flask App")
    print("="*60)

    os.chdir(Path(__file__).parent)

    try:
        # Run Flask app
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n\n👋 Flask app stopped")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting Flask app: {e}")
        sys.exit(1)

def main():
    """Main setup and launcher"""
    print("\n" + "="*60)
    print("☕ Cafe Management Web Application - Auto Setup")
    print("="*60 + "\n")

    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    print("✅ Python version OK")

    # Check .env file
    if not Path('.env').exists():
        print("⚠️  .env file not found, creating from .env.example...")
        if Path('.env.example').exists():
            with open('.env.example', 'r') as f:
                env_content = f.read()
            with open('.env', 'w') as f:
                f.write(env_content)
            print("✅ .env created")
        else:
            print("❌ .env.example not found")
            sys.exit(1)
    else:
        print("✅ .env file exists")

    # Check MongoDB
    print("\n🔍 Checking MongoDB...")
    if not check_mongodb():
        install_mongodb_instructions()
        response = input("Have you installed MongoDB? (yes/no): ").lower()
        if response not in ['yes', 'y']:
            print("❌ MongoDB is required to run this application")
            sys.exit(1)

    # Try to start MongoDB
    print("\n🔄 Setting up database...")
    # Create data directory for local MongoDB
    data_dir = Path('./data')
    data_dir.mkdir(exist_ok=True)
    print("✅ Database directory ready")

    # Start Flask app
    print("\n✅ Setup complete! Launching application...\n")
    time.sleep(1)

    print("🌐 App will be available at: http://localhost:5000")
    print("📝 Press Ctrl+C to stop the application\n")

    # Open browser after a delay
    def open_browser():
        time.sleep(3)
        try:
            webbrowser.open('http://localhost:5000')
            print("🌐 Opening browser at http://localhost:5000")
        except:
            pass

    # Start browser opener in background
    import threading
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()

    # Start Flask app
    start_flask_app()

if __name__ == '__main__':
    main()
