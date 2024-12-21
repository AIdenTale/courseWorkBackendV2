FROM python:3.12

WORKDIR /app

# Установка зависимостей
COPY ./requirements.txt /app/reportKafkaConsumer/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/reportKafkaConsumer/requirements.txt

# Копирование файлов сервиса
COPY . /app/reportKafkaConsumer

CMD ["python3", "main.py"]
