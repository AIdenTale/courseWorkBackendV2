FROM python:3.12

WORKDIR /app
COPY ./requirements.txt /app/authService/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/authService/requirements.txt
COPY . /app/authService
ENV PYTHONPATH=/app

CMD ["uvicorn", "--app-dir=authService", "main:app", "--host=0.0.0.0", "--port=8080"]