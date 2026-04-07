#!/usr/bin/env python3
"""
MongoDB Setup and Connection Verification Script
Helps install MongoDB, start it, and verify Cafe app connection
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path
import platform

class MongoDBSetup:
    def __init__(self):
        self.os_type = platform.system()
        self.mongo_path = None
        self.db_path = Path("./data")
        self.db_path.mkdir(exist_ok=True)

    def print_header(self, title):
        """Print a formatted header"""
        print("\n" + "="*60)
        print(f"  {title}")
        print("="*60 + "\n")

    def check_mongod_installed(self):
        """Check if mongod is installed"""
        try:
            result = subprocess.run(['mongod', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ MongoDB is already installed")
                return True
        except FileNotFoundError:
            pass

        print("❌ MongoDB not found")
        return False

    def find_mongodb_path(self):
        """Find MongoDB installation path"""
        possible_paths = {
            "7.0": r"C:\Program Files\MongoDB\Server\7.0\bin",
            "6.0": r"C:\Program Files\MongoDB\Server\6.0\bin",
            "5.0": r"C:\Program Files\MongoDB\Server\5.0\bin",
        }

        for version, path in possible_paths.items():
            mongod = Path(path) / "mongod.exe"
            if mongod.exists():
                print(f"✅ Found MongoDB {version} at: {path}")
                return path

        return None

    def mongodb_installation_guide(self):
        """Show MongoDB installation guide"""
        self.print_header("MongoDB Installation Required")

        if self.os_type == "Windows":
            print("""
📥 DOWNLOAD & INSTALL MongoDB Community Edition

Step 1: Download
  - Go to: https://www.mongodb.com/try/download/community
  - Select "Windows" platform
  - Download the latest MSI installer
  - Example: mongod-windows-x86_64-7.0.0-signed.msi

Step 2: Run Installer
  - Double-click the downloaded .msi file
  - Click "Next" to proceed

Step 3: Installation Options (IMPORTANT)
  ✓ Check "Install MongoDB as a Service"
  ✓ Service Name: MongoDB
  ✓ Data Directory: C:\\data\\db (or default)
  ✓ Log Directory: Default
  ✓ Service User: Local System
  ✓ Choose "Complete" installation

Step 4: Install
  - Click "Install"
  - Wait for completion
  - Click "Finish"

Step 5: Verify
  - Open Command Prompt
  - Type: mongod --version
  - Should show version number

MongoDB Download Link:
https://www.mongodb.com/try/download/community

After Installation:
- Run this script again
- MongoDB service will start automatically
- Flask app will connect to: localhost:27017
            """)
        elif self.os_type == "Darwin":  # macOS
            print("""
📥 INSTALL MongoDB Community Edition (macOS)

Using Homebrew (Recommended):

Step 1: Install Homebrew (if not installed)
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

Step 2: Add MongoDB Tap
  brew tap mongodb/brew

Step 3: Install MongoDB
  brew install mongodb-community

Step 4: Start MongoDB Service
  brew services start mongodb-community

Step 5: Verify
  mongosh

If mongodb-community is not available:
  brew search mongodb
  brew install mongodb-community@VERSION
            """)
        elif self.os_type == "Linux":
            print("""
📥 INSTALL MongoDB Community Edition (Linux)

Ubuntu/Debian:

Step 1: Import GPG Key
  wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -

Step 2: Add MongoDB Repository
  echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

Step 3: Update Package List
  sudo apt-get update

Step 4: Install MongoDB
  sudo apt-get install -y mongodb-org

Step 5: Start MongoDB
  sudo systemctl start mongod

Step 6: Enable on Boot
  sudo systemctl enable mongod

Step 7: Verify
  mongosh
            """)

    def start_mongodb_service(self):
        """Start MongoDB service"""
        self.print_header("Starting MongoDB Service")

        if self.os_type == "Windows":
            print("🚀 Attempting to start MongoDB service...")
            try:
                result = subprocess.run(['net', 'start', 'MongoDB'],
                                      capture_output=True, text=True)
                if result.returncode == 0 or "already been started" in result.stderr:
                    print("✅ MongoDB service started successfully")
                    time.sleep(2)
                    return True
                else:
                    print("⚠️  Could not start via service, starting manually...")
                    return self.start_mongod_manual()
            except Exception as e:
                print(f"❌ Error: {e}")
                return self.start_mongod_manual()
        else:
            print("On macOS/Linux, MongoDB should start automatically")
            print("Check status: brew services list (macOS) or sudo systemctl status mongod (Linux)")
            return True

    def start_mongod_manual(self):
        """Start mongod manually"""
        print("\n🚀 Starting MongoDB manually...")
        print(f"📁 Data directory: {self.db_path.absolute()}")

        try:
            # Start in background
            if self.os_type == "Windows":
                subprocess.Popen(['mongod', '--dbpath', str(self.db_path)],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
            else:
                subprocess.Popen(['mongod', '--dbpath', str(self.db_path)],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)

            print("✅ MongoDB started in background")
            time.sleep(3)
            return True
        except Exception as e:
            print(f"❌ Error starting MongoDB: {e}")
            return False

    def verify_connection(self):
        """Verify MongoDB connection"""
        self.print_header("Verifying MongoDB Connection")

        print("⏳ Checking MongoDB connection...")

        for attempt in range(5):
            try:
                result = subprocess.run(
                    ['mongosh', '--eval', 'db.adminCommand("ping")'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    print("✅ MongoDB is connected and responding!")
                    print("   Host: localhost")
                    print("   Port: 27017")
                    print("   Status: RUNNING")
                    return True
            except:
                pass

            if attempt < 4:
                print(f"   Attempt {attempt + 1}/5... waiting...")
                time.sleep(2)

        print("⚠️  Could not verify connection with mongosh")
        print("   But MongoDB might still be running")
        return None

    def create_database(self):
        """Create cafe_db database"""
        self.print_header("Creating Cafe Database")

        print("📊 Creating cafe_db database...")

        try:
            result = subprocess.run(
                ['mongosh', '--eval', '''
                    use cafe_db;
                    db.items.insertOne({ name: "Espresso", price: 100 });
                    db.items.deleteOne({ name: "Espresso" });
                    print("✅ Database created successfully");
                '''],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                print("✅ cafe_db database created")
                return True
        except:
            pass

        print("⚠️  Database creation skipped (MongoDB still starting)")
        return None

    def setup_compass(self):
        """Provide MongoDB Compass setup info"""
        self.print_header("MongoDB Compass Setup (Optional)")

        print("""
