import psycopg2
from typing import Any

from productsService.models.api import ProductsCardModel
from productsService.models.db import ProductModel


class PostgresClient():
    def __init__(self):
        self.conn = psycopg2.connect(
            "dbname=products user=service password=hsdg4731jhpasklaksd host=88.218.66.164 port=5432")

    def get_all_products(self) -> list[Any]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM public.products_card")
        records = cur.fetchall()

        cards_models = []
        if len(records) != 0:
            for record in records:
                cards_models.append(ProductsCardModel(id=record[0], title=record[1], description=record[2]))
        else:
            return cards_models

        cur.close()
        for card in cards_models:
            card_id = card.id

            cur = self.conn.cursor()
            cur.execute("SELECT * FROM public.products WHERE card_id = %s", (card_id,))

            records = cur.fetchall()

            if len(records) == 0:
                continue

            products = []
            for record in records:
                products.append(ProductModel(id=record[0], brand=record[1], price=record[2], size=record[3], color=record[4], country=record[5], card_id=card_id))

            card.products = products
            card.count = len(products)


        cur.close()
        return cards_models