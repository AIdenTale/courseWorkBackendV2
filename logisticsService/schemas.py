from typing import Optional

from datetime import datetime

from pydantic import BaseModel


class LogisticsOutput(BaseModel):
    id: int
    order_id: int
    delivery_date: Optional[datetime]
    delivery_point: Optional[str]
    status: Optional[str]
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        orm_mode = True