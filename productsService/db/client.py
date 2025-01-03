import psycopg2
from typing import Any, Tuple
import inspect

from productsService.models.api import ProductsCardModel, ProductsCardInputModel, ProductsCardInputEditModel, \
    ProductInputModel, ProductInputEditModel
from productsService.models.db import ProductModel
from productsService.models.exception import ForeignKeyViolation, ZeroLinesUpdated

conn = psycopg2.connect("dbname=products user=root password=mypassword host=213.171.25.1 port=5432")
def execute_sql_query(query: str, args: Tuple[Any, ...] | None = None, must_commit: bool | None = None) -> Any:
    cur = conn.cursor()
    cur.execute(query, args)

    if must_commit is not None:
        conn.commit()

        if cur.rowcount == 0 and "update" in query:
            raise ZeroLinesUpdated("id не существует")

        if "RETURNING" in query:
            records = cur.fetchall()
            return records

        return

    records = cur.fetchall()
    return records
def get_products_with_sql_request(request: str, args: Tuple[Any, ...] | None = None) -> list[ProductModel] | None:
    records = execute_sql_query(request, args)

    if len(records) == 0:
        return None

    products = []
    for record in records:
        products.append(
            ProductModel(id=record[0], price=record[1], size=record[2], color=record[3],
                         country=record[4], sku=record[7]))

    return products

def get_cards_with_sql_request(request: str, args: Tuple[Any, ...] | None = None) -> list[ProductsCardModel] | None:
        records = execute_sql_query(request, args)

        cards_models = []
        if len(records) != 0:
            for record in records:
                cards_models.append(ProductsCardModel(id=record[0], title=record[1], description=record[2], brand=record[3],))
        else:
            return None

        for card in cards_models:
            products = get_products_with_sql_request("SELECT * FROM public.products WHERE card_id = %s AND is_reserved = false", (card.id,))

            card.products = products if products else []
            card.count = len(products) if products else 0

        return cards_models



def all_products_cards() -> list[Any]:
        return get_cards_with_sql_request("SELECT * FROM public.products_card")

def product_card_by_id(id: int) -> list[Any]:
        return get_cards_with_sql_request("SELECT * FROM public.products_card WHERE id = %s", (id,))

def create_new_card(card: ProductsCardInputModel) -> list[Any]:
        records =  execute_sql_query("insert into public.products_card (title, description, brand) values (%s, %s, %s) RETURNING id;", (card.title, card.description, card.brand), True)
        return records[0]

def edit_card(card: ProductsCardInputEditModel):
    attributes = inspect.getmembers(ProductsCardInputModel, lambda a: not (inspect.isroutine(a)))
    elems = [x[1].keys() for x in [a for a in attributes if not (a[0].startswith('__'))] if x[0] == "model_fields"][0]
    sets_query = ""
    args_query = []
    for elem in elems:
        attribute = getattr(card, elem)
        if attribute is not None:
            sets_query += "set " + elem + " = %s,"
            args_query.append(attribute)
    args_query.append(card.id)
    sets_query = sets_query[0:len(sets_query)-1]
    execute_sql_query(f"update public.products_card {sets_query} where id = %s;",
                                tuple(args_query), True)
    return

def delete_card(card_id: int):
    execute_sql_query("delete from public.products_card where id = %s",
                      (card_id,), True)
    return


def all_products() -> list[Any]:
    return get_products_with_sql_request("SELECT * FROM public.products WHERE is_reserved = false")


def product_by_id(id: int) -> list[Any]:
    return get_products_with_sql_request("SELECT * FROM public.products WHERE id = %s AND is_reserved = false", (id,))

def product_by_card_id_and_sku(card_id: int, sku: int) -> list[Any]:
    return get_products_with_sql_request("SELECT * FROM public.products WHERE card_id = %s AND sku = %s", (card_id, sku))

def create_new_product(product: ProductInputModel) -> list[Any]:
    try:
        records = execute_sql_query(
            "insert into public.products (price, size, color, country, card_id, is_reserved, sku) values "
            "(%s, %s, %s, %s, %s, %s, %s) RETURNING id;",
            (product.price, product.size, product.color, product.country, product.card_id, False, product.sku),
            True)
        return records[0]
    except psycopg2.errors.ForeignKeyViolation as ex:
        raise ForeignKeyViolation("Такого card_id не существует")


def edit_product(product: ProductInputEditModel):

    products = get_products_with_sql_request("SELECT * FROM public.products WHERE id = %s AND is_reserved = true", (product.id,))
    if products is not None:
        raise ValueError("Продукт в заказе, невозможно изменить")

    attributes = inspect.getmembers(ProductInputEditModel, lambda a: not (inspect.isroutine(a)))
    elems = [x[1].keys() for x in [a for a in attributes if not (a[0].startswith('__'))] if x[0] == "model_fields"][0]
    sets_query = "set "
    args_query = []
    for elem in elems:
        attribute = getattr(product, elem)
        if attribute is not None:
            sets_query +=  elem + " = %s,"
            args_query.append(attribute)
    args_query.append(product.id)
    sets_query = sets_query[0:len(sets_query) - 1]
    try:
        execute_sql_query(f"update public.products {sets_query} where id = %s;",
                          tuple(args_query), True)
    except psycopg2.errors.ForeignKeyViolation as ex:
        raise ForeignKeyViolation("Такого card_id не существует")
    return

def delete_product(product_id: int):
    products = get_products_with_sql_request("SELECT * FROM public.products WHERE id = %s AND is_reserved = true", (product_id,))
    if len(products) != 0:
        raise ValueError("Продукт в заказе, невозможно удалить")

    execute_sql_query("delete from public.products where id = %s",
                      (product_id,), True)
    return

def reserve_product(product_id: int):
    execute_sql_query("update public.products set is_reserved = true where id = %s", (product_id,), True)
    return

def reserve_delete_product(product_id: int):
    execute_sql_query("update public.products set is_reserved = false where id = %s", (product_id,), True)
    return