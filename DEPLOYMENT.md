# Deployment Guide: Cafe Management System

## Overview
- **Backend**: Flask API on Render
- **Frontend**: Static HTML/CSS/JS on Vercel
- **Database**: In-memory (can upgrade to PostgreSQL later)

---

## Step 1: Prepare Backend for Render

### 1.1 Create Gunicorn Configuration
Create `gunicorn_config.py` in the root directory:

```python
import os

workers = 4
worker_class = "sync"
bind = f"0.0.0.0:{os.getenv('PORT', 8000)}"
timeout = 120
```

### 1.2 Update requirements.txt
Add Gunicorn to your `requirements.txt`:

```
Flask>=3.0.0
Flask-Cors>=4.0.0
gunicorn>=21.0.0
```

Install locally: `pip install gunicorn`

### 1.3 Update app.py
Modify the last line in `app.py`:

```python
if __name__ == "__main__":
    import os
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### 1.4 Create Render configuration
Create `render.yaml` in root:

```yaml
services:
  - type: web
    name: cafe-backend
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11
```

---

## Step 2: Deploy Backend on Render

### 2.1 Push Changes to GitHub
```bash
git add requirements.txt app.py gunicorn_config.py render.yaml
git commit -m "Add deployment configuration for Render"
git push origin main
```

### 2.2 Deploy on Render
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click **"New +"** → **"Web Service"**
4. Select your GitHub repository: `Farsan-878/cafe`
5. Configure:
   - **Name**: `cafe-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free
6. Click **"Deploy"**

### 2.3 Get Your Backend URL
Once deployed, Render will provide a URL like:
```
https://cafe-backend.onrender.com
```
**Save this URL** - you'll need it for the frontend.

---

## Step 3: Prepare Frontend for Vercel

### 3.1 Extract Frontend Files
Since Vercel doesn't use Flask templating, we need to create a separate frontend:

1. Create a new directory structure:
```
frontend/
├── index.html
├── public/
│   ├── style.css
│   └── script.js
├── package.json
└── vercel.json
```

### 3.2 Update index.html (Remove Flask Template Syntax)
Create `frontend/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Cafe Management System</title>
    <link rel="stylesheet" href="./public/style.css" />
</head>
<body>
    <div class="page-shell">
        <header class="hero">
            <div>
                <p class="eyebrow">Cafe Management System</p>
                <h1>Run the cafe from one clean dashboard.</h1>
                <p class="hero-copy">
                    Manage the menu, place orders, assign service boys, track inventory, and collect customer reviews.
                </p>
            </div>
            <div class="hero-card">
                <h2>Live API Status</h2>
                <p>Backend: Flask + Flask-CORS</p>
                <p>Data: In-memory today, easy to move to SQLite later</p>
            </div>
        </header>

        <main class="dashboard-grid">
            <!-- Menu display and inventory -->
            <section class="panel wide-panel">
                <div class="panel-heading">
                    <div>
                        <p class="section-label">Menu display</p>
                        <h2>Available menu items</h2>
                    </div>
                    <button class="ghost-button" id="refreshMenuBtn" type="button">Refresh</button>
                </div>
                <div id="menuList" class="card-grid"></div>
                <div class="subpanel">
                    <div class="panel-heading compact">
                        <div>
                            <p class="section-label">Inventory</p>
                            <h3>Current stock</h3>
                        </div>
                    </div>
                    <div id="inventoryList" class="list-stack"></div>
                </div>
            </section>

            <!-- Add menu item -->
            <section class="panel">
                <div class="panel-heading">
                    <div>
                        <p class="section-label">Add menu item</p>
                        <h2>New item</h2>
                    </div>
                </div>
                <form id="menuForm" class="form-stack">
                    <label>
                        Item name
                        <input type="text" name="name" placeholder="Paneer wrap" required />
                    </label>
                    <label>
                        Price
                        <input type="number" name="price" min="0" step="0.01" placeholder="140" required />
                    </label>
                    <label>
                        Quantity
                        <input type="number" name="quantity" min="0" step="1" value="10" required />
                    </label>
                    <label class="checkbox-row">
                        <input type="checkbox" name="available" checked />
                        Available
                    </label>
                    <button class="primary-button" type="submit">Add Item</button>
                    <p class="message" id="menuMessage"></p>
                </form>
            </section>

            <!-- Place order -->
            <section class="panel wide-panel">
                <div class="panel-heading">
                    <div>
                        <p class="section-label">Place order</p>
                        <h2>Create a bill</h2>
                    </div>
                    <button class="ghost-button" id="addOrderRowBtn" type="button">Add Item Row</button>
                </div>
                <form id="orderForm" class="form-stack">
                    <label>
                        Service boy
                        <select id="serviceBoySelect" name="service_boy_name" required></select>
                    </label>
                    <div id="orderItems" class="order-items"></div>
                    <button class="primary-button" type="submit">Place Order</button>
                    <p class="message success-message" id="orderMessage"></p>
                </form>
            </section>

            <!-- Add staff -->
            <section class="panel">
                <div class="panel-heading">
                    <div>
                        <p class="section-label">Add staff</p>
                        <h2>Service boy</h2>
                    </div>
                </div>
                <form id="staffForm" class="form-stack">
                    <label>
                        Staff name
                        <input type="text" name="name" placeholder="Rahul" required />
                    </label>
                    <button class="primary-button" type="submit">Add Staff</button>
                    <p class="message" id="staffMessage"></p>
                </form>
            </section>

            <!-- Add review -->
            <section class="panel">
                <div class="panel-heading">
                    <div>
                        <p class="section-label">Add review</p>
                        <h2>Customer feedback</h2>
                    </div>
                </div>
                <form id="reviewForm" class="form-stack">
                    <label>
                        Rating
                        <select name="rating" required>
                            <option value="5">5 - Excellent</option>
                            <option value="4">4 - Good</option>
                            <option value="3">3 - Average</option>
                            <option value="2">2 - Fair</option>
                            <option value="1">1 - Poor</option>
                        </select>
                    </label>
                    <label>
                        Comment
                        <textarea name="comment" rows="4" placeholder="Write your review here" required></textarea>
                    </label>
                    <button class="primary-button" type="submit">Submit Review</button>
                    <p class="message" id="reviewMessage"></p>
                </form>
            </section>

            <!-- Show reviews -->
            <section class="panel wide-panel">
                <div class="panel-heading">
                    <div>
                        <p class="section-label">Show reviews</p>
                        <h2>What customers said</h2>
                    </div>
                    <button class="ghost-button" id="refreshReviewsBtn" type="button">Refresh</button>
                </div>
                <div id="reviewList" class="list-stack"></div>
            </section>
        </main>
    </div>

    <template id="orderRowTemplate">
        <div class="order-row">
            <select class="order-menu-select" required></select>
            <input class="order-quantity-input" type="number" min="1" step="1" value="1" required />
            <button class="icon-button remove-row-button" type="button">Remove</button>
        </div>
    </template>

    <script src="./public/script.js"></script>
</body>
</html>
```

