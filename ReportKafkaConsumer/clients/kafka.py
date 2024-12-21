from datetime import datetime
from confluent_kafka import Consumer, KafkaError

from reportKafkaConsumer.clients.db import delete_completed_report
from reportKafkaConsumer.models.db import ReportModel

# Конфигурация Kafka Consumer
consumer = Consumer({
    'bootstrap.servers': '88.218.66.164:9092',
    'auto.offset.reset': 'earliest',
    'group.id': 'reports-1',
    'enable.auto.commit': False
})

# Подписка на топик
consumer.subscribe(["orders-completed"])

def receive_orders_completed():
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

            report = ReportModel.model_validate_json(value)

            try:
                delete_completed_report(report)
                print(f'[{datetime.now()}]: Report {report.id} deleted')
            except Exception as e:
                print(f'[{datetime.now()}] Error while deleting completed report: {e}')
