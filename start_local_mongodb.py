#!/usr/bin/env python3
"""
Cafe Management App - Local MongoDB Setup & Launcher
Handles MongoDB startup for Windows and runs Flask app
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path
import platform

class LocalMongoDBSetup:
    def __init__(self):
        self.os_type = platform.system()
        self.mongo_path = None
        self.data_dir = Path("C:/data/db") if self.os_type == "Windows" else Path("./data/db")

    def print_header(self, title):
        print("\n" + "="*60)
        print(f"  {title}")
        print("="*60 + "\n")

    def find_mongodb(self):
        """Find MongoDB installation on Windows"""
        if self.os_type != "Windows":
            return self._find_mongodb_unix()

        print("🔍 Searching for MongoDB installation...")

        # Common MongoDB installation paths
        search_paths = [
            r"C:\Program Files\MongoDB\Server",
            r"C:\Program Files (x86)\MongoDB\Server",
        ]

        for base_path in search_paths:
            if Path(base_path).exists():
                # Find the latest version
                versions = sorted(Path(base_path).glob("*"), reverse=True)
                for version_dir in versions:
                    mongod_exe = version_dir / "bin" / "mongod.exe"
                    if mongod_exe.exists():
                        self.mongo_path = str(mongod_exe)
                        print(f"✅ Found MongoDB: {version_dir}")
                        return True

        print("❌ MongoDB not found in standard locations")
        return False

    def _find_mongodb_unix(self):
        """Find MongoDB on Unix systems"""
        try:
            result = subprocess.run(['which', 'mongod'], capture_output=True, text=True)
            if result.returncode == 0:
                self.mongo_path = result.stdout.strip()
                print(f"✅ Found MongoDB: {self.mongo_path}")
                return True
        except:
            pass
        return False

    def check_mongodb_running(self):
        """Check if MongoDB is already running"""
        print("🔄 Checking if MongoDB is running...")

        if self.os_type == "Windows":
            result = subprocess.run(['tasklist'], capture_output=True, text=True)
            if "mongod.exe" in result.stdout:
                print("✅ MongoDB is already RUNNING")
                return True
        else:
            try:
                subprocess.run(['pgrep', 'mongod'], check=True, capture_output=True)
                print("✅ MongoDB is already RUNNING")
                return True
            except:
                pass

        return False

    def create_data_directory(self):
        """Create MongoDB data directory"""
        print(f"📁 Creating data directory: {self.data_dir}")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        print("✅ Data directory ready")

    def start_mongodb_service(self):
        """Start MongoDB service"""
        print("🚀 Starting MongoDB service...")

        if self.os_type == "Windows":
            # Try to start as service
            try:
                result = subprocess.run(['net', 'start', 'MongoDB'],
                                      capture_output=True, text=True)
                if result.returncode == 0 or "already been started" in result.stderr.lower():
                    print("✅ MongoDB service started")
                    time.sleep(2)
                    return True
            except:
                pass

            # Try manual start
            if self.mongo_path:
                print("   Starting mongod manually...")
                try:
                    subprocess.Popen([self.mongo_path, '--dbpath', str(self.data_dir)],
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)
                    print("✅ MongoDB started manually")
                    time.sleep(3)
                    return True
                except Exception as e:
                    print(f"❌ Failed to start MongoDB: {e}")
                    return False

        else:  # Unix
            try:
                subprocess.Popen(['mongod', '--dbpath', str(self.data_dir)],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
                print("✅ MongoDB started")
                time.sleep(3)
                return True
            except Exception as e:
                print(f"❌ Failed to start MongoDB: {e}")
                return False

        return False

    def check_connection(self):
        """Test MongoDB connection"""
        print("🔌 Testing MongoDB connection...")

        for attempt in range(5):
            try:
                result = subprocess.run(
                    ['mongosh', '--eval', 'db.adminCommand("ping")'] if self.os_type != "Windows" else
                    ['mongosh', '--eval', 'db.adminCommand("ping")'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    print("✅ MongoDB connection successful!")
                    return True
            except:
                pass

            if attempt < 4:
                print(f"   Attempt {attempt + 1}/5... waiting...")
                time.sleep(2)

        print("⚠️  Could not verify connection (MongoDB may still be starting)")
        return None

    def update_env_file(self):
        """Ensure .env is configured for local MongoDB"""
        print("📝 Checking .env configuration...")

        env_path = Path(".env")

        if not env_path.exists():
            print("   Creating .env from .env.example...")
            if Path(".env.example").exists():
                with open(".env.example", "r") as f:
                    content = f.read()
                # Replace with local MongoDB URI
                content = content.replace(
                    "mongodb+srv://",
                    "# mongodb+srv://"
                )
                if "MONGODB_URI=mongodb://localhost:27017/cafe_db" not in content:
                    content += "\nMONGODB_URI=mongodb://localhost:27017/cafe_db\n"

                with open(".env", "w") as f:
                    f.write(content)
                print("✅ .env created with local MongoDB configuration")
            else:
                print("❌ .env.example not found")
                return False
        else:
            print("✅ .env file exists")

        return True

    def show_connection_info(self):
        """Display connection information"""
        self.print_header("MongoDB Connection Information")

        print("""
