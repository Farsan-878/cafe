import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mongoengine import MongoEngine
from mongoengine import Document, StringField, IntField, ValidationError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# MongoDB Configuration
mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/cafe_db')
app.config['MONGODB_SETTINGS'] = {
    'host': mongodb_uri
}

db = MongoEngine(app)

# Database Model
class Item(Document):
    name = StringField(required=True, min_length=1, max_length=100)
    price = IntField(required=True, min_value=1)

    meta = {
        'collection': 'items'
    }

    def __repr__(self):
        return f'<Item {self.id}: {self.name}>'

# Initialize database
def init_db():
    pass  # MongoEngine doesn't require explicit initialization

# Routes
@app.route('/')
def index():
    """Display all items"""
    try:
        items = Item.objects.all()
        return render_template('index.html', items=items)
    except Exception as e:
        flash(f'Error loading items: {str(e)}', 'danger')
        return render_template('index.html', items=[])

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    """Add new item"""
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            price = request.form.get('price', '').strip()

            if not name:
                flash('Item name is required', 'warning')
                return redirect(url_for('add_item'))

            if not price:
                flash('Price is required', 'warning')
                return redirect(url_for('add_item'))

            try:
                price = int(price)
                if price <= 0:
                    raise ValueError('Price must be positive')
            except ValueError:
                flash('Price must be a positive number', 'warning')
                return redirect(url_for('add_item'))

            new_item = Item(name=name, price=price)
            new_item.save()
            flash(f'Item "{name}" added successfully!', 'success')
            return redirect(url_for('index'))

        except ValidationError as e:
            flash(f'Validation error: {str(e)}', 'danger')
            return redirect(url_for('add_item'))
        except Exception as e:
            flash(f'Error adding item: {str(e)}', 'danger')
            return redirect(url_for('add_item'))

    return render_template('add_item.html')

@app.route('/edit/<item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    """Edit item"""
    try:
        item = Item.objects.get(id=item_id)
    except Exception:
        flash('Item not found', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            price = request.form.get('price', '').strip()

            if not name:
                flash('Item name is required', 'warning')
                return redirect(url_for('edit_item', item_id=item_id))

            if not price:
                flash('Price is required', 'warning')
                return redirect(url_for('edit_item', item_id=item_id))

            try:
                price = int(price)
                if price <= 0:
                    raise ValueError('Price must be positive')
            except ValueError:
                flash('Price must be a positive number', 'warning')
                return redirect(url_for('edit_item', item_id=item_id))

            item.name = name
            item.price = price
            item.save()
            flash(f'Item "{name}" updated successfully!', 'success')
            return redirect(url_for('index'))

        except ValidationError as e:
            flash(f'Validation error: {str(e)}', 'danger')
            return redirect(url_for('edit_item', item_id=item_id))
        except Exception as e:
            flash(f'Error updating item: {str(e)}', 'danger')
            return redirect(url_for('edit_item', item_id=item_id))

    return render_template('edit_item.html', item=item)

@app.route('/delete/<item_id>')
def delete_item(item_id):
    """Delete item"""
    try:
        item = Item.objects.get(id=item_id)
        item_name = item.name
        item.delete()
        flash(f'Item "{item_name}" deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting item: {str(e)}', 'danger')

    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    flash('Item not found', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('FLASK_ENV', 'development') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
