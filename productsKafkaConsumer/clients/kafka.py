from datetime import datetime

from confluent_kafka import Consumer, KafkaError

from productsKafkaConsumer.clients.db import delete_completed_product
from productsKafkaConsumer.models.db import ProductModel

consumer = Consumer({
    'bootstrap.servers': '88.218.66.164:9092',
    'auto.offset.reset': 'earliest',
    'group.id': 'products-6',
    'enable.auto.commit': False
})
consumer.subscribe(["orders-completed"])

def recive_orders_completed():
    while True:
        msg = consumer.poll(0.05)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f'Error while consuming orders-completed: {msg.error()}')
        else:
            value = msg.value()
            print(f'[{datetime.now()}] Received msg')

            product = ProductModel.model_validate_json(value)

            try:
                delete_completed_product(product)
                print(f'[{datetime.now()}]: Product {product.id} deleted')
            except Exception as e:
                print(f'[{datetime.now()}] Error while deleting completed product: {e}')