
FROM python:3.8

RUN mkdir /app
WORKDIR /app

RUN apt update && \
    apt install -y postgresql-client

COPY Pipfile ./
RUN pip install pipenv
RUN pipenv install --no-cache-dir --system

COPY . .