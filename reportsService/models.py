from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from orderService.database import Base

class ReportOrder(Base):
    __tablename__ = 'report_orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    report_id = Column(Integer, nullable=False)
    order_id = Column(Integer, nullable=False)
    customer_name = Column(String(255), nullable=False)
    order_status = Column(String(50), nullable=False)
    total_amount = Column(Float, nullable=False)
    order_date = Column(DateTime, nullable=False)