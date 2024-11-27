from fastapi import FastAPI

from db.client import PostgresClient

app = FastAPI()


@app.get("/products/all")
async def products_all():
    client = PostgresClient()
    return client.get_all_products()
