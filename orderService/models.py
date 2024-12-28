from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from orderService.database import Base

# Модель заказа
class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    order_date = Column(TIMESTAMP)
    status = Column(String, default='pending')
    total_amount = Column(Float, default=0.0)
    products = relationship("OrderProduct", back_populates="order")

# Модель товаров в заказе
class OrderProduct(Base):
    __tablename__ = 'order_products'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'))
    price = Column(Float)
    size = Column(String(50))
    color = Column(String(50))
    country = Column(String(100))
    sku = Column(Integer)
    card_id = Column(Integer)

    order = relationship("Order", back_populates="products")
