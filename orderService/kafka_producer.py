from confluent_kafka import Producer
import json

producer = Producer({
    'bootstrap.servers': '88.218.66.164:9092'
})

def send_kafka_event(topic: str, event: dict):
    producer.produce(topic, json.dumps(event).encode('utf-8'))
    producer.flush()
