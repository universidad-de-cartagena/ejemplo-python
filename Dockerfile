FROM python:3.7.3-alpine3.10

WORKDIR /app

# Dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Code
COPY notes/ notes/
COPY ejemploPython/ ejemploPython/
COPY manage.py .

ENV DEBUG=False

# Convenient entrypoint
COPY scripts/docker-entrypoint.sh /bin
RUN chmod a+x /bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]

# Expose service
EXPOSE 8080
CMD python manage.py runserver 0.0.0.0:8080