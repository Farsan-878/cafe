# 🚀 MongoDB Atlas Setup (Cloud - 5 Minutes)

## Step 1: Create Free Account
1. Go to: https://www.mongodb.com/cloud/atlas
2. Click **"Start free"**
3. Fill in email, password, organization name
4. Click **Create account**
5. Verify email

## Step 2: Create Cluster
1. Click **"Create a Deployment"**
2. Select **"M0 Free"** tier
3. Choose cloud provider (AWS recommended)
4. Choose region closest to you
5. Click **Create Deployment**
6. Wait 2-3 minutes...

## Step 3: Create Database User
1. Go to **Database Access** (left menu)
2. Click **"Add New Database User"**
3. **Username**: cafe_user
4. **Password**: YourStrongPassword123!
5. Click **Add User**

## Step 4: Whitelist IP
1. Go to **Network Access** (left menu)
2. Click **"Add IP Address"**
3. Click **"Allow Access from Anywhere"** (for dev)
4. Click **Confirm**

## Step 5: Get Connection String
1. Go to **Databases** → Your cluster
2. Click **Connect**
3. Select **Drivers** → **Node.js**
4. Copy the connection string:
```
mongodb+srv://cafe_user:YourStrongPassword123@cluster.mongodb.net/cafe_db?retryWrites=true&w=majority
```

## Step 6: Update .env
Edit `c:\Users\farsa\.vscode\Cafe\.env`:
```
FLASK_ENV=development
PORT=5000
SECRET_KEY=dev-secret-key-change-in-production
MONGODB_URI=mongodb+srv://cafe_user:YourStrongPassword123@cluster.mongodb.net/cafe_db?retryWrites=true&w=majority
```

## Step 7: Run App
```bash
python app.py
```

Done! ✅ No local MongoDB needed!
