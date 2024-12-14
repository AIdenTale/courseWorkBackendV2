FROM python:3.12

WORKDIR /app
COPY ./requirements.txt /app/productsKafkaConsumer/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/productsKafkaConsumer/requirements.txt
COPY . /app/productsKafkaConsumer

CMD ["python3", "main.py"]