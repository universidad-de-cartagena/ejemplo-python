FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt \
    && apt-get update -y \
    && apt-get install -y --no-install-recommends \
        python3-dev \
        default-libmysqlclient-dev \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn

COPY notes/ notes/
COPY ejemploPython/ ejemploPython/
COPY manage.py .
COPY observability/ observability/

ENV OTEL_SERVICE_NAME=ejemplo-python \
    OTEL_SERVICE_VERSION=1.0.0 \
    OTEL_ENVIRONMENT=development \
    OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317

ENV DEBUG=False WAIT_HOSTS=database:3306

COPY scripts/docker-entrypoint.sh /bin
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.6.0/wait /bin/wait
RUN chmod a+x /bin/docker-entrypoint.sh /bin/wait
ENTRYPOINT ["docker-entrypoint.sh"]

EXPOSE 8080
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
