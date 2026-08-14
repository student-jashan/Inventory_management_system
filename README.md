# Inventory Management System

A full-stack Inventory Management System designed to manage products, categories, suppliers, purchases, sales, and stock efficiently.

The project provides a FastAPI-based REST API backend with JWT authentication and role-based authorization, a PostgreSQL database hosted on Supabase, and a frontend built using HTML, CSS, and JavaScript.

## 🚀 Live Demo

- **Frontend:** https://inventory-management-frontend-slfx.onrender.com
- **Backend API:** https://inventory-management-naki.onrender.com

---

## ✨ Features

### Authentication & Authorization

- User registration and login
- Password hashing
- JWT-based authentication
- Role-based access control
- Three user roles:
  - Admin
  - Sales Executive
  - Inventory Manager

### Product Management

- Create products
- View all products
- View product by ID
- Update products
- Delete products
- Category-based product management

### Category Management

- Create categories
- View categories
- Update categories
- Delete categories

### Supplier Management

- Add suppliers
- View suppliers
- Update suppliers
- Delete suppliers

### Purchase Management

- Create purchases
- View purchases
- View purchase by ID
- Update purchases
- Delete purchases
- Automatically increase product stock when a purchase is created
- Calculate purchase totals
- Maintain purchase items

### Sales Management

- Create sales
- View sales
- View sale by ID
- Update sales
- Delete sales
- Automatically decrease product stock when a sale is created
- Prevent sales when available stock is insufficient
- Calculate sale totals
- Maintain sale items

### Stock Management

The system automatically manages stock based on purchase and sales transactions.

```text
Purchase
   ↓
Product Stock Increases
   ↓
Inventory Updated


                    ┌─────────────────────┐
                    │      Frontend       │
                    │   HTML/CSS/JS       │
                    └──────────┬──────────┘
                               │
                               │ REST API
                               ▼
                    ┌─────────────────────┐
                    │     FastAPI         │
                    │      Backend        │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
             JWT Authentication    SQLAlchemy ORM
                                      │
                                      ▼
                              ┌─────────────────┐
                              │    Supabase     │
                              │   PostgreSQL    │
                              └─────────────────┘

🛠️ Technology Stack
Backend
Python
FastAPI
SQLAlchemy
Pydantic
PostgreSQL
Supabase
JWT
Password Hashing
Frontend
HTML5
CSS3
JavaScript
Deployment
Render
Supabase
GitHub
📁 Project Structure
Inventory_management_system/
│
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── style.css
│
├── src/
│   ├── main.py
│   │
│   ├── controllers/
│   │   ├── auth_controller.py
│   │   ├── category_controller.py
│   │   ├── product_controller.py
│   │   ├── supplier_controller.py
│   │   ├── purchase_controller.py
│   │   └── sale_controller.py
│   │
│   ├── models/
│   │   ├── user_model.py
│   │   ├── category_model.py
│   │   ├── product_model.py
│   │   ├── supplier_model.py
│   │   ├── purchase_model.py
│   │   └── sale_model.py
│   │
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── category_routes.py
│   │   ├── product_routes.py
│   │   ├── supplier_routes.py
│   │   ├── purchase_routes.py
│   │   └── sale_routes.py
│   │
│   ├── dtos/
│   │   ├── auth_dto.py
│   │   ├── category_dto.py
│   │   ├── product_dto.py
│   │   ├── supplier_dto.py
│   │   ├── purchase_dto.py
│   │   └── sale_dto.py
│   │
│   └── utils/
│       ├── db.py
│       ├── settings.py
│       └── jwt_handler.py
│
├── tests/
│
├── requirements.txt
├── .gitignore
└── README.md

The exact filenames may vary depending on the current project structure.

🗄️ Database

The application uses PostgreSQL with Supabase as the hosted database platform.

Major entities include:

User
 │
 └── Role


Category
 │
 └── Products


Supplier
 │
 └── Purchases
       │
       └── Purchase Items
              │
              └── Products


Sale
 │
 └── Sale Items
        │
        └── Products

⚙️ Local Installation
1. Clone the repository
git clone https://github.com/student-jashan/Inventory_management_system.git
cd Inventory_management_system
2. Create a virtual environment

Windows:

python -m venv venv
venv\Scripts\activate

Linux/macOS:

python3 -m venv venv
source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Configure environment variables

Create a .env file in the project root:

DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
ALGORITHM=algo
ACCESS_TOKEN_EXPIRE_MINUTES=time

Do not commit .env to GitHub.

5. Run the backend
uvicorn src.main:app --reload

The API will be available at:

http://127.0.0.1:8000

🌐 Frontend

The frontend is built using plain HTML, CSS and JavaScript.

Frontend = "https://inventory-management-frontend-slfx.onrender.com";

The frontend communicates with the FastAPI backend through REST APIs.


👨‍💻 Author

Jashandeep Kaur
B.Tech Computer Science & Engineering
