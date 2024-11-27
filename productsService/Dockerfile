FROM python:3.12


WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN pip install fastapi[standart]
COPY . /app


CMD ["fastapi", "run", "main.py", "--port", "80"]
