import psycopg2
from ordersService.models import CreateOrder, OrderResponse, OrderItem

class PostgresClient:
    def __init__(self):
        self.conn = psycopg2.connect(
            "dbname=orders user=service password=secret host=localhost port=5432"
        )

    def create_order(self, order: CreateOrder) -> int:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO orders (user_id, status) VALUES (%s, %s) RETURNING order_id",
            (order.user_id, 'pending')
        )
        order_id = cur.fetchone()[0]

        for item in order.items:
            cur.execute(
                "INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)",
                (order_id, item.product_id, item.quantity)
            )

        self.conn.commit()
        cur.close()
        return order_id

    def get_order(self, order_id: int) -> OrderResponse:
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT o.order_id, o.user_id, o.status, o.created_at, 
                   i.product_id, i.quantity
            FROM orders o
            LEFT JOIN order_items i ON o.order_id = i.order_id
            WHERE o.order_id = %s
            """, (order_id,)
        )
        records = cur.fetchall()
        cur.close()

        if not records:
            return None

        items
