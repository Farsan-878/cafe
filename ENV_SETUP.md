# Cafe Management System - MongoDB Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment
```bash
cp .env.example .env
# Edit .env with your MongoDB URI
```

### 3. Start MongoDB
**Windows (with MongoDB installed):**
```bash
mongod
```

**macOS (with Homebrew):**
```bash
brew services start mongodb-community
```

**Linux (Ubuntu/Debian):**
```bash
sudo systemctl start mongod
```

Or use **MongoDB Atlas** (cloud):
```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/cafe_db
```

### 4. Run Application
```bash
python app.py
```

Open: `http://localhost:5000`

---

## Environment Variables

### Local Development (.env)
```
FLASK_ENV=development
PORT=5000
SECRET_KEY=dev-secret-key-change-in-production
MONGODB_URI=mongodb://localhost:27017/cafe_db
```

### Production (.env.production)
```
FLASK_ENV=production
PORT=8000
SECRET_KEY=<generate-a-random-secret-key>
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/cafe_db
```

---

## MongoDB Setup

### Option 1: Local MongoDB Installation

**Windows:**
1. Download from https://www.mongodb.com/try/download/community
2. Run installer
3. Choose "Install MongoDB as a Service"
4. Start: `mongod`

**macOS:**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install -y mongodb
sudo systemctl start mongod
```

### Option 2: MongoDB Atlas (Cloud) - Recommended for Production

1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up (free tier available)
3. Create a cluster
4. Get connection string:
   ```
   mongodb+srv://username:password@cluster.mongodb.net/cafe_db
   ```
5. Add to `.env`:
   ```
   MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/cafe_db
   ```

---

## MongoDB Connection URIs

### Local Development
```
mongodb://localhost:27017/cafe_db
```

### MongoDB Atlas (Cloud)
```
mongodb+srv://username:password@cluster.mongodb.net/cafe_db
```

### Remote MongoDB Server
```
mongodb://username:password@hostname:27017/cafe_db
```

---

## Generate Secret Key

For production deployment:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output to your `.env` file.

---

## Running Locally

### First Time
```bash
pip install -r requirements.txt
python app.py
```

The app will:
- Connect to MongoDB automatically
- Create collections on first use
- Be available at `http://localhost:5000`

### Already Set Up
```bash
python app.py
```

---

## Test MongoDB Connection

### Check if MongoDB is running
```bash
mongosh
```

### List databases
```bash
show dbs
```

### Connect to cafe_db
```bash
use cafe_db
```

### View collections
```bash
show collections
```

### View items
```bash
db.items.find()
```

### Exit
```bash
exit
```

---

## Database Backup & Restore

### Backup
```bash
mongodump --db cafe_db --out ./backup
```

### Restore
```bash
mongorestore --db cafe_db ./backup/cafe_db
```

---

## Troubleshooting

### "Connection refused"
- MongoDB not running: Start mongod service
- Wrong host/port: Check MONGODB_URI
- MongoDB Atlas: Whitelist IP address in cluster settings

### "Database does not exist"
- MongoDB creates it automatically
- Just start the app and it will create cafe_db

### "Authentication failed" (MongoDB Atlas)
- Verify username and password
- Create database user in MongoDB Atlas dashboard
- Check IP whitelist settings

### "Cannot connect to MongoDB Atlas"
- IP whitelist: Add your IP to cluster security
- Connection string: Copy exact URI from Atlas
- Network: Check internet connection

### Flask can't connect to database
```bash
# Test connection directly
mongosh "mongodb://localhost:27017/cafe_db"
```

---

## MongoDB vs PostgreSQL

| Feature | MongoDB | PostgreSQL |
|---------|---------|-----------|
| Type | NoSQL (Document) | SQL (Relational) |
| Scaling | Horizontal | Vertical |
| Setup | Simpler | More complex |
| Cloud | MongoDB Atlas | Render, AWS RDS |
| Free Tier | Yes | Limited |
| Schema | Flexible | Strict |

---

## Production Deployment Checklist

- [ ] Generated secure SECRET_KEY
- [ ] MongoDB setup (Atlas or self-hosted)
- [ ] MONGODB_URI verified and working
- [ ] requirements.txt updated with all dependencies
- [ ] .env configured correctly
- [ ] Tested locally: `python app.py`
- [ ] Deployed to production
- [ ] Application running at production URL
- [ ] Database accessible from production
- [ ] CRUD operations working

---

## Common Commands

```bash
# Start MongoDB
mongod

# Connect to MongoDB shell
mongosh

# List all databases
show dbs

# Use specific database
use cafe_db

# Show all collections
show collections

# View all items
db.items.find()

# View pretty-printed items
db.items.find().pretty()

# Count items
db.items.countDocuments()

# Delete all items
db.items.deleteMany({})

# Run Flask app
python app.py

# Run with specific port
python -c "from app import app; app.run(port=8000)"
```

---

## Environment Variables Reference

| Variable | Purpose | Example |
|----------|---------|---------|
| `FLASK_ENV` | development or production | `development` |
| `PORT` | Application port | `5000` |
| `SECRET_KEY` | Session encryption key | `abc123...` |
| `MONGODB_URI` | MongoDB connection string | `mongodb://localhost:27017/cafe_db` |

---

## MongoDB Data Model

### Item Collection

```javascript
{
  _id: ObjectId("..."),
  name: "Cappuccino",
  price: 150
}
```

**Field Details:**
- `_id` - Auto-generated unique identifier
- `name` - String (required, max 100 chars)
- `price` - Integer (required, min 1)

---

## Performance Tips

1. **Indexes**: MongoDB creates indexes automatically on _id
2. **Connection Pooling**: MongoEngine handles this
3. **Batch Operations**: For adding many items, use bulk insert
4. **Query Optimization**: Use specific fields in queries

---

## Security Considerations

- **MongoDB Atlas**: Enable IP whitelist
- **Credentials**: Never commit .env file
- **Connection String**: Keep MONGODB_URI secret
- **Authentication**: Always use username/password
- **HTTPS**: Enable in production

---

## Next Steps

1. Install MongoDB (local or Atlas)
2. Update `.env` with MONGODB_URI
3. Run: `pip install -r requirements.txt`
4. Start: `python app.py`
5. Test at `http://localhost:5000`

---

**MongoDB Configuration Complete!**
Your app is now ready to use MongoDB as the database.
