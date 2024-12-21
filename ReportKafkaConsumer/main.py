from reportKafkaConsumer.clients.kafka import receive_orders_completed
from reportKafkaConsumer.models.db import ReportModel


def main():
    model = ReportModel.model_validate_json(b'{"id": 5}')
    receive_orders_completed()


if __name__ == "__main__":
    main()
