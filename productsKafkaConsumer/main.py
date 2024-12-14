from productsKafkaConsumer.clients.kafka import recive_orders_completed
from productsKafkaConsumer.models.db import ProductModel


def main():
    model = ProductModel.model_validate_json(b'{"id": 5}')
    recive_orders_completed()


if __name__ == "__main__":
    main()