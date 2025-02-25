FROM python:3.12-alpine AS base

# VENV not needed in docker container
ENV POETRY_VIRTUALENVS_CREATE=false 

WORKDIR /app

COPY . . 

# Install dependencies
RUN pip install poetry
RUN poetry install


FROM base as dev

# Expose development port
EXPOSE 5000

# Include host flag to make flask listen on all interfaces
# Otherwise it is not accessible from the outside.
CMD [ "flask", "--app", "senju/main", "run", "--debug", "--host=0.0.0.0"]