### 3.3 Create frontend/public/script.js
Update the API base URL. Update `script.js` to use the backend URL:

```javascript
// Replace this at the top of script.js
const API_BASE_URL = "https://cafe-backend.onrender.com"; // Replace with your Render URL

// ... rest of the script stays the same
```

### 3.4 Copy Static Files
- Copy `static/style.css` → `frontend/public/style.css`
- Copy `static/script.js` → `frontend/public/script.js` and update API_BASE_URL

### 3.5 Create package.json
`frontend/package.json`:

```json
{
  "name": "cafe-frontend",
  "version": "1.0.0",
  "description": "Cafe Management System Frontend",
  "private": true
}
```

### 3.6 Create vercel.json
`frontend/vercel.json`:

```json
{
  "buildCommand": "echo 'Frontend ready'",
  "outputDirectory": "."
}
```

---

## Step 4: Deploy Frontend on Vercel

### 4.1 Create Frontend Directory and Push
```bash
# Create frontend directory with files
mkdir frontend
# Copy files as per Step 3
# Commit and push
git add frontend/
git commit -m "Add frontend for Vercel deployment"
git push origin main
```

### 4.2 Deploy on Vercel
1. Go to [vercel.com](https://vercel.com)
2. Sign in with GitHub
3. Click **"Add New"** → **"Project"**
4. Import repository `Farsan-878/cafe`
5. Configure:
   - **Root Directory**: `frontend`
   - **Build Command**: Leave empty (static site)
   - **Output Directory**: `.`
6. Click **"Deploy"**

### 4.3 Get Your Frontend URL
Vercel will provide a URL like:
```
https://cafe-frontend.vercel.app
```

---

## Step 5: Connect Frontend to Backend

### 5.1 Update Frontend API URL
In `frontend/public/script.js`, ensure the API URL is set to your Render backend:

```javascript
const API_BASE_URL = "https://cafe-backend.onrender.com";
```

### 5.2 Enable CORS in Backend
Your backend already has CORS enabled (`CORS(app)`), so no changes needed!

---

## Environment Variables (Optional Future)

If you need to add environment variables:

### Render Backend
1. Go to your Render service → **Settings**
2. Scroll to **Environment**
3. Add variables (e.g., `DATABASE_URL`, `SECRET_KEY`)

### Vercel Frontend
1. Go to your Vercel project → **Settings**
2. Click **"Environment Variables"**
3. Add variables (must start with `NEXT_PUBLIC_` if client-side)

---

## Testing Your Deployment

1. Visit your Vercel frontend URL
2. Try adding a menu item, staff member, order, or review
3. Check browser console (F12) for any errors
4. Verify API calls are reaching `https://cafe-backend.onrender.com/api/*`

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| CORS errors | Check that Flask backend has `CORS(app)` |
| 404 API errors | Verify `API_BASE_URL` is correct in script.js |
| Backend timeout | Render free tier may sleep after 15 min inactivity |
| Vercel blank page | Check that relative paths in HTML are correct |

---

## Next Steps

1. **Database**: Upgrade from in-memory to SQLite or PostgreSQL
2. **Authentication**: Add login system for staff
3. **Persistence**: Save data to database instead of memory
4. **Monitoring**: Set up error tracking (Sentry)
5. **Analytics**: Track user behavior

