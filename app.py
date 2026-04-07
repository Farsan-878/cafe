from dataclasses import dataclass, field
from datetime import datetime
from itertools import count
from typing import Dict, List, Optional

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@dataclass
class CafeStore:
    """Simple in-memory store that can later be replaced with a database layer."""

    menu_items: List[Dict] = field(default_factory=list)
    staff_members: List[Dict] = field(default_factory=list)
    reviews: List[Dict] = field(default_factory=list)
    orders: List[Dict] = field(default_factory=list)
    menu_id_counter: count = field(default_factory=lambda: count(1))
    staff_id_counter: count = field(default_factory=lambda: count(1))
    review_id_counter: count = field(default_factory=lambda: count(1))
    order_id_counter: count = field(default_factory=lambda: count(1))

    def add_menu_item(self, name: str, price: float, available: bool, quantity: int) -> Dict:
        menu_item = {
            "id": next(self.menu_id_counter),
            "name": name,
            "price": round(float(price), 2),
            "available": bool(available),
            "quantity": int(quantity),
        }
        self.menu_items.append(menu_item)
        return menu_item

    def add_staff_member(self, name: str) -> Dict:
        staff_member = {"id": next(self.staff_id_counter), "name": name}
        self.staff_members.append(staff_member)
        return staff_member

    def add_review(self, rating: int, comment: str) -> Dict:
        review = {
            "id": next(self.review_id_counter),
            "rating": int(rating),
            "comment": comment,
            "created_at": datetime.utcnow().isoformat() + "Z",
        }
        self.reviews.append(review)
        return review

    def place_order(self, service_boy_name: str, items: List[Dict]) -> Dict:
        if not service_boy_name:
            raise ValueError("Service boy name is required.")

        staff_names = {member["name"].lower() for member in self.staff_members}
        if service_boy_name.lower() not in staff_names:
            raise ValueError("Selected service boy is not registered.")

        order_items = []
        total_price = 0.0

        for requested_item in items:
            menu_item_id = int(requested_item.get("menu_item_id", 0))
            quantity = int(requested_item.get("quantity", 0))

            if quantity <= 0:
                raise ValueError("Order quantity must be at least 1 for each item.")

            menu_item = next((item for item in self.menu_items if item["id"] == menu_item_id), None)
            if menu_item is None:
                raise ValueError(f"Menu item with id {menu_item_id} not found.")

            if not menu_item["available"]:
                raise ValueError(f"{menu_item['name']} is currently unavailable.")

            if menu_item["quantity"] < quantity:
                raise ValueError(f"Not enough stock for {menu_item['name']}.")

            subtotal = round(menu_item["price"] * quantity, 2)
            total_price += subtotal
            menu_item["quantity"] -= quantity
            if menu_item["quantity"] <= 0:
                menu_item["available"] = False

            order_items.append(
                {
                    "menu_item_id": menu_item["id"],
                    "name": menu_item["name"],
                    "quantity": quantity,
                    "unit_price": menu_item["price"],
                    "subtotal": subtotal,
                }
            )

        order = {
            "id": next(self.order_id_counter),
            "service_boy_name": service_boy_name,
            "items": order_items,
            "total_price": round(total_price, 2),
            "created_at": datetime.utcnow().isoformat() + "Z",
        }
        self.orders.append(order)
        return order

    def list_inventory(self) -> List[Dict]:
        return [
            {
                "menu_item_id": item["id"],
                "name": item["name"],
                "quantity": item["quantity"],
                "available": item["available"],
            }
            for item in self.menu_items
        ]


store = CafeStore()

# Seed data so the dashboard has content on first load.
store.add_menu_item("Espresso", 120, True, 20)
store.add_menu_item("Cappuccino", 150, True, 15)
store.add_menu_item("Veg Sandwich", 90, True, 25)
store.add_staff_member("Amit")
store.add_staff_member("Rohit")
store.add_review(5, "Great coffee and friendly service.")
store.add_review(4, "Clean place with quick delivery.")


# Frontend page route.
@app.route("/")
def index():
    return render_template("index.html")


# Menu endpoints.
@app.route("/api/menu", methods=["GET", "POST"])
def menu_api():
    if request.method == "GET":
        return jsonify({"success": True, "data": store.menu_items})

    payload = request.get_json(force=True, silent=True) or {}
    name = str(payload.get("name", "")).strip()
    price = payload.get("price")
    available = bool(payload.get("available", True))
    quantity = int(payload.get("quantity", 10))

    if not name:
        return jsonify({"success": False, "message": "Menu item name is required."}), 400

    if price is None:
        return jsonify({"success": False, "message": "Price is required."}), 400

    try:
        menu_item = store.add_menu_item(name, float(price), available, quantity)
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Please provide a valid price and quantity."}), 400

    return jsonify({"success": True, "message": "Menu item added successfully.", "data": menu_item}), 201


# Inventory endpoint.
@app.route("/api/inventory", methods=["GET"])
def inventory_api():
    return jsonify({"success": True, "data": store.list_inventory()})


# Staff endpoints.
@app.route("/api/staff", methods=["GET", "POST"])
def staff_api():
    if request.method == "GET":
        return jsonify({"success": True, "data": store.staff_members})

    payload = request.get_json(force=True, silent=True) or {}
    name = str(payload.get("name", "")).strip()

    if not name:
        return jsonify({"success": False, "message": "Staff name is required."}), 400

    staff_member = store.add_staff_member(name)
    return jsonify({"success": True, "message": "Staff member added successfully.", "data": staff_member}), 201


# Review endpoints.
@app.route("/api/reviews", methods=["GET", "POST"])
def reviews_api():
    if request.method == "GET":
        return jsonify({"success": True, "data": store.reviews})

    payload = request.get_json(force=True, silent=True) or {}
    rating = payload.get("rating")
    comment = str(payload.get("comment", "")).strip()

    try:
        rating_value = int(rating)
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Rating must be a number from 1 to 5."}), 400

    if rating_value < 1 or rating_value > 5:
        return jsonify({"success": False, "message": "Rating must be between 1 and 5."}), 400

    if not comment:
        return jsonify({"success": False, "message": "Comment is required."}), 400

    review = store.add_review(rating_value, comment)
    return jsonify({"success": True, "message": "Review added successfully.", "data": review}), 201


# Order endpoints.
@app.route("/api/orders", methods=["POST"])
def orders_api():
    payload = request.get_json(force=True, silent=True) or {}
    service_boy_name = str(payload.get("service_boy_name", "")).strip()
    items = payload.get("items", [])

    if not isinstance(items, list) or not items:
        return jsonify({"success": False, "message": "At least one order item is required."}), 400

    try:
        order = store.place_order(service_boy_name, items)
    except ValueError as error:
        return jsonify({"success": False, "message": str(error)}), 400

    return jsonify({"success": True, "message": "Order placed successfully.", "data": order}), 201


if __name__ == "__main__":
    app.run(debug=True)
