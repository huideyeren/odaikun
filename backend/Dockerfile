
FROM python:3.8

RUN mkdir /app
WORKDIR /app

RUN apt update && \
    apt install -y postgresql-client

RUN pip install --upgrade pip && pip install pipenv --no-cache-dir && \
    pipenv install --system --deploy --dev && \
    pipenv lock -r requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .