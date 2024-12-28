import base64
import os

import aiohttp

from orderService.model.models import ProductInfo, ProductInfoInOrder
from orderService.model.tokenGenerator import TokenGeneratorTokenGenRequest, ServiceUnavailableException, \
    TokenVerifyException


async def get_products_byid(products_ids: list[int]) -> list[ProductInfo]:
    token = os.getenv("TOKEN")
    if token is None:
        raise ValueError("token is missing")


    products = []
    for product_id in products_ids:
        session = aiohttp.ClientSession()
        session.headers.setdefault('Authorization', "Bearer " + token)
        response = await session.get("http://localhost:8081/products/by_id?product_id="+str(product_id))


        if response.status == 500:
            raise ServiceUnavailableException("cannot make request")

        data = await response.json()
        if response.status == 400:
            raise TokenVerifyException(data)

        if response.status == 422:
            continue

        data = data[0]


        products.append(ProductInfoInOrder(id=data["id"], price=data["price"], size=data["size"], color=data["color"],
                                    country=data["country"],sku=data["sku"]))
        await session.close()

    return products

async def reverve_products(products_ids: list[int]) -> None:
    products = []
    for product_id in products_ids:
        session = aiohttp.ClientSession()
        response = await session.get("http://localhost:8081/cards/reserve?product_id="+str(product_id))

        if response.status == 500:
            raise ServiceUnavailableException("cannot make request")

        await session.close()

    return products