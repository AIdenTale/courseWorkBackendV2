from typing import Tuple, Any

import psycopg2

conn = psycopg2.connect("dbname=products user=service password=hsdg4731jhpasklaksd host=88.218.66.164 port=5432")


async def get_all_user_orders(user_id: int):
    query = "select * from orders s LEFT JOIN order_products p on s.id = p.order_id WHERE user_id = %s;"
    records = execute_sql_query(query, (user_id,))


def execute_sql_query(query: str, args: Tuple[Any, ...] | None = None, must_commit: bool | None = None) -> Any:
    cur = conn.cursor()
    cur.execute(query, args)

    if must_commit is not None:
        conn.commit()


        if "RETURNING" in query:
            records = cur.fetchall()
            return records

        return

    records = cur.fetchall()
    return records