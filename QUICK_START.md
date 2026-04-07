# 🚀 Quick Start Guide - Cafe Management App (MongoDB)

## 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start MongoDB
```bash
mongod
```

Or use MongoDB Atlas (cloud) - no setup needed!

### 3. Configure Environment
```bash
cp .env.example .env
# Default .env already has: MONGODB_URI=mongodb://localhost:27017/cafe_db
# For Atlas, update the MONGODB_URI
```

### 4. Run Application
```bash
python app.py
```

### 5. Open in Browser
```
http://localhost:5000
```

---

## Database Credentials (MongoDB Local)

```
Host:     localhost
Port:     27017
Database: cafe_db
```

No username/password needed for local MongoDB by default.

---

## Files Created/Modified

### ✅ Core Application
- `app.py` - Flask backend with CRUD routes and MongoEngine ODM

### ✅ Templates (Jinja2)
- `templates/base.html` - Base layout with navbar and flash messages
- `templates/navbar.html` - Navigation bar component
- `templates/index.html` - Display all items in table
- `templates/add_item.html` - Add new item form
- `templates/edit_item.html` - Edit existing item form

### ✅ Styling
- `static/style.css` - Complete CSS with responsive design

### ✅ Configuration
- `requirements.txt` - Python dependencies (updated for MongoDB)
- `.env.example` - Environment variables template (updated)
- `ENV_SETUP.md` - MongoDB setup guide (updated)
- `README.md` - Complete documentation (updated)

---

## Database Schema

MongoDB Collection: `items`

```json
{
  "_id": ObjectId("..."),
  "name": "Cappuccino",
  "price": 150
}
```

---

## CRUD Routes

| Operation | Route | Method |
|-----------|-------|--------|
| **C**reate | `/add` | GET & POST |
| **R**ead | `/` | GET |
| **U**pdate | `/edit/<id>` | GET & POST |
| **D**elete | `/delete/<id>` | GET |

---

## Features

✅ Database: MongoDB with MongoEngine ODM
✅ Models: Item (name, price)
✅ CRUD: All 4 operations fully implemented
✅ Templates: Inheritance with base.html and navbar
✅ Forms: Add and Edit item forms with validation
✅ Styling: Responsive CSS with modern design
✅ Messages: Flash messages for success/error

---

## Environment Variables (.env)

```
FLASK_ENV=development
PORT=5000
SECRET_KEY=dev-secret-key-change-in-production
MONGODB_URI=mongodb://localhost:27017/cafe_db
```

### For MongoDB Atlas (Production):
```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/cafe_db
```

---

## Project Structure

```
Cafe/
├── app.py
├── requirements.txt
├── .env.example
├── ENV_SETUP.md
├── README.md
├── QUICK_START.md
├── IMPLEMENTATION_SUMMARY.md
├── DEPLOYMENT.md
├── templates/
│   ├── base.html
│   ├── navbar.html
│   ├── index.html
│   ├── add_item.html
│   └── edit_item.html
└── static/
    └── style.css
```

---

## Common Commands

```bash
# Start MongoDB
mongod

# Start app
python app.py

# Connect to MongoDB shell
mongosh

# View all items
db.items.find()

# Count items
db.items.countDocuments()

# Delete all items
db.items.deleteMany({})

# Backup
mongodump --db cafe_db --out ./backup

# Restore
mongorestore --db cafe_db ./backup/cafe_db
```

---

## Troubleshooting

### MongoDB Connection Error
```bash
# Check if MongoDB is running
mongosh

# Verify .env MONGODB_URI is correct
cat .env | grep MONGODB_URI
```

### Port Already in Use
```bash
python -c "from app import app; app.run(port=5001)"
```

### Clear MongoDB Data
```bash
mongosh
use cafe_db
db.items.deleteMany({})
exit
```

---

## Testing

1. **Add Item**: Navigate to `/add`, add "Cappuccino" for 150
2. **View**: On home page (`/`), see the item in the table
3. **Edit**: Click Edit, change price to 160
4. **Delete**: Click Delete, confirm

✅ All operations successful!

---

## Production Deployment

For MongoDB Atlas + Render:
1. Create MongoDB Atlas cluster
2. Get connection string
3. Push code to GitHub
4. Create Render Web Service
5. Set MONGODB_URI environment variable
6. Deploy

See `DEPLOYMENT.md` for detailed instructions.

---

## Support

- **Setup Issues**: Check `ENV_SETUP.md`
- **Features**: See `README.md`
- **What Was Built**: View `IMPLEMENTATION_SUMMARY.md`
- **Deployment**: Follow `DEPLOYMENT.md`

---

**Built with Python Flask + MongoDB + Jinja2**
**Ready to Use! 🎉**
