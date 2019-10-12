FROM python:3.7.4-alpine

RUN apk update \
    # gcc for uvicorn
    && apk add build-base
COPY requirements.txt /requirements/
RUN pip install -r /requirements/requirements.txt

WORKDIR /app