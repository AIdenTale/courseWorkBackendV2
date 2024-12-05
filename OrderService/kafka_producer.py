from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_to_kafka(order_id, user_id, items):
    producer.send('orders', {
        'order_id': order_id,
        'user_id': user_id,
        'items': [{'product_id': item.product_id, 'quantity': item.quantity} for item in items]
    })
