FROM python:3.12-alpine AS base

ENV POETRY_VIRTUALENVS_CREATE=true
ENV FLASK_APP=senju/main.py

COPY ./entrypoint.sh /

WORKDIR /app

COPY . .

# Install dependencies
RUN apk add curl
RUN pip install poetry
RUN poetry install

FROM base as dev

# Expose development port
EXPOSE 5000

RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
