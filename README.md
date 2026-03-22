# 🧠 BioLogist Backend (Django REST API)

## 📌 Description
This is the backend of the BioLogist e-commerce platform built using Django and Django REST Framework. It provides RESTful APIs for managing products, users, cart, and orders.

---

## 🚀 Features
- Product management (list, add, update, delete)
- Cart functionality (add/remove/update items)
- Order management
- REST API integration with frontend
- Relational database design

---

## 🛠️ Tech Stack
- Python
- Django
- Django REST Framework (DRF)
- SQLite / MySQL
- REST APIs

---

## 🗄️ Database Models
- **User** – stores user information
- **Product** – product details (name, price, etc.)
- **Cart** – linked to user
- **CartItem** – products inside cart
- **Order** – final purchase data

---

## 🔗 API Endpoints

### Products
- `GET /products/` → Get all products
- `POST /products/` → Add new product

### Cart
- `POST /cart/` → Add item to cart
- `PUT /cart/` → Update cart item
- `DELETE /cart/` → Remove item

### Orders
- `POST /order/` → Place order

---

## ⚙️ Business Logic

- **Add to Cart**:
  - Checks if product already exists in cart
  - If yes → updates quantity
  - If no → creates new cart item

- **Order Creation**:
  - Converts cart items into order records
  - Clears cart after order is placed

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
