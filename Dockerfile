FROM nvidia/cuda:10.2-runtime-ubuntu18.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y && \
    apt-get install -y \
        ca-certificates \
        build-essential \
        gfortran \
        g++ \
        git \
        python3 \
        python3-tk \
        python3-venv \
        python3-dev \
        python3-pip \
        libfreetype6-dev \
        dumb-init \
        nvidia-modprobe \
        libpq-dev \
	python-psycopg2 \
	nodejs \
	npm \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* \
	;

RUN mkdir /workdir

WORKDIR /workdir

COPY / /workdir/

RUN pip3 install -U pip

RUN pip3 install -r requirements.txt --extra-index-url https://pypi.rasa.com/simple

RUN chgrp -R 0 . && chmod -R g=u .

RUN chmod a+rwx models/20191211-172733.tar.gz

RUN chmod +777 /usr/lib/python3/dist-packages/ --recursive

EXPOSE 5005
