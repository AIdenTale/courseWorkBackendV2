FROM python:3.12

WORKDIR /app
COPY ./requirements.txt /app/orderServise/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/orderServise/requirements.txt
COPY . /app/authService
ENV PYTHONPATH=/app

CMD ["uvicorn", "--app-dir=orderServise", "main:app", "--host=0.0.0.0", "--port=8080"]