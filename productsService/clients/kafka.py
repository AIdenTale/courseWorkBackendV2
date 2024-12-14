import datetime

from confluent_kafka import Producer

from productsService.models.api import ProductModel, ProductsCardModel

producer = Producer({
    'bootstrap.servers': '88.218.66.164:9092',
})

async def send_new_product_to_kafka(product: ProductModel):
    try:
        data = product.model_dump_json().encode('utf-8')
        producer.produce('products-new', value=data)
        producer.flush()
        print(f"[{datetime.datetime.now()}] Product {product.id} sent to Kafka]")
    except Exception as e:
        print(f'Error sending data to kafka topic: products-new product_id: {product.id}: {e}')

async def send_deleted_product_to_kafka(product: ProductModel):
    try:
        data = product.model_dump_json().encode('utf-8')
        producer.produce('products-deleted', value=data)
        producer.flush()
        print(f"[{datetime.datetime.now()}] Product {product.id} sent to Kafka")
    except Exception as e:
        print(f'Error sending data to kafka topic: products-deleted product_id: {product.id}: {e}')


async def send_new_card_to_kafka(card: ProductsCardModel):
    try:
        data = card.model_dump_json().encode('utf-8')
        producer.produce('cards-new', value=data)
        producer.flush()
        print(f"[{datetime.datetime.now()}] Card {card.id} sent to Kafka]")
    except Exception as e:
        print(f'Error sending data to kafka topic: cards-new card_id: {card.id}: {e}')

async def send_deleted_card_to_kafka(card: ProductsCardModel):
    try:
        data = card.model_dump_json().encode('utf-8')
        producer.produce('cards-deleted', value=data)
        producer.flush()
        print(f"[{datetime.datetime.now()}] Card {card.id} sent to Kafka")
    except Exception as e:
        print(f'Error sending data to kafka topic: cards-deleted product_id: {card.id}: {e}')