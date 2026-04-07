# Cafe Management Web Application - MongoDB Edition

A complete full-stack Cafe Management System built with **Python Flask**, **MongoDB**, and **Jinja2 Templates**.

## Features

✅ **CRUD Operations** for Menu Items
- **Create**: Add new items to the menu
- **Read**: Display all items in a table
- **Update**: Edit existing items
- **Delete**: Remove items from the menu

✅ **Database Integration**
- MongoDB NoSQL database with MongoEngine ODM
- Automatic collection creation
- Proper error handling and validation

✅ **User-Friendly Interface**
- Template inheritance with base.html
- Responsive navbar with navigation
- Success/error flash messages
- Clean, modern CSS styling

✅ **Data Validation**
- Item name validation
- Price validation (positive numbers)
- Error handling for database operations

## Project Structure

```
Cafe/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── .env.example             # Environment configuration template
├── templates/
│   ├── base.html            # Base layout with navbar
│   ├── navbar.html          # Navigation component
│   ├── index.html           # Display all items
│   ├── add_item.html        # Add new item form
│   └── edit_item.html       # Edit existing item form
└── static/
    └── style.css            # Styling (navbar, forms, table, etc.)
```

## Database Model

### Item Collection
| Field | Type | Description |
|-------|------|-------------|
| _id | ObjectId | Auto-generated unique identifier |
| name | String | Item name, required, max 100 chars |
| price | Integer | Price in rupees, required, min 1 |

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- MongoDB 4.0+ (local or MongoDB Atlas)
- pip (Python package manager)

### 2. Clone and Install

```bash
# Navigate to project directory
cd Cafe

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your MongoDB URI
# Local: mongodb://localhost:27017/cafe_db
# Atlas: mongodb+srv://username:password@cluster.mongodb.net/cafe_db
```

### 4. MongoDB Setup

**Local MongoDB:**
```bash
# Start MongoDB service
mongod
```

**MongoDB Atlas (Cloud):**
1. Go to https://www.mongodb.com/cloud/atlas
2. Create free account
3. Create a cluster
4. Get connection string
5. Update MONGODB_URI in .env

### 5. Run the Application

```bash
# Development mode
python app.py

# The app will be available at http://localhost:5000
```

## API Routes

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Display all menu items |
| GET | `/add` | Show add item form |
| POST | `/add` | Create new item |
| GET | `/edit/<id>` | Show edit item form |
| POST | `/edit/<id>` | Update item |
| GET | `/delete/<id>` | Delete item |

## Usage Examples

### Adding an Item
1. Click **"+ Add Item"** in the navbar
2. Enter item name (e.g., "Cappuccino")
3. Enter price in rupees (e.g., 150)
4. Click **"Add Item"**
5. Success message appears, redirected to home

### Editing an Item
1. Click **"Edit"** button next to an item
2. Modify the name or price
3. Click **"Update Item"**
4. Changes are saved

### Deleting an Item
1. Click **"Delete"** button next to an item
2. Confirm the deletion
3. Item is removed

## Configuration

### Environment Variables (.env)

```
FLASK_ENV=development          # development or production
PORT=5000                      # Port for Flask app
SECRET_KEY=your-secret-key     # Session secret (change in production)
MONGODB_URI=mongodb://...      # MongoDB connection URI
```

### MongoDB Connection String Format

**Local:**
```
mongodb://localhost:27017/cafe_db
```

**MongoDB Atlas:**
```
mongodb+srv://username:password@cluster.mongodb.net/cafe_db
```

**Remote:**
```
mongodb://username:password@hostname:27017/cafe_db
```

## Features Implemented

### ✅ Backend
- Flask framework with proper routing
- MongoEngine ODM for database operations
- Document model with proper validation
- Error handling with flash messages
- 404 error handling

### ✅ Frontend
- Template inheritance (base.html)
- Reusable navbar component
- Responsive table layout
- Form validation feedback
- Success/error alerts
- Mobile-responsive design

### ✅ Database
- MongoDB integration
- MongoEngine ODM
- Automatic collection creation
- Proper connection URI configuration

## Error Handling

The application includes:
- Item not found handling
- Form validation errors
- Database operation errors with try/catch
- User-friendly error messages

## Browser Compatibility

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Styling

- Modern cafe-themed color scheme
- Smooth transitions and hover effects
- Responsive design for all screen sizes
- Clean typography with Fraunces and Manrope fonts

## Security Considerations

- Form validation on both client and server
- XSS prevention through Jinja2 auto-escaping
- CSRF protection ready (can be enabled with Flask-WTF)
- Environment variables for sensitive data
- MongoDB injection prevention through MongoEngine

## Deployment

### MongoDB Atlas + Render

1. Create MongoDB Atlas account and cluster
2. Get connection string (MONGODB_URI)
3. Push code to GitHub
4. Connect repository to Render
5. Set environment variables in Render dashboard
6. Deploy

See `DEPLOYMENT.md` for detailed deployment instructions.

## Database Backup

To backup your MongoDB collection:

```bash
mongodump --db cafe_db --out ./backup
```

To restore:

```bash
mongorestore --db cafe_db ./backup/cafe_db
```

## Development Tips

- Enable debug mode in development:
  ```
  FLASK_ENV=development
  ```
- Use MongoDB shell for testing:
  ```bash
  mongosh
  ```
- Check logs in console for debugging
- Use `db.items.find().pretty()` to view data

## Common Issues

### Connection Refused
- Ensure MongoDB is running
- Check MONGODB_URI is correct
- Verify database access

### Import Errors
- Install dependencies: `pip install -r requirements.txt`
- Check Python version is 3.8+

### 404 Errors
- Ensure item ID exists
- Check URL format in templates

## MongoDB vs PostgreSQL

This app was converted from PostgreSQL to MongoDB for:
- **Flexibility**: Document-based schema
- **Scalability**: Horizontal scaling
- **Simplicity**: Easier setup and dev
- **Cost**: Free tier with MongoDB Atlas

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
1. Check the error message displayed
2. Review the logs in console
3. Verify environment configuration
4. Check MongoDB connection

---

**Built with ❤️ using Flask, MongoDB, and Jinja2**
