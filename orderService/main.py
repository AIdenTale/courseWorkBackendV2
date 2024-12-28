from fastapi import FastAPI
from orderService.routers import orders

app = FastAPI(title="Order Service")

app.include_router(orders.router)
