FROM python:3.7
MAINTAINER Alexandre Ribeiro <alexolirib@gmail.com>

COPY requirements.txt /tmp

RUN useradd -m -d /app innovation_dreams && \
    apt-get update && \
    apt-get -y install libpq-dev python3-dev vim && \
    pip install -r /tmp/requirements.txt

USER innovation_dreams
WORKDIR /app
EXPOSE 8000

COPY --chown=innovation_dreams:innovation_dreams . innovation_dreams
WORKDIR /app/innovation_dreams

ENTRYPOINT bash app.sh