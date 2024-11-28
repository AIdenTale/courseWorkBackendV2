import psycopg2
from ordersService.models import CreateOrder, OrderResponse, OrderItem, ProductDetail

class PostgresClient:
    def __init__(self):
        # Подключение к базе данных
        self.conn = psycopg2.connect(
            "dbname=orders user=service password=hsdg4731jhpasklaksd host=88.218.66.164 port=5432"
        )

    def create_order(self, order: CreateOrder) -> int:
        cur = self.conn.cursor()
        try:
            # Создаем заказ
            cur.execute(
                "INSERT INTO orders (user_id, status) VALUES (%s, %s) RETURNING order_id",
                (order.user_id, 'pending')
            )
            order_id = cur.fetchone()[0]

            # Добавляем позиции заказа
            for item in order.items:
                cur.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)",
                    (order_id, item.product.product_id, item.quantity)
                )

            self.conn.commit()
            return order_id
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cur.close()

    def get_order(self, order_id: int) -> OrderResponse:
        cur = self.conn.cursor()
        try:
            # Получаем детали заказа
            cur.execute(
                """
                SELECT o.order_id, o.user_id, o.status, o.created_at, 
                       p.product_id, p.title, p.brand, p.price, p.color, p.size, i.quantity
                FROM orders o
                LEFT JOIN order_items i ON o.order_id = i.order_id
                LEFT JOIN products p ON i.product_id = p.product_id
                WHERE o.order_id = %s
                """, (order_id,)
            )
            records = cur.fetchall()

            if not records:
                return None

            items = [
                OrderItem(
                    product=ProductDetail(
                        product_id=rec[4],
                        title=rec[5],
                        brand=rec[6],
                        price=rec[7],
                        color=rec[8],
                        size=rec[9],
                    ),
                    quantity=rec[10]
                )
                for rec in records
            ]
            order_data = records[0]
            return OrderResponse(
                order_id=order_data[0],
                user_id=order_data[1],
                status=order_data[2],
                created_at=order_data[3],
                items=items
            )
        except Exception as e:
            raise e
        finally:
            cur.close()
