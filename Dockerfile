FROM docker.io/python:3.13-slim-trixie

WORKDIR /app

# Pip dependencies, mysqlclient requires build deps that are auto removed for space
COPY requirements.txt .
RUN apt update -y \
    && apt install -y --no-install-recommends \
        build-essential pkg-config libpython3-dev default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --no-cache-dir -r requirements.txt \
    && apt remove -y build-essential pkg-config libpython3-dev default-libmysqlclient-dev \
    && apt autoremove -y

# Code
COPY notes/ notes/
COPY ejemploPython/ ejemploPython/
COPY manage.py .

ENV DEBUG=False WAIT_HOSTS=database:3306

# Convenient entrypoint and wait program
COPY scripts/docker-entrypoint.sh /bin
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.6.0/wait /bin/wait
RUN chmod a+x /bin/docker-entrypoint.sh /bin/wait
ENTRYPOINT ["docker-entrypoint.sh"]

# Expose service
EXPOSE 8080
CMD python manage.py runserver 0.0.0.0:8080
