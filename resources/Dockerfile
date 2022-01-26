FROM discord-bots/base:latest

COPY resources .

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

USER discord