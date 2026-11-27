from fastapi import FastAPI

app = FastAPI()

from auth_routes import auth_router
from order_routes import order_router
from product_routes import product_router

app.include_router(auth_router)
app.include_router(order_router)
app.include_router(product_router)