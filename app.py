import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mongoengine import MongoEngine
from mongoengine import Document, StringField, IntField, ValidationError, ListField, DictField, DateTimeField, ReferenceField
from dotenv import load_dotenv
from datetime import datetime

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

# Database Models
class Staff(Document):
    name = StringField(required=True, min_length=1, max_length=100)
    phone = StringField(required=True, min_length=10, max_length=15)
    email = StringField(required=True, min_length=5, max_length=100)
    position = StringField(required=True, choices=['Service Boy', 'Chef', 'Manager', 'Cashier'])
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'staff'
    }

    def __repr__(self):
        return f'<Staff {self.id}: {self.name}>'


class Item(Document):
    name = StringField(required=True, min_length=1, max_length=100)
    price = IntField(required=True, min_value=1)

    meta = {
        'collection': 'items'
    }

    def __repr__(self):
        return f'<Item {self.id}: {self.name}>'


class Order(Document):
    order_id = StringField(required=True, unique=True)
    items = ListField(DictField())  # [{item_id, item_name, quantity, price}, ...]
    total_price = IntField(required=True)
    status = StringField(required=True, choices=['Pending', 'In Progress', 'Ready', 'Completed', 'Cancelled'], default='Pending')
    service_boy_id = ReferenceField(Staff, allow_null=True)
    table_number = IntField(min_value=1)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'orders'
    }

    def __repr__(self):
        return f'<Order {self.order_id}>'

# Initialize database
def init_db():
    pass  # MongoEngine doesn't require explicit initialization

# Menu Item Routes
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

# Staff Management Routes
@app.route('/staff')
def staff_list():
    """Display all staff members"""
    try:
        staff = Staff.objects.all()
        return render_template('staff_list.html', staff=staff)
    except Exception as e:
        flash(f'Error loading staff: {str(e)}', 'danger')
        return render_template('staff_list.html', staff=[])

@app.route('/staff/add', methods=['GET', 'POST'])
def add_staff():
    """Add new staff member"""
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            phone = request.form.get('phone', '').strip()
            email = request.form.get('email', '').strip()
            position = request.form.get('position', '').strip()

            if not all([name, phone, email, position]):
                flash('All fields are required', 'warning')
                return redirect(url_for('add_staff'))

            new_staff = Staff(name=name, phone=phone, email=email, position=position)
            new_staff.save()
            flash(f'Staff member "{name}" added successfully!', 'success')
            return redirect(url_for('staff_list'))

        except ValidationError as e:
            flash(f'Validation error: {str(e)}', 'danger')
            return redirect(url_for('add_staff'))
        except Exception as e:
            flash(f'Error adding staff: {str(e)}', 'danger')
            return redirect(url_for('add_staff'))

    positions = ['Service Boy', 'Chef', 'Manager', 'Cashier']
    return render_template('add_staff.html', positions=positions)

@app.route('/staff/edit/<staff_id>', methods=['GET', 'POST'])
def edit_staff(staff_id):
    """Edit staff member"""
    try:
        staff_member = Staff.objects.get(id=staff_id)
    except Exception:
        flash('Staff member not found', 'danger')
        return redirect(url_for('staff_list'))

    if request.method == 'POST':
        try:
            staff_member.name = request.form.get('name', '').strip()
            staff_member.phone = request.form.get('phone', '').strip()
            staff_member.email = request.form.get('email', '').strip()
            staff_member.position = request.form.get('position', '').strip()
            staff_member.save()
            flash('Staff member updated successfully!', 'success')
            return redirect(url_for('staff_list'))
        except Exception as e:
            flash(f'Error updating staff: {str(e)}', 'danger')
            return redirect(url_for('edit_staff', staff_id=staff_id))

    positions = ['Service Boy', 'Chef', 'Manager', 'Cashier']
    return render_template('edit_staff.html', staff_member=staff_member, positions=positions)

@app.route('/staff/delete/<staff_id>')
def delete_staff(staff_id):
    """Delete staff member"""
    try:
        staff_member = Staff.objects.get(id=staff_id)
        name = staff_member.name
        staff_member.delete()
        flash(f'Staff member "{name}" deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting staff: {str(e)}', 'danger')

    return redirect(url_for('staff_list'))

# Order Management Routes
@app.route('/orders')
def orders_list():
    """Display all orders"""
    try:
        orders = Order.objects.all().order_by('-created_at')
        return render_template('orders_list.html', orders=orders)
    except Exception as e:
        flash(f'Error loading orders: {str(e)}', 'danger')
        return render_template('orders_list.html', orders=[])

@app.route('/orders/add', methods=['GET', 'POST'])
def add_order():
    """Add new order"""
    try:
        items = Item.objects.all()
        staff = Staff.objects.all()
    except Exception:
        flash('Error loading data', 'danger')
        return redirect(url_for('orders_list'))

    if request.method == 'POST':
        try:
            order_id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            table_number = int(request.form.get('table_number', 0))
            service_boy_id = request.form.get('service_boy_id', '')

            # Parse items from form
            items_list = []
            total_price = 0
            item_ids = request.form.getlist('item_id')
            quantities = request.form.getlist('quantity')

            for item_id, quantity in zip(item_ids, quantities):
                if item_id and quantity:
                    item = Item.objects.get(id=item_id)
                    qty = int(quantity)
                    price = item.price * qty
                    total_price += price
                    items_list.append({
                        'item_id': str(item.id),
                        'item_name': item.name,
                        'quantity': qty,
                        'price': item.price
                    })

            if not items_list:
                flash('Please add at least one item to the order', 'warning')
                return redirect(url_for('add_order'))

            new_order = Order(
                order_id=order_id,
                items=items_list,
                total_price=total_price,
                table_number=table_number if table_number > 0 else None,
                service_boy_id=service_boy_id if service_boy_id else None
            )
            new_order.save()
            flash(f'Order "{order_id}" created successfully!', 'success')
            return redirect(url_for('orders_list'))

        except Exception as e:
            flash(f'Error creating order: {str(e)}', 'danger')
            return redirect(url_for('add_order'))

    return render_template('add_order.html', items=items, staff=staff)

@app.route('/orders/edit/<order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    """Edit order"""
    try:
        order = Order.objects.get(id=order_id)
        staff = Staff.objects.all()
    except Exception:
        flash('Order not found', 'danger')
        return redirect(url_for('orders_list'))

    if request.method == 'POST':
        try:
            order.status = request.form.get('status', 'Pending')
            order.table_number = int(request.form.get('table_number', 0)) or None
            service_boy_id = request.form.get('service_boy_id', '')
            order.service_boy_id = service_boy_id if service_boy_id else None
            order.save()
            flash('Order updated successfully!', 'success')
            return redirect(url_for('orders_list'))
        except Exception as e:
            flash(f'Error updating order: {str(e)}', 'danger')
            return redirect(url_for('edit_order', order_id=order_id))

    statuses = ['Pending', 'In Progress', 'Ready', 'Completed', 'Cancelled']
    return render_template('edit_order.html', order=order, staff=staff, statuses=statuses)

@app.route('/orders/delete/<order_id>')
def delete_order(order_id):
    """Delete order"""
    try:
        order = Order.objects.get(id=order_id)
        order_num = order.order_id
        order.delete()
        flash(f'Order "{order_num}" deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting order: {str(e)}', 'danger')

    return redirect(url_for('orders_list'))

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
