FROM python:3.11-slim AS python-base

FROM python-base AS dependencies

ENV PYTHONUNBUFFERED=1

WORKDIR /tmp

COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    pip install -U pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

FROM python-base AS runtime

WORKDIR /code

COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

COPY . /code/

ENV PYTHONPATH=/code
