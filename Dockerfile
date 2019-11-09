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
    && pipenv install --system

COPY setup.py ./setup.py
COPY stupidchess ./stupidchess
RUN pip install .

COPY config ./config
COPY etc/uwsgi/uwsgi.ini /etc/uwsgi/uwsgi.ini

ENTRYPOINT ["uwsgi", "--ini", "/etc/uwsgi/uwsgi.ini"]
