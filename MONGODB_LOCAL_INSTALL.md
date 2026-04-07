# 📦 Local MongoDB Installation (Windows)

## Quick Setup (3 Steps)

### Step 1: Download
1. Go to: https://www.mongodb.com/try/download/community
2. Select **Windows** platform
3. Download the **MSI installer** (latest version)
4. File will be: `mongod-windows-x86_64-*.msi`

### Step 2: Install
1. Double-click the `.msi` file
2. Click **Next** through the installer
3. **IMPORTANT**: Check ✓ "Install MongoDB as a Service"
4. Finish installation
5. MongoDB will auto-start!

### Step 3: Verify
Open Command Prompt and run:
```bash
mongod --version
```
Should show version number like: `db version v7.0.0`

---

## Create Data Directory

Create folder for MongoDB data:
```bash
mkdir C:\data\db
```

---

## Update .env

Edit `c:\Users\farsa\.vscode\Cafe\.env`:
```
FLASK_ENV=development
PORT=5000
SECRET_KEY=dev-secret-key-change-in-production
MONGODB_URI=mongodb://localhost:27017/cafe_db
```

---

## Start MongoDB Service

### Option A: Auto-Start (Already Running)
MongoDB service starts automatically after installation.

Check if running:
```bash
tasklist | find "mongod"
```

### Option B: Start Manually
```bash
mongod --dbpath C:\data\db
```

Or start service:
```bash
net start MongoDB
```

---

## Test Connection

Open new Command Prompt:
```bash
mongosh
```

Should connect and show: `cafe_db>`

Type `exit` to quit.

---

## Run Flask App

```bash
python app.py
```

Should show:
```
Running on http://127.0.0.1:5000
WARNING: This is a development server. Do not use it in production.
```

---

## Troubleshooting

### "Port 27017 already in use"
```bash
# Find what's using port 27017
netstat -ano | findstr :27017

# Kill the process (replace PID with actual number)
taskkill /PID 1234 /F
```

### "mongod command not found"
- Reinstall MongoDB
- Ensure "Install as service" is checked
- Restart computer after installation

### "Cannot connect"
- Check if MongoDB is running: `tasklist | find "mongod"`
- Check .env file MONGODB_URI
- Check data directory exists: `C:\data\db`

---

## MongoDB Shell Commands

```bash
# Connect
mongosh

# Use cafe_db database
use cafe_db

# View all collections
show collections

# View items
db.items.find()

# Count items
db.items.countDocuments()

# Pretty print
db.items.find().pretty()

# Exit
exit
```

---

**Installation complete! Now run: `python app.py`**
