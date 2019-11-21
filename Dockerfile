FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install python3 python3-pip -y && \
    pip3 install pipenv

ENV LC_ALL=C.UTF-8 LANG=C.UTF-8

EXPOSE 80/tcp

COPY . /app
WORKDIR /app

RUN pipenv install --deploy --system

ENV UPLOADS_DIR=uploads/
# Comment this out to create the directory on container launch!
# RUN mkdir -p uploads/

CMD gunicorn --bind 0.0.0.0:80 dino
