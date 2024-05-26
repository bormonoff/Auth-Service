FROM python:3.12.0

ENV POETRY_VERSION 1.7.1

WORKDIR /app

RUN pip install poetry==$POETRY_VERSION

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
  && poetry install --no-root

COPY . .
