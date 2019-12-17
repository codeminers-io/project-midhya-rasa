FROM nvidia/cuda:10.2-runtime-ubuntu18.04 AS builder

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

RUN mkdir /rasa

WORKDIR /rasa

COPY / /rasa/

RUN pip3 install -U pip

RUN pip3 install -r requirements.txt --extra-index-url https://pypi.rasa.com/simple

FROM haskell:8 AS stackbuilder

RUN apt-get update -qq && \
  apt-get install -qq -y libpcre3 libpcre3-dev build-essential --fix-missing --no-install-recommends && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* 

RUN mkdir /log
RUN mkdir d
WORKDIR d

ADD /duckling/ /d/

RUN stack setup

# NOTE:`stack build` will use as many cores as are available to build
# in parallel. However, this can cause OOM issues as the linking step
# in GHC can be expensive. If the build fails, try specifying the
# '-j1' flag to force the build to run sequentially.
RUN stack install

FROM nvidia/cuda:10.2-runtime-ubuntu18.04
WORKDIR /app

COPY --from=builder /rasa .
COPY --from=stackbuilder /d .

EXPOSE 8000
EXPOSE 5005
