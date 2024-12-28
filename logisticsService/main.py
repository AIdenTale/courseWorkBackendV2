from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from datetime import datetime
from starlette.requests import Request
from starlette.responses import JSONResponse
from typing import Optional

from logisticsService.database import SessionLocal
from logisticsService.middlewares import verify_token_middleware
from logisticsService.models import LogisticsDB
from logisticsService.schemas import LogisticsOutput

app = FastAPI()


# Dependency для сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/logistics/get_info")
async def get_order_info(request: Request, db: Session = Depends(get_db)):
    result = await verify_token_middleware(request)
    if isinstance(result, JSONResponse):
        return result


    user_id = result.id
    logistics = db.query(LogisticsDB).filter(LogisticsDB.user_id == user_id).all()
    if not logistics:
        raise HTTPException(status_code=404, detail="Order not found")
    return logistics
