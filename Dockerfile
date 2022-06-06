# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /application

# Installing Dependencies
RUN pip install --upgrade pip && pip install pipenv

COPY ./Pipfile* /application/
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --system --deploy

COPY . /application/
CMD gunicorn wsgi:app --bind 0.0.0.0:$PORT