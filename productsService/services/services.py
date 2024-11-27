from productsService.db.client import PostgresClient


class ProductsService:
    def __init__(self):
        pass

    def get_all_products(self):
        client = PostgresClient()
        client.get_all_products()