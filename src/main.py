from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from src.routes import category_routes, supplier_routes
from src.utils.db import engine, Base
import src.models.category
import src.models.product
import src.models.supplier
from src.routes.category_routes import category_routes as category_routes
from src.routes.product_routes import product_routes as product_routes
from src.routes.supplier_routes import supplier_routes as supplier_routes
from src.routes.purchase_routes import purchase_routes
from src.routes.sales_routes import sales_router as routes
from src.models.user import UserModel
from src.routes.auth_routes import router as auth_router

Base.metadata.create_all(engine)
app = FastAPI (title = "Inventory Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(category_routes)
app.include_router(product_routes)
app.include_router(supplier_routes)
app.include_router(purchase_routes)
app.include_router(routes)
app.include_router(auth_router)
