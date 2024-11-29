from ordersService.db import PostgresClient
from ordersService.kafka_producer import send_to_kafka
from ordersService.models import CreateOrder, OrderResponse

class OrderService:
    def __init__(self):
        self.db = PostgresClient()

    def create_order(self, order: CreateOrder) -> int:
        order_id = self.db.create_order(order)
        send_to_kafka(order_id, order.user_id, order.items)
        return order_id

    def get_order(self, order_id: int) -> OrderResponse:
        return self.db.get_order(order_id)