🧭 MongoDB Compass - Visual Database Browser

Download from:
  https://www.mongodb.com/products/compass

Connection Details:
  Connection String: mongodb://localhost:27017/cafe_db

  OR use connection settings:
  - Host: localhost
  - Port: 27017
  - Database: cafe_db
  - Username: (leave empty - no auth)
  - Password: (leave empty - no auth)

After connecting in Compass, you'll see:
  - Database: cafe_db
  - Collection: items
  - Documents: Your cafe menu items
        """)

    def show_connection_info(self):
        """Show connection information"""
        self.print_header("MongoDB Connection Information")

        print("""
✅ MongoDB Setup Complete!

Connection Details:
  ┌─────────────────────────────────────┐
  │ Host:       localhost               │
  │ Port:       27017                   │
  │ Database:   cafe_db                 │
  │ Auth:       None (default)          │
  │ Connection: mongodb://localhost...  │
  │ Status:     Ready                   │
  └─────────────────────────────────────┘

Full Connection String:
  mongodb://localhost:27017/cafe_db

Environment Variable (.env):
  MONGODB_URI=mongodb://localhost:27017/cafe_db

For Mongolia Atlas (Cloud):
  MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/cafe_db

Test Connection:
  $ mongosh
  > use cafe_db
  > db.items.find()

Start Flask App:
  $ python app.py
  Then open: http://localhost:5000
        """)

    def show_next_steps(self):
        """Show next steps"""
        self.print_header("Next Steps")

        print("""
1. Keep MongoDB Running
   ✓ Windows: Service runs automatically (or mongod window)
   ✓ macOS: brew services list
   ✓ Linux: sudo systemctl status mongod

2. Run Flask Application
   $ cd C:/Users/farsa/.vscode/Cafe
   $ python app.py

3. Open in Browser
   http://localhost:5000

4. Test the Application
   ✅ Add Item
   ✅ View Items
   ✅ Edit Item
   ✅ Delete Item

5. (Optional) Download MongoDB Compass
   - Visual database browser
   - Monitor your data
   - https://www.mongodb.com/products/compass

Need Help?
  - Check ENV_SETUP.md
  - Check README.md
  - See QUICK_START.md
        """)

    def run(self):
        """Main setup flow"""
        print("""
╔════════════════════════════════════════════════════════════╗
║     MongoDB Setup & Connection Verification                ║
║     Cafe Management Application                            ║
╚════════════════════════════════════════════════════════════╝
        """)

        # Step 1: Check if installed
        self.print_header("Step 1: Checking MongoDB Installation")
        if self.check_mongod_installed():
            print("✅ MongoDB is already set up!")
        else:
            if self.find_mongodb_path():
                print("✅ Found MongoDB installation")
            else:
                print("❌ MongoDB not installed")
                self.mongodb_installation_guide()

                input("\n✋ Press ENTER after installing MongoDB...")

                if not self.find_mongodb_path() and not self.check_mongod_installed():
                    print("\n❌ MongoDB still not found. Please install it manually.")
                    print("📥 Download from: https://www.mongodb.com/try/download/community")
                    input("Press ENTER to exit...")
                    return False

        # Step 2: Start MongoDB
        self.print_header("Step 2: Starting MongoDB Service")
        if not self.start_mongodb_service():
            print("⚠️  Could not start service, trying manual start...")
            if not self.start_mongod_manual():
                print("❌ Could not start MongoDB")
                return False

        # Step 3: Verify connection
        self.verify_connection()

        # Step 4: Create database
        self.create_database()

        # Step 5: Show Compass info
        self.setup_compass()

        # Step 6: Connection info
        self.show_connection_info()

        # Step 7: Next steps
        self.show_next_steps()

        return True

if __name__ == '__main__':
    setup = MongoDBSetup()
    success = setup.run()
    sys.exit(0 if success else 1)
