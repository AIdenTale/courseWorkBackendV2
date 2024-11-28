FROM python:3.12

WORKDIR /app
COPY ./requirements.txt /app/productsService/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/productsService/requirements.txt
COPY . /app/productsService
ENV PYTHONPATH=/app

CMD ["uvicorn", "--app-dir=productsService", "main:app", "--host=0.0.0.0", "--port=8080"]