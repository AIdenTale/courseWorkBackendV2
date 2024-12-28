FROM python:3.12

WORKDIR /app

COPY ./requirements.txt /app/reportKafkaConsumer/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/reportKafkaConsumer/requirements.txt

COPY . /app/reportKafkaConsumer

CMD ["python3", "main.py"]
