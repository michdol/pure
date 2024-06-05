FROM python:3.12.3-slim-bullseye AS build

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        libpython3-dev \
        curl \
        sudo \
        libpq-dev \
        gcc && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

CMD mkdir /pure
COPY . /pure
WORKDIR /pure

RUN pip install -r /pure/requirements.txt

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
CMD tail -f /dev/null