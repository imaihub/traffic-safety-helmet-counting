FROM ubuntu:24.04

COPY . /bikehelmets
WORKDIR /bikehelmets

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get -y install gcc && \
    apt-get -y install libgl1 && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.11 python3.11-distutils python3.11-venv && \
    apt-get install -y curl && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python3.11 -m pip install -r requirements.txt
RUN python3.11 -m pip install --no-deps -r requirements2.txt

ENV PYTHONPATH=/bikehelmets

CMD ["python3.11", "gradio_server/server.py"]

