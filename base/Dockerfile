FROM ubuntu:latest

RUN apt-get update && \
    apt-get -y install python3 \
                       python3-dev \
                       python3-pip \
                       git \
                       wget \
                       vim

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

RUN useradd -u 8787 -m discord

WORKDIR /home/discord
