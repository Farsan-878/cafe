#!/usr/bin/env python3
"""
MongoDB Connection Fix - Choose and Configure
Helps users quickly setup MongoDB Atlas or Local MongoDB
"""

import os
import sys

def print_header(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def option_atlas():
    """MongoDB Atlas (Cloud) setup"""
    print_header("Option 1: MongoDB Atlas (Cloud) - RECOMMENDED")

    print("""
✅ Advantages:
  - No installation needed
  - Free tier available
  - Hosted in cloud
  - Automatic backups
  - Easy to scale

⏱️  Setup Time: 5 minutes

STEPS:

1. Go to: https://www.mongodb.com/cloud/atlas

2. Click "Start free" and create account

3. Create M0 (Free) cluster

4. Add Database User:
   - Username: cafe_user
   - Password: YourStrongPassword123!

5. Whitelist IP:
   - Choose "Allow Access from Anywhere"

6. Get Connection String:
   https://www.mongodb.com/cloud/atlas
   → Your cluster → Connect → Connection string

7. Copy the connection string (starts with mongodb+srv://)

8. Update .env file:
   """)

    print("   MONGODB_URI=mongodb+srv://cafe_user:PASSWORD@cluster.mongodb.net/cafe_db?retryWrites=true&w=majority")

    print("""
9. Save .env file

10. Run: python app.py

✅ Done! Your app is now using MongoDB Atlas!
    """)

def option_local():
    """Local MongoDB setup"""
    print_header("Option 2: Local MongoDB Installation")

    print("""
✅ Advantages:
  - No cloud account needed
  - Full local control
  - Works offline
  - Good for development

⏱️  Setup Time: 10 minutes

STEPS:

1. Download MongoDB Community:
   https://www.mongodb.com/try/download/community
   → Select Windows
   → Download MSI installer

2. Run the installer (.msi file)
   → Click Next
   → ✓ Check "Install MongoDB as a Service"
   → Finish

3. MongoDB will auto-start after installation

4. Verify installation:
   Open Command Prompt: mongod --version
   Should show version number

5. Create data directory:
   mkdir C:\\data\\db

6. Update .env file:
   """)

    print("   MONGODB_URI=mongodb://localhost:27017/cafe_db")

    print("""
7. Save .env file

8. Run: python app.py

✅ Done! Using local MongoDB!

TROUBLESHOOTING:
- Check MongoDB running: tasklist | find "mongod"
- Start service: net start MongoDB
- Check connection: mongosh
    """)

def option_both():
    """Show both options"""
    option_atlas()
    input("\n[ Press ENTER to see local installation option... ]")
    option_local()

def main():
    print_header("MongoDB Setup Helper")

    print("""
Your app needs MongoDB to run!

Choose your setup method:
""")

    print("1️⃣  MongoDB Atlas (Cloud) - ⭐ RECOMMENDED")
    print("   - Easiest to setup")
    print("   - Free forever")
    print("   - No local installation")
    print("")
    print("2️⃣  Local MongoDB")
    print("   - Full control")
    print("   - Works offline")
    print("   - Download and install")
    print("")
    print("3️⃣  View both options")
    print("")

    choice = input("Choose (1, 2, or 3): ").strip()

    if choice == "1":
        option_atlas()
    elif choice == "2":
        option_local()
    elif choice == "3":
        option_both()
    else:
        print("❌ Invalid choice!")
        sys.exit(1)

    print("\n" + "="*60)
    print("  NEXT STEPS")
    print("="*60)
    print("""
After setting up MongoDB:

1. Edit .env file with your connection string

2. Run the app:
   python app.py

3. Open in browser:
   http://localhost:5000

4. Test CRUD operations:
   ✓ Add Item
   ✓ View Items
   ✓ Edit Item
   ✓ Delete Item

Need help? Check:
- MONGODB_ATLAS_SETUP.md
- MONGODB_LOCAL_INSTALL.md
- ENV_SETUP.md
    """)

if __name__ == "__main__":
    main()
