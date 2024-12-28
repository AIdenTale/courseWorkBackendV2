import datetime

import sqlalchemy
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import JSONResponse

from orderService.clients.productsService import get_products_byid, reverve_products
from orderService.database import SessionLocal
from orderService.kafka_producer import send_kafka_event
from orderService.middlewares import verify_token_middleware
from orderService.model.models import OrderInfo, ProductInfo, ProductInfoInOrder, OrderInfoToProducts
from orderService.model.tokenGenerator import TokenGeneratorTokenGenRequest
from orderService.models import Order, OrderProduct
from orderService.schemas import OrderResponseSchema, OrderCreateSchema, OrderResponseSchemaDetailed
from reportsService.database import get_db, get_aggregated_statuses_data

app = FastAPI(title="Order Service")


@app.get("/get_aggregated_order_states")
async def get_order(request: Request, db: Session = Depends(get_db)):
    result = await verify_token_middleware(request)
    if isinstance(result, JSONResponse):
        return result

    aggregatedData = await get_aggregated_statuses_data()
    if not aggregatedData:
        raise HTTPException(status_code=404, detail="Order not found")
    return aggregatedData
