FROM python:3.7-slim
LABEL maintainer=norwood.john.m@gmail.com

ARG APP_DIR=/opt/stupidchess
WORKDIR ${APP_DIR}

COPY Pipfile Pipfile.lock ./
RUN pip install --upgrade \
        pip \
        pipenv \
        setuptools \
        wheel \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libffi-dev \
        libssl-dev \
    && pipenv install --system \
    && mkdir -p /opt/stupidchess/logs \
    && ln -s /dev/stdout /opt/stupidchess/logs/app.log

COPY setup.py ./setup.py
COPY stupidchess ./stupidchess
RUN pip install .

COPY config ./config
COPY uwsgi.ini ./uwsgi.ini

ENTRYPOINT ["uwsgi", "--ini", "/opt/stupidchess/uwsgi.ini"]
