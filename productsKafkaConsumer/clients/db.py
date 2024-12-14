from typing import Tuple, Any

import psycopg2

from productsService.models.api import ProductModel

conn = psycopg2.connect("dbname=products user=service password=hsdg4731jhpasklaksd host=88.218.66.164 port=5432")

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

def delete_completed_product(product: ProductModel):
    execute_sql_query("delete from public.products where id = %s",
                      (product.id,), True)

    return