from productsService.db.client import PostgresClient



async def get_all_products():
    client = PostgresClient()
    return client.get_all_products()

async def get_products_by_id():
    client = PostgresClient()
    return client.get_all_products()