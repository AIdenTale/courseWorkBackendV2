from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()

class LogisticsDB(Base):
    __tablename__ = 'logistics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, nullable=False)
    delivery_date = Column(DateTime, nullable=False)
    delivery_point = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    user_id = Column(Integer, nullable=False)

