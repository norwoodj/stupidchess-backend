FROM python:3.11.4-slim-bookworm@sha256:55221704bcc5432f978bc5184d58f54c93ad25313363a1d0db20606a4cf2aef7
LABEL maintainer=norwood.john.m@gmail.com

ARG APP_DIR=/etc/stupidchess
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
COPY uwsgi.ini ./uwsgi.ini

ENTRYPOINT ["uwsgi", "--ini", "/etc/stupidchess/uwsgi.ini"]
