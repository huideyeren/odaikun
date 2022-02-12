
FROM python:3.10.0b3

RUN mkdir /app
WORKDIR /app

RUN apt update && \
    apt install -y postgresql-client

RUN pip install --upgrade pip && pip install pipenv --no-cache-dir
COPY Pipfile /app
COPY Pipfile.lock /app
RUN pipenv install --system --deploy --dev

COPY . .