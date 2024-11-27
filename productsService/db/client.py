import psycopg2
from typing import Any

from models.db import ProductModel


class PostgresClient():
    def __init__(self):
        self.conn = psycopg2.connect(
            "dbname=products user=service password=hsdg4731jhpasklaksd host=88.218.66.164 port=5432")

    def get_all_products(self) -> list[Any]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM public.products")
        records = cur.fetchall()

        models = []
        if len(records) != 0:
            for record in records:
                models.append(ProductModel(id=record[0], title=record[1], brand=record[2], price=record[3], size=record[4], color=record[5], country=record[6]))

        return models