✅ MongoDB is Ready!

Connection Details:
  ┌─────────────────────────────────────┐
  │ Host:       localhost               │
  │ Port:       27017                   │
  │ Database:   cafe_db                 │
  │ URI:        mongodb://localhost:... │
  │ Status:     Ready                   │
  └─────────────────────────────────────┘

Configuration:
  - MONGODB_URI=mongodb://localhost:27017/cafe_db
  - Located in: .env file

Test Connection:
  $ mongosh
  > use cafe_db
  > db.items.find()
  > exit
        """)

    def launch_flask_app(self):
        """Launch Flask application"""
        self.print_header("Starting Flask Application")

        print("🚀 Starting Cafe Management App...")
        print("")
        print("⏳ App starting...")
        print("   Wait for: 'Running on http://127.0.0.1:5000'")
        print("")

        def open_browser():
            time.sleep(3)
            try:
                webbrowser.open('http://localhost:5000')
                print("\n🌐 Opening browser at http://localhost:5000")
            except:
                pass

        # Start browser opener in background
        import threading
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()

        # Run Flask app
        try:
            subprocess.run([sys.executable, 'app.py'])
        except KeyboardInterrupt:
            print("\n\n👋 Application stopped")
            sys.exit(0)

    def run(self):
        """Main setup and launcher"""
        print("""
╔════════════════════════════════════════════════════════════╗
║     Cafe Management App - Local MongoDB Setup              ║
╚════════════════════════════════════════════════════════════╝
        """)

        self.print_header("Step 1: Finding MongoDB Installation")

        if not self.find_mongodb():
            print("""
❌ MongoDB not found!

Please install MongoDB Community Edition:
https://www.mongodb.com/try/download/community

Then run this script again.
            """)
            input("Press ENTER to exit...")
            return False

        self.print_header("Step 2: Checking MongoDB Status")

        if not self.check_mongodb_running():
            self.print_header("Step 3: Creating Data Directory")
            self.create_data_directory()

            self.print_header("Step 4: Starting MongoDB")
            if not self.start_mongodb_service():
                print("❌ Failed to start MongoDB")
                print("\nTroubleshooting:")
                print("1. Ensure MongoDB is installed correctly")
                print("2. Check that port 27017 is available")
                print("3. Restart your computer")
                input("Press ENTER to exit...")
                return False
        else:
            print("✅ Skipping startup (already running)")

        self.print_header("Step 5: Verifying Connection")
        self.check_connection()

        self.print_header("Step 6: Configuring Application")
        if not self.update_env_file():
            return False

        self.show_connection_info()

        self.print_header("Step 7: Launching Application")
        self.launch_flask_app()

        return True

if __name__ == '__main__':
    setup = LocalMongoDBSetup()
    success = setup.run()
    sys.exit(0 if success else 1)
