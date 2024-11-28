FROM python:3.12

WORKDIR /app
COPY ./requirements.txt /app/tokenGeneratorService/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/tokenGeneratorService/requirements.txt
COPY . /app/tokenGeneratorService
ENV PYTHONPATH=/app

CMD ["uvicorn", "--app-dir=tokenGeneratorService", "main:app", "--host=0.0.0.0", "--port=8080"]
